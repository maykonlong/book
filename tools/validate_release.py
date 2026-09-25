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
ILLUSTRATED_CHAPTERS = {1, 8, 12, 17, 22, 27, 31, 34, 39, 40}
THEMES = (
    "Carga mental feminina",
    "Trabalho doméstico desigual",
    "Solidão no casamento",
    "Perda e reconstrução da identidade",
    "Maternidade real e culpa materna",
    "Divórcio e julgamento social",
    "Independência financeira",
    "Amor-próprio e limites",
    "Terapia e saúde emocional",
    "Amizade feminina e rede de apoio",
    "Dependência emocional e medo da solidão",
    "Reconstrução familiar e coparentalidade",
    "Autonomia para escolher o próprio futuro",
)
FORBIDDEN_TEXT = (
    "eventually",
    "Léo process.",
    "chamava m",
    "quebrado família",
    "segurou rostinho",
    "os snacks",
    "band-aid",
    "stalkeava",
    "Campeonato Brasileiro",
    "receita de antibiótico",
    "Bia dormia no berço",
    "gerente de projetos",
    "saiu de casa decidida",
    "assumiria as parcelas que faltavam",
    "feed do Instagram",
    "decanter",
    "happy hour",
    "performance",
    "hobby",
    "não era um status",
    "39,2ºC",
)


def fail(message: str) -> None:
    raise AssertionError(message)


def validate_chapters() -> int:
    chapters = sorted((ROOT / "03-MANUSCRITO").glob("CAP_*.md"))
    if len(chapters) != 40:
        fail(f"Esperados 40 capítulos; encontrados {len(chapters)}")
    numbers = [int(re.search(r"CAP_(\d{2})_", path.name).group(1)) for path in chapters]
    if numbers != list(range(1, 41)):
        fail(f"Numeração de capítulos inválida: {numbers}")

    texts = [path.read_text(encoding="utf-8").lstrip("\ufeff") for path in chapters]
    for chapter_number, text in enumerate(texts, 1):
        if not text.startswith(f"# CAPÍTULO {chapter_number}\n## "):
            fail(f"Cabeçalho inconsistente no capítulo {chapter_number}")
    word_counts = [len(re.findall(r"\b[\wÀ-ÿ]+\b", text, flags=re.UNICODE)) for text in texts]
    short = [(numbers[index], count) for index, count in enumerate(word_counts) if count < 900]
    if short:
        fail(f"Capítulos abaixo de 900 palavras: {short}")

    combined = "\n".join(texts)
    leftovers = [token for token in FORBIDDEN_TEXT if token.casefold() in combined.casefold()]
    if leftovers:
        fail(f"Resíduos linguísticos encontrados: {leftovers}")
    if "Tipo o quê? eu" in combined:
        fail("Letra minúscula indevida após interrogação")

    if any("Daniel" in text for text in texts[:26]):
        fail("Daniel aparece antes do capítulo 27")

    continuity_markers = {
        1: "bombinha de asma do Léo",
        9: "Ricardo voltou para casa tarde",
        10: "mudança definitiva de Ricardo",
        11: "gerente comercial",
        12: "Abril estava no dia 8",
        29: "sempre imaginei que seria pai",
        34: "ideia de uma casa cheia",
        37: "Daniel nunca tinha escondido",
    }
    for chapter_number, marker in continuity_markers.items():
        if marker.casefold() not in texts[chapter_number - 1].casefold():
            fail(f"Marcador de continuidade ausente no capítulo {chapter_number}: {marker}")

    repeated_sentences: dict[str, set[int]] = {}
    for chapter_number, text in enumerate(texts, 1):
        for sentence in re.split(r"(?<=[.!?])\s+", text):
            normalized = " ".join(re.findall(r"[\wÀ-ÿ]+", sentence.casefold()))
            if len(normalized.split()) >= 10:
                repeated_sentences.setdefault(normalized, set()).add(chapter_number)
    duplicates = {
        sentence: chapters
        for sentence, chapters in repeated_sentences.items()
        if len(chapters) > 1
    }
    if duplicates:
        sample = next(iter(duplicates.items()))
        fail(f"Frase longa repetida nos capítulos {sorted(sample[1])}: {sample[0]}")

    ending = texts[-1]
    for sentence in ("Estava solteira.", "Estava feliz.", "Estava inteira."):
        if sentence not in ending:
            fail(f"Fecho ausente no capítulo 40: {sentence}")

    arc_markers = {
        37: "ser pai",
        38: "mais um filho",
        39: "solteira por escolha",
    }
    for chapter_number, marker in arc_markers.items():
        if marker.casefold() not in texts[chapter_number - 1].casefold():
            fail(f"Preparação do desfecho ausente no capítulo {chapter_number}: {marker}")

    return sum(word_counts)


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

    reader = (ROOT / "ler.html").read_text(encoding="utf-8")
    art_refs = re.findall(r"art:\s*'(assets/illustrations-web/cap-(\d{2})-[^']+\.jpg)'", reader)
    illustrated = {int(number) for _, number in art_refs}
    if illustrated != ILLUSTRATED_CHAPTERS:
        fail(f"Artes do leitor divergentes: {sorted(illustrated)}")
    for relative_path, _ in art_refs:
        art_path = ROOT / relative_path
        if not art_path.is_file():
            fail(f"Arte web ausente: {relative_path}")
        if art_path.stat().st_size > 400_000:
            fail(f"Arte web acima de 400 KB: {relative_path}")


def validate_site_content() -> None:
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    beta = (ROOT / "05-PUBLICACAO" / "manuscrito_beta.html").read_text(encoding="utf-8")
    if index.count("<h1") != 1:
        fail("A página inicial deve ter exatamente um H1")
    if '<link rel="canonical" href="https://maykonlong.github.io/book/">' not in index:
        fail("URL canônica da página inicial ausente")

    description_match = re.search(r'<meta name="description" content="([^"]+)">', index)
    if not description_match or not 70 <= len(description_match.group(1)) <= 160:
        fail("Meta description ausente ou fora do intervalo de 70 a 160 caracteres")

    theme_section = re.search(r'<section class="section inside" id="temas">(.*?)</section>', index, re.S)
    if not theme_section:
        fail("Seção visível de temas ausente")
    visible_themes = len(re.findall(r'<li class="inside-card(?: inside-card--wide)?">', theme_section.group(1)))
    if visible_themes != len(THEMES):
        fail(f"Seção visual contém {visible_themes} temas em vez de {len(THEMES)}")

    json_match = re.search(r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>', index, re.S)
    if not json_match:
        fail("JSON-LD ausente")
    data = json.loads(json_match.group(1))
    graph = data.get("@graph", [])
    book = next(item for item in graph if item.get("@type") == "Book")
    item_list = next(item for item in graph if item.get("@type") == "ItemList")
    faq = next(item for item in graph if item.get("@type") == "FAQPage")

    about = tuple(item["name"] for item in book.get("about", []))
    listed = tuple(item["name"] for item in item_list.get("itemListElement", []))
    if about != THEMES or listed != THEMES or item_list.get("numberOfItems") != len(THEMES):
        fail("Os 13 temas divergem entre Book, ItemList e a lista oficial")
    questions = {item["name"] for item in faq.get("mainEntity", [])}
    if "Quais temas sobre a vida das mulheres aparecem no livro?" not in questions:
        fail("Pergunta AEO sobre os 13 temas ausente")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    numbered_themes = re.findall(r"(?m)^\d+\. ", llms)
    if len(numbered_themes) != len(THEMES):
        fail(f"llms.txt contém {len(numbered_themes)} temas numerados")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if sitemap.count("<lastmod>2026-09-25</lastmod>") != 2:
        fail("Datas do sitemap não foram atualizadas")

    beta_leftovers = [token for token in FORBIDDEN_TEXT if token.casefold() in beta.casefold()]
    if beta_leftovers or "Beatriz, do grupo" in beta or "Um Ano Depois: A Nova Paz" in beta:
        fail(f"Manuscrito beta desatualizado: {beta_leftovers}")
    if "Júlia e Teresa" not in beta:
        fail("Renomeação de Teresa ausente no manuscrito beta")


def validate_epub() -> dict[str, int]:
    epub = PACKAGE / "ebook" / "A_Metade_Que_Me_Faltava_Era_Eu.epub"
    with zipfile.ZipFile(epub) as archive:
        bad = archive.testzip()
        if bad:
            fail(f"EPUB corrompido em {bad}")
        chapter_files = [name for name in archive.namelist() if re.fullmatch(r"OEBPS/text/chapter-\d{2}\.xhtml", name)]
        if len(chapter_files) != 40:
            fail(f"EPUB contém {len(chapter_files)} capítulos em vez de 40")
        art_files = [name for name in archive.namelist() if re.fullmatch(r"OEBPS/images/chapter-\d{2}\.jpg", name)]
        art_numbers = {int(re.search(r"chapter-(\d{2})", name).group(1)) for name in art_files}
        if art_numbers != ILLUSTRATED_CHAPTERS:
            fail(f"Artes do EPUB divergentes: {sorted(art_numbers)}")

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
    chapter_words = validate_chapters()
    validate_site_links()
    validate_site_content()
    epubcheck = validate_epub()
    validate_package()
    bundle = ROOT / "PACOTE_PUBLICACAO" / "A_Metade_Que_Me_Faltava_Era_Eu_KDP.zip"
    print(
        json.dumps(
            {
                "status": "APROVADO",
                "capitulos": 40,
                "palavras_com_titulos": chapter_words,
                "ilustracoes": len(ILLUSTRATED_CHAPTERS),
                "temas_na_pagina": len(THEMES),
                "arco_final": "OK",
                "linguagem": "OK",
                "dados_estruturados": "OK",
                "manuscrito_beta": "OK",
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
    except (AssertionError, FileNotFoundError, KeyError, StopIteration, ValueError, zipfile.BadZipFile) as exc:
        print(f"REPROVADO: {exc}", file=sys.stderr)
        raise SystemExit(1)
