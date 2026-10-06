"""Validação reproduzível dos arquivos do livro e do pacote KDP."""

from __future__ import annotations

import hashlib
import json
import re
import struct
import sys
import zipfile
from pathlib import Path

from pypdf import PdfReader


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
    unsupported_glyphs = sorted({f"U+{ord(char):04X}" for char in combined if ord(char) > 0xFFFF})
    if unsupported_glyphs:
        fail(f"Caracteres sem suporte garantido no miolo impresso: {unsupported_glyphs}")
    leftovers = [token for token in FORBIDDEN_TEXT if token.casefold() in combined.casefold()]
    if leftovers:
        fail(f"Resíduos linguísticos encontrados: {leftovers}")
    editorial_regressions = {
        3: ("Ricardo tinha dito na cozinha", "uma esposa de onze anos"),
        6: ("mensageiro", "invisível sob a marquise"),
        8: ("nunca tinha visto. Ferro.", "seu filho esquece o aniversário"),
        9: ("tendo que acordar o pai", "Eles mereciam saber direto da gente", "ouvir o carro ir embora"),
        10: ("E Fi ficaram", "sobressaltada", "por sentir sozinha", "A gente ainda dá tempo", "Léo hesitou. — Você tá mais leve", "Camila sempre tinha querido silêncio"),
        11: ("caneta em riste", "Mais uma ruptura", "Léo tentando acordar o pai"),
        12: ("Não apagaram as parcelas da escola", "Abril estava no dia 8"),
        13: ("via jornal", "amava pequeno"),
        15: ("(recém-cortado)", "Vira-se", "ia atrás quinze minutos", "Segunda, quarta e domingo:"),
        16: ("primeira visita oficial", "Um Sábado Só Minha"),
        17: ("Quatorze anos depois", "não conseguiu lembrar a última vez que tinha feito algo só para ela"),
        18: ("Porque era terça. Crianças com o pai",),
        21: ("se eles vão voltar", "Fechou diário", "Não felicidade. Mas aceitação"),
        25: ("no apart-hotel de Ricardo",),
        27: ("Isso era uma informação nova e valiosa",),
        29: ("Ela contou que tinha voltado a pintar. Daniel perguntou", "apenas para ela (melhores amigos)", "pedaço que o casamento tinha ficado"),
        30: ("Encontro três.", "Encontro quatro.", "Encontro cinco."),
        31: ("onze anos de Dia das Mães",),
        32: ("Onze anos de férias",),
        33: ("— Eu também. Mas vai dar certo.",),
        34: ("Fez os dois devolverem o pegador",),
        36: ("Onze anos com o Ricardo",),
        38: ("malas na calçada", "gritando que ela tinha estragado tudo", "Ricardo não estava no celular. Estava filmando"),
        39: ("Camila encontrou seu diário antigo", "No dia seguinte, Camila encontrou Daniel", "Hoje ele esqueceu o aniversário do Léo"),
        40: ("Era o Ato I", "uma novidade recente que todos adoravam"),
    }
    for chapter_number, tokens in editorial_regressions.items():
        for token in tokens:
            if token.casefold() in texts[chapter_number - 1].casefold():
                fail(f"Regressão editorial no capítulo {chapter_number}: {token}")
    if re.search(r"(?<!Um )Dia de cada vez", texts[9], re.I):
        fail("Expressão incompleta no capítulo 10: 'Dia de cada vez'")
    if "Tipo o quê? eu" in combined:
        fail("Letra minúscula indevida após interrogação")

    if any("Daniel" in text for text in texts[:26]):
        fail("Daniel aparece antes do capítulo 27")

    # Âncoras editoriais: detectam regressões conhecidas, não julgam naturalidade.
    if "quatorze anos: três de namoro e onze de casamento" not in texts[0]:
        fail("Abertura deve distinguir 14 anos juntos de 11 anos de casamento")
    if re.search(r"(?:quatorze|catorze|14) anos de casamento", combined, re.I):
        fail("Duração da relação confundida com duração do casamento")
    romance_steps = ("O primeiro beijo foi curto", "no fim de abril", "— Então estamos namorando?")
    positions = [texts[29].find(marker) for marker in romance_steps]
    if min(positions) < 0 or positions != sorted(positions):
        fail("Capítulo 30 sem progressão de beijo, passagem de tempo e decisão de namorar")
    if "— É, filho. A gente está namorando." not in texts[31]:
        fail("Camila não responde claramente a Léo sobre o namoro no capítulo 32")
    if "um domingo de julho" not in texts[32] or "No começo de agosto" not in texts[32]:
        fail("Apresentação aos filhos e aproximação antes da viagem perderam a ponte temporal")

    continuity_markers = {
        1: "bombinha de asma do Léo",
        9: "Ricardo voltou para casa tarde",
        10: "A mudança definitiva aconteceu",
        11: "gerente comercial",
        12: "Era a primeira semana de abril",
        19: "Não tinha parado de trabalhar",
        27: "Camila Ferreira Santos",
        29: "sempre imaginei que seria pai",
        34: "ideia de uma casa cheia",
        37: "Daniel nunca tinha escondido",
    }
    for chapter_number, marker in continuity_markers.items():
        if marker.casefold() not in texts[chapter_number - 1].casefold():
            fail(f"Marcador de continuidade ausente no capítulo {chapter_number}: {marker}")

    if "Camila Ferreira Santos" not in texts[28] or "*Camila Ferreira*" not in texts[28]:
        fail("Mudança de nome de Camila ausente no capítulo 29")
    if "Daniel e Mariana" not in texts[36] or "criado os filhos sozinha" not in texts[36]:
        fail("Família de Daniel divergente entre os capítulos 30 e 37")
    if "Voltar ao escritório depois da separação" in texts[18]:
        fail("O capítulo 19 sugere uma ausência do trabalho que não ocorreu")

    compiled = (ROOT / "manuscrito_completo.md").read_text(encoding="utf-8-sig")
    for chapter_number, chapter_text in enumerate(texts, 1):
        normalized = "\n".join(line.rstrip() for line in chapter_text.strip().splitlines())
        if normalized not in compiled:
            fail(f"Manuscrito consolidado desatualizado no capítulo {chapter_number}")

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
    for relative_path in re.findall(r"file:\s*'([^']+)'", reader):
        if not (ROOT / relative_path).is_file():
            fail(f"Fonte do leitor ausente: {relative_path}")
    if "00-PLANEJAMENTO/ULTIMA_PALAVRA.md" not in reader or 'class="front-cover"' not in reader:
        fail("Leitor sem capa de abertura ou convite final em tela própria")
    for source in ("ABERTURA_BIBLICA.md", "CONSAGRACAO_FINAL.md"):
        if f"00-PLANEJAMENTO/{source}" not in reader:
            fail(f"Página bíblica ausente do leitor: {source}")
    if reader.count("{ file: '") != 45:
        fail("Índice online deve ter abertura, página bíblica, 40 capítulos e três páginas finais")
    if "metade-leitor-progresso-v2" not in reader or "metade-leitor-progresso-v1" not in reader:
        fail("Novo índice do leitor não preserva o marcador da edição anterior")
    if "scroll-behavior: smooth" in reader or "behavior: 'instant'" not in reader or "loadSequence" not in reader:
        fail("Troca de capítulo pode manter a rolagem anterior ou sofrer corrida entre carregamentos")
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    if 'href="./ler.html?cap=1">Começar' in index or 'href="./ler.html?inicio=1"' not in index:
        fail("CTA de início não abre a capa e as páginas iniciais")
    if "params.get('inicio') === '1'" not in reader or "url.searchParams.delete('inicio')" not in reader:
        fail("Leitor não prioriza o início nem limpa o parâmetro de entrada")
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


def validate_pwa() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("start_url") != "./ler.html" or manifest.get("display") != "standalone":
        fail("PWA não abre diretamente no leitor instalado")
    icons = {item.get("sizes"): item.get("src") for item in manifest.get("icons", [])}
    for size in (192, 512):
        icon = icons.get(f"{size}x{size}")
        if not icon:
            fail(f"Ícone PWA {size}x{size} ausente no manifesto")
        data = (ROOT / icon.removeprefix("./")).read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", data[16:24]) != (size, size):
            fail(f"Ícone PWA {size}x{size} inválido")

    for page in ("index.html", "ler.html"):
        html = (ROOT / page).read_text(encoding="utf-8")
        if '<link rel="manifest" href="./manifest.json">' not in html or '<script src="./pwa.js" defer></script>' not in html:
            fail(f"Manifesto ou instalação PWA ausente em {page}")
    reader = (ROOT / "ler.html").read_text(encoding="utf-8")
    if "loadProgress()" not in reader or "fetch(CHAPTERS[i].file, { cache: 'no-store' })" not in reader:
        fail("Leitor não retoma progresso ou pode guardar capítulos offline")
    if "saved.c === chapterIndex" not in reader or "window.addEventListener('pagehide', saveProgress)" not in reader:
        fail("Leitor pode perder a posição ao recarregar ou fechar o app")

    worker = (ROOT / "sw.js").read_text(encoding="utf-8")
    match = re.search(r"const SHELL_FILES = \[(.*?)\];", worker, re.S)
    shell = set(re.findall(r"'([^']+)'", match.group(1))) if match else set()
    expected = {
        "./index.html", "./ler.html", "./manifest.json",
        "./assets/app-icon-180.png", "./assets/app-icon-192.png", "./assets/app-icon-512.png",
    }
    if shell != expected:
        fail("Cache PWA deve conter somente a estrutura do site e os ícones")


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
    story_words = sum(
        len(re.findall(r"\b[\wÀ-ÿ]+\b", "\n".join(path.read_text(encoding="utf-8-sig").splitlines()[2:])))
        for path in (ROOT / "03-MANUSCRITO").glob("CAP_*.md")
    )
    print_pages = len(PdfReader(str(PACKAGE / "impresso" / "miolo-5.5x8.5-creme-sem-sangria.pdf")).pages)
    if book.get("wordCount") != story_words or book.get("numberOfPages") != print_pages:
        fail("Métricas do Book no site diferem da história ou do PDF atual")
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
    public_descriptions = {
        "landing": index,
        "llms": llms,
        "Amazon": (PACKAGE / "metadados" / "descricao-amazon.txt").read_text(encoding="utf-8"),
    }
    for name, text in public_descriptions.items():
        if "quatorze" not in text.casefold() or "onze" not in text.casefold():
            fail(f"Descrição de {name} sem distinção entre relação e casamento")
        if "Há onze anos, ela organiza a casa, os filhos" in text:
            fail(f"Descrição de {name} atribui 11 anos à maternidade")
    numbered_themes = re.findall(r"(?m)^\d+\. ", llms)
    if len(numbered_themes) != len(THEMES):
        fail(f"llms.txt contém {len(numbered_themes)} temas numerados")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    site_modified = next(item for item in graph if item.get("@type") == "WebPage").get("dateModified")
    if not site_modified or sitemap.count(f"<lastmod>{site_modified}</lastmod>") != 2:
        fail("Datas do sitemap e da página divergem")

    beta_leftovers = [token for token in FORBIDDEN_TEXT if token.casefold() in beta.casefold()]
    if beta_leftovers or "Beatriz, do grupo" in beta or "Um Ano Depois: A Nova Paz" in beta:
        fail(f"Manuscrito beta desatualizado: {beta_leftovers}")
    if "Júlia e Teresa" not in beta:
        fail("Renomeação de Teresa ausente no manuscrito beta")
    if "\ufeff" in beta or re.search(r"<p>\s*# CAPÍTULO", beta):
        fail("Títulos com BOM ou Markdown cru no manuscrito beta")
    if "<h2>SOBRE O LIVRO</h2>" in beta:
        fail("Sinopse comercial indevida antes do capítulo 1 no manuscrito beta")
    if not (beta.index("Eclesiastes 3:1") < beta.index("CAPÍTULO 1") < beta.index("AGRADECIMENTOS") < beta.index("Salmos 90:17")):
        fail("Páginas bíblicas ou agradecimentos fora de ordem na leitura beta")
    if "A gota d'água não foi a febre." not in index:
        fail("Trecho do site não corresponde ao capítulo 7")


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
        front = archive.read("OEBPS/text/front.xhtml").decode("utf-8")
        opening_verse = archive.read("OEBPS/text/opening-verse.xhtml").decode("utf-8")
        back = archive.read("OEBPS/text/back.xhtml").decode("utf-8")
        final_note = archive.read("OEBPS/text/final.xhtml").decode("utf-8")
        consecration = archive.read("OEBPS/text/consecration.xhtml").decode("utf-8")
        nav = archive.read("OEBPS/nav.xhtml").decode("utf-8")
        if "SOBRE O LIVRO" in front or "Subtítulo:" in front:
            fail("Abertura do EPUB contém sinopse comercial ou rótulo de planejamento")
        for anchor in ("#dedicatoria", "#carta"):
            if anchor not in nav:
                fail(f"Entrada de índice ausente no EPUB: {anchor}")
        if "UMA ÚLTIMA PALAVRA" in back or "UMA ÚLTIMA PALAVRA" not in final_note or "text/final.xhtml" not in nav:
            fail("Convite final não está separado e navegável no EPUB")
        if "Eclesiastes 3:1" not in opening_verse or "Salmos 90:17" not in consecration or "text/consecration.xhtml" not in nav:
            fail("Páginas bíblicas ausentes ou fora do sumário do EPUB")
        spine = archive.read("OEBPS/package.opf").decode("utf-8")
        ordered = ('idref="front"', 'idref="opening-verse"', 'idref="chapter-01"', 'idref="chapter-40"', 'idref="back"', 'idref="final"', 'idref="consecration"')
        if [spine.index(token) for token in ordered] != sorted(spine.index(token) for token in ordered):
            fail("Ordem das páginas bíblicas e dos capítulos incorreta no EPUB")

    report_path = PACKAGE / "metadados" / "epubcheck-report.json"
    epub_path = PACKAGE / "ebook" / "A_Metade_Que_Me_Faltava_Era_Eu.epub"
    if report_path.stat().st_mtime_ns < epub_path.stat().st_mtime_ns:
        fail("EPUBCheck pendente: o relatório é anterior ao EPUB reconstruído")
    report = json.loads(report_path.read_text(encoding="utf-8-sig"))
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
        for path in PACKAGE.rglob("*"):
            if not path.is_file():
                continue
            member = "AMAZON_KDP/" + path.relative_to(PACKAGE).as_posix()
            if member not in archive.namelist() or archive.read(member) != path.read_bytes():
                fail(f"ZIP final desatualizado: {member}")


def main() -> int:
    chapter_words = validate_chapters()
    validate_site_links()
    validate_pwa()
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
                "regressoes_linguisticas_conhecidas": "OK (não substitui leitura editorial)",
                "dados_estruturados": "OK",
                "manuscrito_beta": "OK",
                "links_locais": "OK",
                "pwa_sem_livro_offline": "OK",
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
