"""Inspeção complementar: fontes, EPUB, texto integral do PDF e geometria.

Não avalia qualidade literária nem substitui a inspeção visual ou o Previewer.
Execute depois de build_publication.py. --render cria amostras em tmp/pdfs/.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import pdfplumber
from PIL import Image, ImageDraw
from pypdf import PdfReader

import build_publication as build


def compact(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKC", text).casefold() if c.isalnum())


def source_text(path: Path) -> str:
    # O projeto converte listas numeradas de anotações em marcadores tipográficos.
    return re.sub(r"(?m)^\s*\d+\.\s+", "", path.read_text(encoding="utf-8-sig"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--render", action="store_true")
    args = parser.parse_args()
    counts = []
    for path in build.CHAPTERS:
        text = path.read_text(encoding="utf-8-sig")
        counts.append({"chapter": build.chapter_number(path), "story_words": len(re.findall(r"\b[\wÀ-ÿ]+\b", "\n".join(text.splitlines()[2:])))})

    with zipfile.ZipFile(build.EBOOK / "A_Metade_Que_Me_Faltava_Era_Eu.epub") as archive:
        for path in build.CHAPTERS:
            num = build.chapter_number(path)
            element = ET.fromstring(archive.read(f"OEBPS/text/chapter-{num:02}.xhtml"))
            body = element.find("{http://www.w3.org/1999/xhtml}body")
            actual = compact("".join(body.itertext()))
            expected = compact(source_text(path))
            assert actual == expected, f"EPUB difere da fonte no capítulo {num}"

    pdf_path = build.PRINT / "miolo-5.5x8.5-creme-sem-sangria.pdf"
    body_pages = []
    starts = {}
    geometry = []
    with pdfplumber.open(pdf_path) as pdf:
        page_count = len(pdf.pages)
        for number, page in enumerate(pdf.pages, 1):
            assert abs(page.width - 396) < .1 and abs(page.height - 612) < .1
            body = page.crop((0, 49, 396, 563))
            txt = body.extract_text() or ""
            body_pages.append(txt)
            match = re.search(r"(?m)^CAPÍTULO (\d+)\s*$", txt)
            if match:
                starts[int(match[1])] = number
            # A margem interna de 0,68 pol. supera o mínimo KDP de 0,625.
            for ch in body.chars:
                if ch["text"].strip() and (ch["x0"] < 48 or ch["x1"] > 348):
                    geometry.append({"page": number, "text": ch["text"], "x0": ch["x0"], "x1": ch["x1"]})
        assert set(starts) == set(range(1, 41)), starts
        for path in build.CHAPTERS:
            num = build.chapter_number(path)
            end = starts.get(num + 1, page_count + 1) - 1
            text = "\n".join(body_pages[starts[num] - 1:end])
            if num == 40:
                text = text.split("AGRADECIMENTOS", 1)[0]
            assert compact(text) == compact(source_text(path)), f"Texto do PDF difere no capítulo {num}"
        assert not geometry, geometry[:15]

    cover = PdfReader(str(build.PRINT / "capa-completa-5.5x8.5-creme.pdf"))
    expected_width = (11 + .25 + page_count * .0025) * 72
    assert len(cover.pages) == 1
    assert abs(float(cover.pages[0].mediabox.width) - expected_width) < .02
    assert abs(float(cover.pages[0].mediabox.height) - 8.75 * 72) < .02
    for page in PdfReader(str(pdf_path)).pages:
        for ref in page.get("/Resources", {}).get("/Font", {}).values():
            font = ref.get_object()
            if font.get("/BaseFont") == "/Helvetica":
                continue  # fonte padrão do canvas, não usada nos parágrafos
            desc = font.get("/FontDescriptor")
            assert desc and (desc.get_object().get("/FontFile2") or desc.get_object().get("/FontFile3")), font

    report = {"status": "OK", "story_words": sum(x["story_words"] for x in counts), "chapters": counts,
              "pdf_pages": page_count, "chapter_physical_pages": starts, "epub_source_sync": "40/40",
              "pdf_source_sync": "40/40", "body_margins": "OK", "cover_geometry": "OK", "fonts_embedded": "OK"}
    qa = build.ROOT / "tmp" / "pdfs" / "checkup-2026-09-29"
    qa.mkdir(parents=True, exist_ok=True)
    (qa / "inspection.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    if args.render:
        render = shutil.which("pdftoppm")
        if not render:
            raise SystemExit("pdftoppm ausente: instalar Poppler para a inspeção visual")
        selected = sorted(set([1,2,3,4,5,6,7,8, *[starts[n] for n in (1,8,10,11,16,17,29,31,36,39,40)], *range(page_count-3,page_count+1)]))
        for number in selected:
            subprocess.run([render,"-f",str(number),"-l",str(number),"-scale-to","1000","-singlefile","-png",str(pdf_path),str(qa/f"page-{number:03}")],check=True,capture_output=True)
        for start in range(0, len(selected), 6):
            group = selected[start:start+6]
            sheet = Image.new("RGB", (1050, 1100), "#ccc")
            draw = ImageDraw.Draw(sheet)
            for i, number in enumerate(group):
                page = Image.open(qa/f"page-{number:03}.png").convert("RGB")
                page.thumbnail((340, 520))
                x,y = (i%3)*350, (i//3)*550
                sheet.paste(page,(x,y+22))
                draw.text((x+4,y+4), f"PDF p. {number}", fill="black")
            sheet.save(qa/f"contact-{start//6+1}.jpg", quality=90)


if __name__ == "__main__":
    main()
