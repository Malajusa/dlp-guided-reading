#!/usr/bin/env python3
"""Audit the structural contract of a weekly Shared and Guided Reading pack.

The audit intentionally uses only the Python standard library. It checks PPTX
package structure and the explicit layout manifest; it does not replace visual,
pedagogical, factual, cultural, or accessibility review.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import zipfile
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
NS = {"p": P_NS, "a": A_NS, "r": R_NS, "pr": PKG_REL_NS}

A4_LANDSCAPE_EMU = (10_692_000, 7_560_000)
SIZE_TOLERANCE_EMU = 2_000
EXPECTED_GROUPS = [
    ("Alpha", "Monday", "very low", "strongest"),
    ("Beta", "Tuesday", "low", "substantial"),
    ("Gamma", "Wednesday", "at level", "moderate"),
    ("Delta", "Thursday", "above level", "minimal"),
    ("Epsilon", "Friday", "Year 9 reading level", "none"),
]
GROUP_WORDS = "|".join(group.lower() for group, _, _, _ in EXPECTED_GROUPS)


def qname(namespace: str, local: str) -> str:
    return f"{{{namespace}}}{local}"


def normalise_text(text: str, *, ignore_copy_number: bool = False) -> str:
    text = text.replace("\u00a0", " ")
    if ignore_copy_number:
        text = re.sub(r"\bcopy\s+\d+\s+of\s+7\b", "copy # of 7", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def passage_text(text: str) -> str:
    text = text.lower()
    text = re.sub(rf"\b(?:{GROUP_WORDS})\b", " ", text)
    text = re.sub(r"\bcopy\s+\d+\s+of\s+7\b", " ", text)
    text = re.sub(r"\bpage\s+\d+\s+of\s+\d+\b", " ", text)
    text = re.sub(r"[^a-z0-9']+", " ", text)
    return normalise_text(text)


def relationship_map(blob: bytes) -> dict[str, str]:
    root = ET.fromstring(blob)
    return {
        rel.attrib["Id"]: rel.attrib["Target"]
        for rel in root.findall("pr:Relationship", NS)
        if "Id" in rel.attrib and "Target" in rel.attrib
    }


def resolve_target(base_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(base_part), target))


class PptxDeck:
    def __init__(self, path: Path):
        self.path = path
        self.slide_size = (0, 0)
        self.slides: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not self.path.is_file():
            raise ValueError(f"PowerPoint not found: {self.path}")
        if self.path.suffix.lower() != ".pptx":
            raise ValueError(f"Expected .pptx: {self.path}")

        with zipfile.ZipFile(self.path) as archive:
            names = set(archive.namelist())
            presentation_part = "ppt/presentation.xml"
            presentation_rels = "ppt/_rels/presentation.xml.rels"
            if presentation_part not in names or presentation_rels not in names:
                raise ValueError(f"Invalid PPTX package: {self.path}")

            root = ET.fromstring(archive.read(presentation_part))
            size = root.find("p:sldSz", NS)
            if size is not None:
                self.slide_size = (int(size.attrib.get("cx", "0")), int(size.attrib.get("cy", "0")))

            pres_rels = relationship_map(archive.read(presentation_rels))
            ordered_parts: list[str] = []
            for slide_id in root.findall("p:sldIdLst/p:sldId", NS):
                rel_id = slide_id.attrib.get(qname(R_NS, "id"))
                if not rel_id or rel_id not in pres_rels:
                    raise ValueError(f"Unresolved slide relationship in {self.path}")
                ordered_parts.append(resolve_target(presentation_part, pres_rels[rel_id]))

            for part in ordered_parts:
                if part not in names:
                    raise ValueError(f"Missing slide part {part} in {self.path}")
                slide_xml = archive.read(part)
                slide_root = ET.fromstring(slide_xml)
                texts = [node.text or "" for node in slide_root.findall(".//a:t", NS)]

                rel_part = posixpath.join(
                    posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels"
                )
                slide_rels = relationship_map(archive.read(rel_part)) if rel_part in names else {}
                image_hashes: list[str] = []
                for blip in slide_root.findall(".//a:blip", NS):
                    rel_id = blip.attrib.get(qname(R_NS, "embed"))
                    if not rel_id or rel_id not in slide_rels:
                        image_hashes.append("missing-relationship")
                        continue
                    target = resolve_target(part, slide_rels[rel_id])
                    if target not in names:
                        image_hashes.append("missing-part")
                        continue
                    image_hashes.append(hashlib.sha256(archive.read(target)).hexdigest())

                transforms: list[tuple[str, str, str, str]] = []
                for transform in slide_root.findall(".//a:xfrm", NS):
                    offset = transform.find("a:off", NS)
                    extent = transform.find("a:ext", NS)
                    transforms.append(
                        (
                            offset.attrib.get("x", "") if offset is not None else "",
                            offset.attrib.get("y", "") if offset is not None else "",
                            extent.attrib.get("cx", "") if extent is not None else "",
                            extent.attrib.get("cy", "") if extent is not None else "",
                        )
                    )

                self.slides.append(
                    {
                        "text": normalise_text(" ".join(texts)),
                        "editable_chars": len(normalise_text(" ".join(texts))),
                        "image_hashes": sorted(image_hashes),
                        "image_count": len(image_hashes),
                        "transforms": transforms,
                        "shape_counts": {
                            "shape": len(slide_root.findall(".//p:sp", NS)),
                            "picture": len(slide_root.findall(".//p:pic", NS)),
                            "graphic_frame": len(slide_root.findall(".//p:graphicFrame", NS)),
                        },
                    }
                )

    def page(self, one_based_slide: int) -> dict[str, Any]:
        if one_based_slide < 1 or one_based_slide > len(self.slides):
            raise IndexError(one_based_slide)
        return self.slides[one_based_slide - 1]

    def signature(self, one_based_slide: int) -> str:
        page = dict(self.page(one_based_slide))
        page["text"] = normalise_text(page["text"], ignore_copy_number=True)
        page.pop("editable_chars", None)
        raw = json.dumps(page, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()


class Audit:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.checks: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def checked(self, message: str) -> None:
        self.checks.append(message)


def validate_guided(deck: PptxDeck, manifest: dict[str, Any], audit: Audit) -> list[str]:
    width, height = deck.slide_size
    expected_width, expected_height = A4_LANDSCAPE_EMU
    if abs(width - expected_width) > SIZE_TOLERANCE_EMU or abs(height - expected_height) > SIZE_TOLERANCE_EMU:
        audit.error(
            "Guided deck is not exact A4 landscape: "
            f"found {width}x{height} EMU; expected {expected_width}x{expected_height} EMU"
        )
    else:
        audit.checked("Guided deck uses A4 landscape geometry")

    groups = manifest.get("guided_reading", {}).get("groups")
    if not isinstance(groups, list) or len(groups) != 5:
        audit.error("Manifest must contain exactly five Guided Reading groups")
        return []

    expected_next_slide = 1
    canonical_passages: list[str] = []

    for index, (entry, expected) in enumerate(zip(groups, EXPECTED_GROUPS), start=1):
        group, day, profile, visual_support = expected
        prefix = f"Group {index} ({group})"
        if entry.get("group") != group:
            audit.error(f"{prefix}: expected group name {group!r}")
        if entry.get("day") != day:
            audit.error(f"{prefix}: expected day {day!r}")
        if str(entry.get("profile", "")).lower() != profile.lower():
            audit.error(f"{prefix}: expected assessed profile {profile!r}")
        if str(entry.get("visual_support", "")).lower() != visual_support.lower():
            audit.error(f"{prefix}: expected visual support {visual_support!r}")

        teacher_slide = entry.get("teacher_slide")
        if not isinstance(teacher_slide, int):
            audit.error(f"{prefix}: teacher_slide must be an integer")
            continue
        if teacher_slide != expected_next_slide:
            audit.error(
                f"{prefix}: teacher slide must be {expected_next_slide} to preserve print order; found {teacher_slide}"
            )

        copies = entry.get("student_copies")
        if not isinstance(copies, list) or len(copies) != 7:
            audit.error(f"{prefix}: must declare exactly seven complete student copies")
            continue

        ranges: list[tuple[int, int]] = []
        for copy_number, item in enumerate(copies, start=1):
            if (
                not isinstance(item, list)
                or len(item) != 2
                or not all(isinstance(value, int) for value in item)
            ):
                audit.error(f"{prefix}: copy {copy_number} must be an inclusive [start, end] range")
                continue
            start, end = item
            if start > end:
                audit.error(f"{prefix}: copy {copy_number} has a reversed range")
            ranges.append((start, end))

        if len(ranges) != 7:
            continue
        page_counts = [end - start + 1 for start, end in ranges]
        if min(page_counts) < 1 or len(set(page_counts)) != 1:
            audit.error(f"{prefix}: all seven copies must have the same positive page count")
            continue

        cursor = teacher_slide + 1
        for copy_number, (start, end) in enumerate(ranges, start=1):
            if start != cursor:
                audit.error(
                    f"{prefix}: copy {copy_number} must start at slide {cursor}; found {start}"
                )
            cursor = end + 1
        expected_next_slide = cursor

        if teacher_slide > len(deck.slides) or any(end > len(deck.slides) for _, end in ranges):
            audit.error(f"{prefix}: declared slide range exceeds the Guided Reading deck")
            continue

        pages_per_copy = page_counts[0]
        canonical_start, _ = ranges[0]
        canonical_signatures = [
            deck.signature(canonical_start + offset) for offset in range(pages_per_copy)
        ]
        for copy_number, (start, _) in enumerate(ranges[1:], start=2):
            for offset, expected_signature in enumerate(canonical_signatures):
                if deck.signature(start + offset) != expected_signature:
                    audit.error(
                        f"{prefix}: student copy {copy_number}, page {offset + 1} does not match copy 1"
                    )

        min_chars = int(entry.get("min_editable_chars_per_student_page", 80))
        for copy_number, (start, end) in enumerate(ranges, start=1):
            for slide_number in range(start, end + 1):
                if deck.page(slide_number)["editable_chars"] < min_chars:
                    audit.error(
                        f"{prefix}: copy {copy_number} slide {slide_number} has fewer than "
                        f"{min_chars} editable text characters"
                    )

        canonical_text = " ".join(
            deck.page(canonical_start + offset)["text"] for offset in range(pages_per_copy)
        )
        canonical_passages.append(passage_text(canonical_text))

        exceptions = entry.get("epsilon_visual_exceptions", [])
        if not isinstance(exceptions, list):
            audit.error(f"{prefix}: epsilon_visual_exceptions must be a list")
            exceptions = []
        if group != "Epsilon" and exceptions:
            audit.error(f"{prefix}: Epsilon visual exceptions must be empty for Alpha-Delta")
        if group == "Epsilon":
            allowed_pages: set[int] = set()
            for exception in exceptions:
                if not isinstance(exception, dict):
                    audit.error("Epsilon visual exception must be an object")
                    continue
                page_number = exception.get("page")
                if not isinstance(page_number, int) or not 1 <= page_number <= pages_per_copy:
                    audit.error("Epsilon visual exception page is outside the student reading")
                    continue
                if exception.get("kind") != "scientific_or_technical_diagram":
                    audit.error("Epsilon visual exception kind must be scientific_or_technical_diagram")
                if not str(exception.get("purpose", "")).strip():
                    audit.error("Epsilon visual exception requires a purpose")
                if not str(exception.get("source", "")).strip():
                    audit.error("Epsilon visual exception requires a source")
                allowed_pages.add(page_number)

            for copy_number, (start, _) in enumerate(ranges, start=1):
                for offset in range(pages_per_copy):
                    picture_count = deck.page(start + offset)["image_count"]
                    if picture_count and offset + 1 not in allowed_pages:
                        audit.error(
                            f"Epsilon copy {copy_number}, page {offset + 1} contains "
                            f"{picture_count} undeclared embedded image(s)"
                        )

    if expected_next_slide - 1 != len(deck.slides):
        audit.error(
            "Guided deck contains unrecorded or missing slides: manifest covers "
            f"1-{expected_next_slide - 1}, deck contains {len(deck.slides)}"
        )
    else:
        audit.checked("Guided deck slide coverage and print order are complete")

    if len(canonical_passages) == 5:
        for left in range(5):
            for right in range(left + 1, 5):
                a_text = canonical_passages[left]
                b_text = canonical_passages[right]
                if min(len(a_text), len(b_text)) < 150:
                    continue
                ratio = SequenceMatcher(None, a_text, b_text).ratio()
                left_name = EXPECTED_GROUPS[left][0]
                right_name = EXPECTED_GROUPS[right][0]
                if ratio >= 0.985:
                    audit.error(
                        f"{left_name}/{right_name} student passages appear duplicated "
                        f"(similarity {ratio:.3f})"
                    )
                elif ratio >= 0.90:
                    audit.warn(
                        f"Review {left_name}/{right_name} differentiation closely "
                        f"(similarity {ratio:.3f})"
                    )
        audit.checked("Compared canonical Alpha-Epsilon passage text for likely duplication")

    return canonical_passages


def word_shingles(text: str, size: int = 8) -> set[tuple[str, ...]]:
    words = passage_text(text).split()
    return {tuple(words[index : index + size]) for index in range(len(words) - size + 1)}


def validate_shared(
    deck: PptxDeck,
    manifest: dict[str, Any],
    guided_passages: list[str],
    audit: Audit,
) -> None:
    shared = manifest.get("shared_reading")
    if not isinstance(shared, dict):
        audit.error("Manifest is missing shared_reading")
        return

    lead_slides = shared.get("lead_slides", [])
    pairs = shared.get("pairs", [])
    if not isinstance(lead_slides, list) or not all(isinstance(value, int) for value in lead_slides):
        audit.error("shared_reading.lead_slides must be a list of slide numbers")
        return
    if not isinstance(pairs, list) or not pairs:
        audit.error("Shared Reading must declare at least one question/answer pair")
        return

    coverage = list(lead_slides)
    expected_question = len(lead_slides) + 1
    for pair_number, pair in enumerate(pairs, start=1):
        if not isinstance(pair, dict):
            audit.error(f"Shared pair {pair_number} must be an object")
            continue
        question_slide = pair.get("question_slide")
        answer_slide = pair.get("answer_slide")
        if question_slide != expected_question or answer_slide != expected_question + 1:
            audit.error(
                f"Shared pair {pair_number} must be slides {expected_question}/{expected_question + 1}; "
                f"found {question_slide}/{answer_slide}"
            )
        if isinstance(question_slide, int) and isinstance(answer_slide, int):
            coverage.extend([question_slide, answer_slide])
            if 1 <= question_slide <= len(deck.slides):
                question_marks = deck.page(question_slide)["text"].count("?")
                if question_marks != 1:
                    audit.warn(
                        f"Shared question slide {question_slide} contains {question_marks} question marks; "
                        "verify that it asks exactly one question"
                    )
        expected_question += 2

    if coverage != list(range(1, len(deck.slides) + 1)):
        audit.error("Shared Reading manifest does not cover every slide in strict order")
    else:
        audit.checked("Shared Reading slides follow the declared question/answer sequence")

    shared_text = " ".join(page["text"] for page in deck.slides)
    shared_shingles = word_shingles(shared_text)
    if not shared_shingles:
        audit.error("Shared Reading deck contains too little editable text to audit")
        return
    for index, guided_text in enumerate(guided_passages):
        guided_shingles = word_shingles(guided_text)
        if not guided_shingles:
            continue
        overlap = len(shared_shingles & guided_shingles) / min(len(shared_shingles), len(guided_shingles))
        group = EXPECTED_GROUPS[index][0]
        if overlap >= 0.65:
            audit.error(
                f"Shared Reading and {group} appear to reuse a passage "
                f"(8-word shingle overlap {overlap:.2%})"
            )
        elif overlap >= 0.35:
            audit.warn(
                f"Review Shared Reading/{group} text independence "
                f"(8-word shingle overlap {overlap:.2%})"
            )
    audit.checked("Compared Shared Reading and Guided Reading for likely passage reuse")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--guided-deck", type=Path, required=True)
    parser.add_argument("--shared-deck", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    audit = Audit()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if manifest.get("schema_version") != "1.0":
            audit.error("Manifest schema_version must be 1.0")

        guided_deck = PptxDeck(args.guided_deck)
        guided_passages = validate_guided(guided_deck, manifest, audit)

        if args.shared_deck:
            shared_deck = PptxDeck(args.shared_deck)
            validate_shared(shared_deck, manifest, guided_passages, audit)
        else:
            audit.warn("Shared Reading deck was not supplied; cross-component checks were skipped")
    except (OSError, ValueError, KeyError, json.JSONDecodeError, zipfile.BadZipFile, ET.ParseError) as exc:
        audit.error(str(exc))

    report = {
        "status": "PASS" if not audit.errors else "FAIL",
        "errors": audit.errors,
        "warnings": audit.warnings,
        "checks": audit.checks,
        "manual_gates": [
            "Render and inspect every slide at full size",
            "Confirm teacher/student passage, question, answer, and evidence parity",
            "Confirm factual, cultural, Health-safety, and source integrity",
            "Confirm genuine Alpha-Epsilon differentiation and visual usefulness",
            "Confirm print preview yields one teacher sheet and seven complete student sets per group",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
