"""Validação reproduzível dos arquivos do livro e do pacote KDP."""

from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "PACOTE_PUBLICACAO" / "AMAZON_KDP"


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_chapters() -> None:
    chapters = sorted((ROOT / "03-MANUSCRITO").glob("CAP_*.md"))
    if len(chapters) != 40:
        fail(f"Esperados 40 capítulos; encontrados {len(chapters)}")
    numbers = [int(re.search(r"CAP_(\d{2})_", path.name).group(1)) for path in chapters]
    if numbers != list(range(1, 41)):
        fail(f"Numeração de capítulos inválida: {numbers}")


def validate_site_links() -> None:
    missing: set[str] = set()
    for html_file in (ROOT / "index.html", ROOT / "ler.html"):
        text = html_file.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:src|href)="([^"#?]+)', text):
            if "+" in ref or "{" in ref:
                continue
            if re.match(r"^(?:https?:|mailto:|data:)", ref):
                continue
            candidate = ROOT / ref.removeprefix("./")
            if not candidate.exists():
                missing.add(f"{html_file.name}: {ref}")
    if missing:
        fail("Referências locais ausentes: " + ", ".join(sorted(missing)))


def validate_epub() -> dict[str, int]:
    epub = PACKAGE / "ebook" / "A_Metade_Que_Me_Faltava_Era_Eu.epub"
    with zipfile.ZipFile(epub) as archive:
        bad = archive.testzip()
        if bad:
            fail(f"EPUB corrompido em {bad}")
        chapter_files = [name for name in archive.namelist() if re.fullmatch(r"OEBPS/text/chapter-\d{2}\.xhtml", name)]
        if len(chapter_files) != 40:
            fail(f"EPUB contém {len(chapter_files)} capítulos em vez de 40")

    report = json.loads((PACKAGE / "metadados" / "epubcheck-report.json").read_text(encoding="utf-8-sig"))
    checker = report["checker"]
    result = {key: int(checker[key]) for key in ("nFatal", "nError", "nWarning")}
    if any(result.values()):
        fail(f"EPUBCheck encontrou problemas: {result}")
    return result


def validate_package() -> None:
    required = [
        PACKAGE / "ebook" / "A_Metade_Que_Me_Faltava_Era_Eu.epub",
        PACKAGE / "ebook" / "capa-kindle-1600x2560-v2.jpg",
        PACKAGE / "impresso" / "miolo-5.5x8.5-creme-sem-sangria.pdf",
        PACKAGE / "impresso" / "capa-completa-5.5x8.5-creme.pdf",
        PACKAGE / "impresso" / "capa-completa-5.5x8.5-creme-300dpi-cmyk.jpg",
        PACKAGE / "LEIA-ME.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.is_file() or path.stat().st_size == 0]
    if missing:
        fail("Arquivos finais ausentes ou vazios: " + ", ".join(missing))

    checksums = PACKAGE / "SHA256SUMS.txt"
    for line in checksums.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        target = PACKAGE / relative
        actual = hashlib.sha256(target.read_bytes()).hexdigest()
        if actual != expected:
            fail(f"Checksum divergente: {relative}")

    bundle = ROOT / "PACOTE_PUBLICACAO" / "A_Metade_Que_Me_Faltava_Era_Eu_KDP.zip"
    with zipfile.ZipFile(bundle) as archive:
        bad = archive.testzip()
        if bad:
            fail(f"ZIP final corrompido em {bad}")


def main() -> int:
    validate_chapters()
    validate_site_links()
    epubcheck = validate_epub()
    validate_package()
    bundle = ROOT / "PACOTE_PUBLICACAO" / "A_Metade_Que_Me_Faltava_Era_Eu_KDP.zip"
    print(
        json.dumps(
            {
                "status": "APROVADO",
                "capitulos": 40,
                "links_locais": "OK",
                "epubcheck": epubcheck,
                "checksums": "OK",
                "zip_final": "OK",
                "zip_mb": round(bundle.stat().st_size / 1_048_576, 2),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, FileNotFoundError, KeyError, ValueError, zipfile.BadZipFile) as exc:
        print(f"REPROVADO: {exc}", file=sys.stderr)
        raise SystemExit(1)
