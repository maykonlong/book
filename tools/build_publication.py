from __future__ import annotations

import hashlib
import html
import io
import json
import re
import shutil
import textwrap
import uuid
import zipfile
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    Image as RLImage,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "PACOTE_PUBLICACAO" / "AMAZON_KDP"
EBOOK = OUT / "ebook"
PRINT = OUT / "impresso"
META = OUT / "metadados"
ART = OUT / "artes"
SOURCE = OUT / "fonte"

TITLE = "A Metade Que Me Faltava Era Eu"
SUBTITLE = "A jornada de uma mulher que cansou de ser a única a tentar"
AUTHOR = "Mariana Duarte"
LANG = "pt-BR"
BOOK_ID = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'https://maykonlong.github.io/book/')}"

TRIM_W = 5.5
TRIM_H = 8.5
CREAM_SPINE_PER_PAGE = 0.0025

CHAPTERS = sorted((ROOT / "03-MANUSCRITO").glob("CAP_*.md"))
ART_MAP = {
    1: "cap-01-rotina-invisivel.png",
    8: "cap-08-separacao.png",
    12: "cap-12-recomeco-financeiro.png",
    17: "cap-17-voltando-a-pintar.png",
    22: "cap-22-primeiro-natal.png",
    27: "cap-27-o-encontro.png",
    31: "cap-31-dia-das-maes.png",
    34: "cap-34-viagem-a-quatro.png",
    39: "cap-39-carta-para-mim.png",
    40: "cap-40-inteira.png",
}
ART_ALTS = {
    1: "Camila prepara a rotina da família antes do amanhecer.",
    8: "Camila observa Ricardo partir e sustenta a decisão de se separar.",
    12: "Camila organiza as contas ao lado dos bolos que começou a vender.",
    17: "Camila volta a pintar aquarelas depois de muitos anos.",
    22: "Camila e os filhos vivem um Natal simples, imperfeito e cheio de afeto.",
    27: "Camila e Daniel se conhecem diante de uma aquarela na exposição.",
    31: "Léo e Bia surpreendem Camila com um café da manhã no Dia das Mães.",
    34: "Camila, Daniel, Léo e Bia observam as estrelas na primeira viagem juntos.",
    39: "Camila escreve para a mulher que foi enquanto prepara sua série de aquarelas.",
    40: "Camila contempla a série Renascimento na galeria vazia.",
}

FONT_DIR = Path("C:/Windows/Fonts")
GEORGIA = FONT_DIR / "georgia.ttf"
GEORGIA_BOLD = FONT_DIR / "georgiab.ttf"
GEORGIA_ITALIC = FONT_DIR / "georgiai.ttf"
GEORGIA_BOLD_ITALIC = FONT_DIR / "georgiaz.ttf"


def ensure_dirs() -> None:
    for folder in (EBOOK, PRINT, META, ART, SOURCE):
        folder.mkdir(parents=True, exist_ok=True)


def chapter_number(path: Path) -> int:
    return int(re.search(r"CAP_(\d+)", path.name).group(1))


def clean_markdown(md: str) -> str:
    md = md.replace("\r\n", "\n")
    md = md.replace("\ufeff", "")
    md = re.sub(r"\[\^\d+\]", "", md)
    return md.strip()


def reading_front_matter(md: str, include_title: bool = True) -> str:
    """Remove a sinopse comercial from the reader-facing opening."""
    cleaned = clean_markdown(md)
    marker = "## DEDICATÓRIA"
    if marker not in cleaned:
        raise ValueError("Dedicatória ausente da abertura do livro")
    title_page = f"# {TITLE}\n\n*{SUBTITLE}*\n\n" if include_title else ""
    return title_page + marker + cleaned.split(marker, 1)[1]


def inline_markup(text: str) -> str:
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    return escaped


def markdown_blocks(md: str) -> list[tuple[str, str]]:
    lines = clean_markdown(md).splitlines()
    blocks: list[tuple[str, str]] = []
    para: list[str] = []

    def flush() -> None:
        nonlocal para
        if para:
            blocks.append(("p", " ".join(x.strip() for x in para)))
            para = []

    for raw in lines:
        line = raw.strip()
        if not line:
            flush()
            continue
        if line in {"---", "***"}:
            flush()
            blocks.append(("scene", ""))
        elif line.startswith("## "):
            flush()
            blocks.append(("h2", line[3:].strip()))
        elif line.startswith("# "):
            flush()
            blocks.append(("h1", line[2:].strip()))
        elif line.startswith("> "):
            flush()
            blocks.append(("quote", line[2:].strip()))
        elif re.match(r"^[-*]\s+", line):
            flush()
            blocks.append(("li", re.sub(r"^[-*]\s+", "", line)))
        elif re.match(r"^\d+\.\s+", line):
            flush()
            blocks.append(("li", re.sub(r"^\d+\.\s+", "", line)))
        else:
            para.append(line)
    flush()
    return blocks


def chapter_title(md: str, fallback: str) -> tuple[str, str]:
    h1 = re.search(r"^#\s+(.+)$", md, re.M)
    h2 = re.search(r"^##\s+(.+)$", md, re.M)
    return (h1.group(1).strip() if h1 else fallback, h2.group(1).strip() if h2 else fallback)


def crop_fill(im: Image.Image, size: tuple[int, int], focus_x: float = 0.5) -> Image.Image:
    target_w, target_h = size
    src_ratio = im.width / im.height
    target_ratio = target_w / target_h
    if src_ratio > target_ratio:
        new_w = int(im.height * target_ratio)
        left = int((im.width - new_w) * focus_x)
        left = max(0, min(left, im.width - new_w))
        im = im.crop((left, 0, left + new_w, im.height))
    else:
        new_h = int(im.width / target_ratio)
        top = max(0, (im.height - new_h) // 2)
        im = im.crop((0, top, im.width, top + new_h))
    return im.resize(size, Image.Resampling.LANCZOS)


def fit_font(text: str, font_path: Path, max_size: int, max_width: int, draw: ImageDraw.ImageDraw) -> ImageFont.FreeTypeFont:
    size = max_size
    while size > 20:
        font = ImageFont.truetype(str(font_path), size)
        if draw.textbbox((0, 0), text, font=font)[2] <= max_width:
            return font
        size -= 2
    return ImageFont.truetype(str(font_path), size)


def draw_centered(draw: ImageDraw.ImageDraw, xy_y: int, text: str, font: ImageFont.FreeTypeFont,
                  fill: tuple[int, ...], width: int, stroke_width: int = 0,
                  stroke_fill: tuple[int, ...] | None = None) -> None:
    box = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
    x = (width - (box[2] - box[0])) // 2
    draw.text((x, xy_y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


def build_front_cover() -> Path:
    src = Image.open(ROOT / "assets" / "capa-arte.png").convert("RGB")
    cover = crop_fill(src, (1600, 2560), focus_x=0.52)

    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 1600, 780), fill=(9, 28, 44, 170))
    od.rectangle((0, 2080, 1600, 2560), fill=(9, 28, 44, 185))
    overlay = overlay.filter(ImageFilter.GaussianBlur(26))
    cover = Image.alpha_composite(cover.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(cover)

    gold = (226, 185, 96, 255)
    cream = (255, 249, 237, 255)
    navy = (8, 24, 38, 255)
    title_font = ImageFont.truetype(str(GEORGIA_BOLD), 154)
    title_font_small = ImageFont.truetype(str(GEORGIA_BOLD), 132)
    sub_font = ImageFont.truetype(str(GEORGIA_ITALIC), 45)
    author_font = ImageFont.truetype(str(GEORGIA_BOLD), 62)
    draw_centered(draw, 126, "A METADE", title_font, cream, 1600, 2, navy)
    draw_centered(draw, 300, "QUE ME FALTAVA", title_font_small, cream, 1600, 2, navy)
    draw_centered(draw, 455, "ERA EU", title_font, gold, 1600, 2, navy)
    draw.line((430, 654, 1170, 654), fill=gold, width=3)
    sub_lines = ["A jornada de uma mulher que cansou", "de ser a única a tentar"]
    for idx, line in enumerate(sub_lines):
        draw_centered(draw, 686 + idx * 59, line, sub_font, cream, 1600, 1, navy)
    draw_centered(draw, 2300, AUTHOR.upper(), author_font, cream, 1600, 2, navy)

    path = ART / "capa-kindle-1600x2560-v2.jpg"
    cover.convert("RGB").save(path, "JPEG", quality=96, optimize=True, progressive=True, dpi=(300, 300))
    shutil.copy2(path, EBOOK / path.name)
    shutil.copy2(path, ROOT / "assets" / "capa-amazon-v2.jpg")
    return path


def optimize_art() -> dict[int, Path]:
    result: dict[int, Path] = {}
    for num, name in ART_MAP.items():
        src = ROOT / "assets" / "illustrations-v2" / name
        im = Image.open(src).convert("RGB")
        target = ART / name.replace(".png", ".jpg")
        im.save(target, "JPEG", quality=92, optimize=True, progressive=True, dpi=(300, 300))
        result[num] = target
    return result


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("Georgia", str(GEORGIA)))
    pdfmetrics.registerFont(TTFont("Georgia-Bold", str(GEORGIA_BOLD)))
    pdfmetrics.registerFont(TTFont("Georgia-Italic", str(GEORGIA_ITALIC)))
    pdfmetrics.registerFont(TTFont("Georgia-BoldItalic", str(GEORGIA_BOLD_ITALIC)))
    pdfmetrics.registerFontFamily(
        "Georgia", normal="Georgia", bold="Georgia-Bold", italic="Georgia-Italic", boldItalic="Georgia-BoldItalic"
    )


class BookDocTemplate(BaseDocTemplate):
    def __init__(self, filename: str, first_chapter_page: int = 7, **kwargs):
        super().__init__(filename, **kwargs)
        self.first_chapter_page = first_chapter_page
        self.chapter_pages: dict[int, int] = {}
        page_w, page_h = self.pagesize
        margin = 0.68 * inch
        frame = Frame(margin, 0.70 * inch, page_w - 2 * margin, page_h - 1.38 * inch,
                      leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="book")
        self.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=self.draw_page)])

    def draw_page(self, canvas, doc):
        page = canvas.getPageNumber()
        canvas.saveState()
        if page > self.first_chapter_page:
            canvas.setFont("Georgia", 7.4)
            canvas.setFillColor(colors.HexColor("#77716a"))
            header = TITLE if page % 2 == 0 else AUTHOR
            canvas.drawCentredString(self.pagesize[0] / 2, self.pagesize[1] - 0.40 * inch, header.upper())
            canvas.setStrokeColor(colors.HexColor("#d8d0c4"))
            canvas.setLineWidth(0.35)
            canvas.line(0.68 * inch, self.pagesize[1] - 0.49 * inch,
                        self.pagesize[0] - 0.68 * inch, self.pagesize[1] - 0.49 * inch)
            canvas.setFont("Georgia", 8.5)
            # The first chapter page is logical page 1, even though its folio is suppressed.
            canvas.drawCentredString(self.pagesize[0] / 2, 0.39 * inch, str(page - self.first_chapter_page + 1))
        canvas.restoreState()

    def afterFlowable(self, flowable):
        number = getattr(flowable, "_chapter_number", None)
        if number is not None:
            self.chapter_pages[number] = self.page


def make_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "body": ParagraphStyle("BookBody", parent=base["BodyText"], fontName="Georgia", fontSize=10.4,
                               leading=14.1, textColor=colors.HexColor("#211f1c"), alignment=TA_JUSTIFY,
                               firstLineIndent=15, spaceAfter=6, allowWidows=0, allowOrphans=0),
        "body_first": ParagraphStyle("BookBodyFirst", parent=base["BodyText"], fontName="Georgia", fontSize=10.4,
                                     leading=14.1, textColor=colors.HexColor("#211f1c"), alignment=TA_JUSTIFY,
                                     firstLineIndent=0, spaceAfter=6, allowWidows=0, allowOrphans=0),
        "chapter_no": ParagraphStyle("ChapterNo", fontName="Georgia-Bold", fontSize=9.2, leading=12,
                                     textColor=colors.HexColor("#a04130"), alignment=TA_CENTER,
                                     tracking=2, spaceAfter=9),
        "chapter_title": ParagraphStyle("ChapterTitle", fontName="Georgia-Bold", fontSize=21, leading=24,
                                        textColor=colors.HexColor("#13283b"), alignment=TA_CENTER, spaceAfter=14),
        "quote": ParagraphStyle("Quote", fontName="Georgia-Italic", fontSize=10.2, leading=14,
                                textColor=colors.HexColor("#514b44"), leftIndent=24, rightIndent=24,
                                alignment=TA_LEFT, spaceBefore=8, spaceAfter=10),
        "small": ParagraphStyle("Small", fontName="Georgia", fontSize=8.7, leading=12,
                                textColor=colors.HexColor("#514b44"), alignment=TA_CENTER),
        "center": ParagraphStyle("Center", fontName="Georgia", fontSize=10.4, leading=14,
                                 textColor=colors.HexColor("#211f1c"), alignment=TA_CENTER, spaceAfter=8),
        "h2": ParagraphStyle("H2", fontName="Georgia-Bold", fontSize=14, leading=18,
                             textColor=colors.HexColor("#13283b"), alignment=TA_CENTER,
                             spaceBefore=18, spaceAfter=12),
        "list": ParagraphStyle("List", fontName="Georgia", fontSize=10.2, leading=13.8,
                               leftIndent=18, firstLineIndent=-10, spaceAfter=4),
        "toc_entry": ParagraphStyle("TocEntry", fontName="Georgia", fontSize=9.4, leading=12.5,
                                    textColor=colors.HexColor("#211f1c")),
        "toc_page": ParagraphStyle("TocPage", fontName="Georgia", fontSize=9.4, leading=12.5,
                                   textColor=colors.HexColor("#211f1c"), alignment=TA_CENTER),
    }


def scene_break(styles) -> list:
    return [Spacer(1, 7), Paragraph("• &nbsp; • &nbsp; •", styles["small"]), Spacer(1, 7)]


def body_flowables(md: str, styles: dict[str, ParagraphStyle], skip_headings: bool = True) -> list:
    out = []
    first = True
    for kind, text in markdown_blocks(md):
        if kind in {"h1", "h2"} and skip_headings:
            continue
        if kind == "scene":
            out.extend(scene_break(styles))
            first = True
        elif kind == "quote":
            out.append(Paragraph(inline_markup(text), styles["quote"]))
            first = False
        elif kind == "li":
            out.append(Paragraph("• " + inline_markup(text), styles["list"]))
            first = False
        elif kind == "h2":
            out.append(Paragraph(inline_markup(text), styles["h2"]))
            first = True
        elif kind == "h1":
            out.append(Paragraph(inline_markup(text), styles["chapter_title"]))
            first = True
        else:
            out.append(Paragraph(inline_markup(text), styles["body_first"] if first else styles["body"]))
            first = False
    return out


def render_interior(path: Path, art_paths: dict[int, Path], toc_pages: dict[int, int] | None = None) -> tuple[int, dict[int, int]]:
    register_fonts()
    styles = make_styles()
    first_chapter_page = 9 if toc_pages is not None else 7
    doc = BookDocTemplate(str(path), pagesize=(TRIM_W * inch, TRIM_H * inch),
                          title=TITLE, author=AUTHOR, subject=SUBTITLE,
                          creator="Edição independente de Mariana Duarte",
                          first_chapter_page=first_chapter_page)
    story = []

    story += [Spacer(1, 1.60 * inch), Paragraph(TITLE.upper(), styles["chapter_title"]), PageBreak()]
    story += [Spacer(1, 1.22 * inch), Paragraph(TITLE, styles["chapter_title"]),
              Spacer(1, 0.18 * inch), Paragraph(SUBTITLE, styles["quote"]),
              Spacer(1, 1.20 * inch), Paragraph(AUTHOR.upper(), styles["center"]), PageBreak()]
    copyright_text = (
        "© 2026 Mariana Duarte. Todos os direitos reservados.<br/><br/>"
        "Primeira edição independente — 2026.<br/><br/>"
        "Nenhuma parte desta obra pode ser reproduzida ou transmitida sem autorização prévia da autora, "
        "exceto em breves citações para resenhas.<br/><br/>"
        "Esta é uma obra de ficção. Personagens, diálogos e acontecimentos foram criados para a narrativa. "
        "O livro se inspira em vivências e sentimentos compartilhados ao longo de muitos anos, "
        "mas não reproduz a história, a identidade ou o atendimento de nenhuma pessoa em particular."
    )
    story += [Spacer(1, 2.25 * inch), Paragraph(copyright_text, styles["small"]), PageBreak()]
    story += [Spacer(1, 1.55 * inch), Paragraph("DEDICATÓRIA", styles["chapter_no"]),
              Paragraph("<em>Para toda mulher que já carregou o mundo sozinha — e que, um dia, decidiu se salvar.</em>", styles["quote"]),
              Paragraph("<em>Para as que ainda estão no meio do caminho, segurando as pontas com as unhas: você não está sozinha. E você vai conseguir.</em>", styles["quote"]), PageBreak()]
    story += [Spacer(1, 1.60 * inch),
              Paragraph("<em>“Eu passei tanto tempo procurando a metade que me faltava. Em outras pessoas, em casamentos, em validações. Mas ela sempre esteve aqui, dentro de mim. Esperando que eu me reencontrasse.”</em>", styles["quote"]), PageBreak()]

    if toc_pages is not None:
        for group in (range(1, 21), range(21, 41)):
            title = "SUMÁRIO" if group.start == 1 else "SUMÁRIO — CONTINUAÇÃO"
            story += [Spacer(1, 0.42 * inch), Paragraph(title, styles["chapter_title"]), Spacer(1, 0.13 * inch)]
            rows = []
            for number in group:
                chapter_path = CHAPTERS[number - 1]
                _, chapter_name = chapter_title(chapter_path.read_text(encoding="utf-8-sig"), f"Capítulo {number}")
                rows.append([
                    Paragraph(f"{number}. {inline_markup(chapter_name)}", styles["toc_entry"]),
                    Paragraph(str(toc_pages[number]), styles["toc_page"]),
                ])
            table = Table(rows, colWidths=[3.57 * inch, 0.57 * inch], hAlign="LEFT")
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (0, -1), 8),
                ("RIGHTPADDING", (1, 0), (1, -1), 0),
                ("LEFTPADDING", (1, 0), (1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story += [table, PageBreak()]

    letter = clean_markdown((ROOT / "00-PLANEJAMENTO" / "FRONT_MATTER.md").read_text(encoding="utf-8"))
    letter_match = re.search(r"## CARTA À LEITORA\s+(.*)$", letter, re.S)
    letter_md = letter_match.group(1).strip() if letter_match else ""
    story += [Paragraph("CARTA À LEITORA", styles["chapter_title"]), Spacer(1, 8)]
    story += body_flowables(letter_md, styles, skip_headings=True)
    story.append(PageBreak())

    for idx, ch_path in enumerate(CHAPTERS):
        num = chapter_number(ch_path)
        md = ch_path.read_text(encoding="utf-8")
        _, title = chapter_title(md, f"Capítulo {num}")
        story.append(Spacer(1, 0.30 * inch))
        chapter_heading = Paragraph(f"CAPÍTULO {num}", styles["chapter_no"])
        chapter_heading._chapter_number = num
        story.append(chapter_heading)
        story.append(Paragraph(inline_markup(title), styles["chapter_title"]))
        if num in art_paths:
            img = RLImage(str(art_paths[num]), width=4.14 * inch, height=2.76 * inch)
            story += [Spacer(1, 4), img, Spacer(1, 16)]
        story += body_flowables(md, styles, skip_headings=True)
        if idx < len(CHAPTERS) - 1:
            story.append(PageBreak())

    story.append(PageBreak())
    post = (ROOT / "00-PLANEJAMENTO" / "POS_TEXTUAIS.md").read_text(encoding="utf-8")
    story += body_flowables(post, styles, skip_headings=False)

    doc.build(story)
    pages = len(PdfReader(str(path)).pages)
    if pages % 2:
        # Append one blank page without rebuilding the already-consumed Platypus story.
        reader = PdfReader(str(path))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_blank_page(width=TRIM_W * inch, height=TRIM_H * inch)
        temp = path.with_suffix(".tmp.pdf")
        with temp.open("wb") as handle:
            writer.write(handle)
        temp.replace(path)
        pages = len(PdfReader(str(path)).pages)
    return pages, doc.chapter_pages


def build_interior(art_paths: dict[int, Path]) -> tuple[Path, int]:
    path = PRINT / "miolo-5.5x8.5-creme-sem-sangria.pdf"
    preliminary = PRINT / "miolo-preliminar-temporario.pdf"
    _, physical_pages = render_interior(preliminary, art_paths)
    if set(physical_pages) != set(range(1, 41)):
        raise ValueError("Não foi possível localizar todos os capítulos no miolo preliminar")
    # A abertura do capítulo 1 é a página lógica 1; o sumário acrescenta duas páginas antes dela.
    toc_pages = {number: physical_pages[number] - 6 for number in range(1, 41)}
    pages, final_physical_pages = render_interior(path, art_paths, toc_pages)
    if any(final_physical_pages[number] - 8 != toc_pages[number] for number in range(1, 41)):
        raise ValueError("As páginas do sumário impresso não correspondem ao miolo final")
    preliminary.unlink()
    return path, pages


def paragraphs_to_xhtml(md: str) -> str:
    output: list[str] = []
    in_list = False
    for kind, text in markdown_blocks(md):
        if kind != "li" and in_list:
            output.append("</ul>")
            in_list = False
        if kind == "p":
            output.append(f"<p>{inline_markup(text)}</p>")
        elif kind == "quote":
            output.append(f"<blockquote>{inline_markup(text)}</blockquote>")
        elif kind == "scene":
            output.append('<div class="scene" aria-hidden="true">• • •</div>')
        elif kind == "h1":
            output.append(f"<h1>{inline_markup(text)}</h1>")
        elif kind == "h2":
            output.append(f"<h2>{inline_markup(text)}</h2>")
        elif kind == "li":
            if not in_list:
                output.append("<ul>")
                in_list = True
            output.append(f"<li>{inline_markup(text)}</li>")
    if in_list:
        output.append("</ul>")
    return "\n".join(output)


def xhtml_page(title: str, body: str, body_class: str = "chapter", css_href: str = "../styles/book.css") -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="pt-BR" xml:lang="pt-BR">
<head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="{css_href}"/></head>
<body class="{body_class}">{body}</body></html>'''


def build_epub(front_cover: Path, art_paths: dict[int, Path]) -> Path:
    stage = OUT / ".epub-stage"
    if stage.exists():
        shutil.rmtree(stage)
    (stage / "META-INF").mkdir(parents=True)
    for d in ("text", "styles", "images"):
        (stage / "OEBPS" / d).mkdir(parents=True)
    (stage / "mimetype").write_text("application/epub+zip", encoding="ascii")
    (stage / "META-INF" / "container.xml").write_text(
        '<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>',
        encoding="utf-8",
    )
    css = '''body{font-family:serif;line-height:1.55;margin:5%;color:#211f1c}h1,h2{text-align:center;color:#13283b;line-height:1.18}h1{margin-top:18%;font-size:1.15em;letter-spacing:.08em}h2{font-size:1.8em;margin:.5em 0 1.2em}p{text-align:justify;text-indent:1.2em;margin:0 0 .35em}h2+p,.chapter-art+p,.scene+p{ text-indent:0}.scene{text-align:center;letter-spacing:.8em;color:#8e4736;margin:1.6em 0}blockquote{font-style:italic;margin:1.3em 10%;color:#514b44}.chapter-art{margin:1em 0 1.6em;text-align:center}.chapter-art img{max-width:100%;height:auto}.titlepage{text-align:center;margin-top:30%}.titlepage p{text-align:center;text-indent:0}.copyright p{text-indent:0;text-align:left;font-size:.9em}ul{margin:1em 0 1em 1.5em}li{margin:.3em 0}.cover{margin:0;padding:0;text-align:center}.cover img{width:100%;height:auto}'''
    (stage / "OEBPS" / "styles" / "book.css").write_text(css, encoding="utf-8")

    cover_name = "cover.jpg"
    shutil.copy2(front_cover, stage / "OEBPS" / "images" / cover_name)
    for num, path in art_paths.items():
        shutil.copy2(path, stage / "OEBPS" / "images" / f"chapter-{num:02d}.jpg")

    items = []
    spine = []
    nav_points = []
    cover_xhtml = xhtml_page(TITLE, '<div class="cover"><img src="../images/cover.jpg" alt="Capa do livro A Metade Que Me Faltava Era Eu"/></div>', "cover")
    (stage / "OEBPS" / "text" / "cover.xhtml").write_text(cover_xhtml, encoding="utf-8")
    items.append(('cover-page', 'text/cover.xhtml', 'application/xhtml+xml', ''))
    spine.append('cover-page')

    title_body = f'<section class="titlepage" epub:type="titlepage"><h1>{html.escape(TITLE)}</h1><p><em>{html.escape(SUBTITLE)}</em></p><p>{html.escape(AUTHOR)}</p></section>'
    (stage / "OEBPS" / "text" / "title.xhtml").write_text(xhtml_page(TITLE, title_body, "titlepage"), encoding="utf-8")
    items.append(('title-page', 'text/title.xhtml', 'application/xhtml+xml', ''))
    spine.append('title-page')

    front_md = reading_front_matter((ROOT / "00-PLANEJAMENTO" / "FRONT_MATTER.md").read_text(encoding="utf-8"), include_title=False)
    front_body = paragraphs_to_xhtml(front_md)
    for heading, anchor in (("DEDICATÓRIA", "dedicatoria"), ("EPÍGRAFE", "epigrafe"), ("CARTA À LEITORA", "carta")):
        front_body = front_body.replace(f"<h2>{heading}</h2>", f'<h2 id="{anchor}">{heading}</h2>')
    (stage / "OEBPS" / "text" / "front.xhtml").write_text(xhtml_page("Início", front_body, "frontmatter"), encoding="utf-8")
    items.append(('front', 'text/front.xhtml', 'application/xhtml+xml', ''))
    spine.append('front')
    nav_points.append(("Início", "text/front.xhtml"))
    nav_points.extend([
        ("Dedicatória", "text/front.xhtml#dedicatoria"),
        ("Epígrafe", "text/front.xhtml#epigrafe"),
        ("Carta à leitora", "text/front.xhtml#carta"),
    ])

    for ch_path in CHAPTERS:
        num = chapter_number(ch_path)
        md = ch_path.read_text(encoding="utf-8")
        _, title = chapter_title(md, f"Capítulo {num}")
        body = f'<h1>CAPÍTULO {num}</h1><h2>{html.escape(title)}</h2>'
        if num in art_paths:
            body += f'<figure class="chapter-art"><img src="../images/chapter-{num:02d}.jpg" alt="{html.escape(ART_ALTS[num])}"/></figure>'
        blocks = [(k, v) for k, v in markdown_blocks(md) if k not in {"h1", "h2"}]
        temp_md = "\n\n".join((f"> {v}" if k == "quote" else "---" if k == "scene" else f"- {v}" if k == "li" else v) for k, v in blocks)
        body += paragraphs_to_xhtml(temp_md)
        fname = f"chapter-{num:02d}.xhtml"
        (stage / "OEBPS" / "text" / fname).write_text(xhtml_page(f"Capítulo {num} — {title}", body), encoding="utf-8")
        items.append((f"chapter-{num:02d}", f"text/{fname}", "application/xhtml+xml", ""))
        spine.append(f"chapter-{num:02d}")
        nav_points.append((f"Capítulo {num} — {title}", f"text/{fname}"))

    post_md = (ROOT / "00-PLANEJAMENTO" / "POS_TEXTUAIS.md").read_text(encoding="utf-8")
    (stage / "OEBPS" / "text" / "back.xhtml").write_text(xhtml_page("Agradecimentos", paragraphs_to_xhtml(post_md), "backmatter"), encoding="utf-8")
    items.append(('back', 'text/back.xhtml', 'application/xhtml+xml', ''))
    spine.append('back')
    nav_points.append(("Agradecimentos e sobre a autora", "text/back.xhtml"))

    nav_links = "".join(f'<li><a href="{href}">{html.escape(label)}</a></li>' for label, href in nav_points)
    nav = xhtml_page("Sumário", f'<nav epub:type="toc" id="toc"><h1>Sumário</h1><ol>{nav_links}</ol></nav>', "nav", "styles/book.css")
    (stage / "OEBPS" / "nav.xhtml").write_text(nav, encoding="utf-8")

    ncx_points = "".join(
        f'<navPoint id="nav-{i}" playOrder="{i}"><navLabel><text>{html.escape(label)}</text></navLabel><content src="{href}"/></navPoint>'
        for i, (label, href) in enumerate(nav_points, 1)
    )
    ncx = f'''<?xml version="1.0" encoding="UTF-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="{BOOK_ID}"/></head><docTitle><text>{html.escape(TITLE)}</text></docTitle><navMap>{ncx_points}</navMap></ncx>'''
    (stage / "OEBPS" / "toc.ncx").write_text(ncx, encoding="utf-8")

    manifest = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
        '<item id="css" href="styles/book.css" media-type="text/css"/>',
        '<item id="cover-image" href="images/cover.jpg" media-type="image/jpeg" properties="cover-image"/>',
    ]
    manifest += [f'<item id="{i}" href="{href}" media-type="{media}"{(" properties=" + chr(34) + prop + chr(34)) if prop else ""}/>' for i, href, media, prop in items]
    manifest += [f'<item id="image-{n:02d}" href="images/chapter-{n:02d}.jpg" media-type="image/jpeg"/>' for n in art_paths]
    spine_xml = "".join(f'<itemref idref="{i}"/>' for i in spine)
    opf = f'''<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="pt-BR"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{BOOK_ID}</dc:identifier><dc:title>{html.escape(TITLE)}</dc:title><dc:creator>{html.escape(AUTHOR)}</dc:creator><dc:language>pt-BR</dc:language><dc:date>{date.today().isoformat()}</dc:date><dc:description>{html.escape(SUBTITLE)}</dc:description><meta property="dcterms:modified">{date.today().isoformat()}T00:00:00Z</meta></metadata><manifest>{''.join(manifest)}</manifest><spine toc="ncx">{spine_xml}</spine></package>'''
    (stage / "OEBPS" / "package.opf").write_text(opf, encoding="utf-8")

    out = EBOOK / "A_Metade_Que_Me_Faltava_Era_Eu.epub"
    with zipfile.ZipFile(out, "w") as zf:
        zf.write(stage / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(stage.rglob("*")):
            if path.is_file() and path.name != "mimetype":
                zf.write(path, path.relative_to(stage).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
    shutil.rmtree(stage)
    return out


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines, line = [], []
    for word in words:
        test = " ".join(line + [word])
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            line.append(word)
        else:
            if line:
                lines.append(" ".join(line))
            line = [word]
    if line:
        lines.append(" ".join(line))
    return lines


def build_print_cover(front_cover: Path, page_count: int) -> tuple[Path, Path, float]:
    spine = page_count * CREAM_SPINE_PER_PAGE
    full_w = TRIM_W * 2 + spine + 0.25
    full_h = TRIM_H + 0.25
    dpi = 300
    px_w, px_h = round(full_w * dpi), round(full_h * dpi)
    canvas = Image.new("RGB", (px_w, px_h), (17, 40, 58))

    # Back cover: muted watercolor texture based on the opening illustration.
    back_src = Image.open(ROOT / "assets" / "illustrations-v2" / ART_MAP[1]).convert("RGB")
    back = crop_fill(back_src, (round(5.625 * dpi), px_h), focus_x=0.08)
    back = ImageEnhance.Brightness(back).enhance(0.46)
    back = ImageEnhance.Color(back).enhance(0.68)
    canvas.paste(back, (0, 0))

    spine_x = round((TRIM_W + 0.125) * dpi)
    spine_w = max(1, round(spine * dpi))
    sd = ImageDraw.Draw(canvas, "RGBA")
    sd.rectangle((spine_x, 0, spine_x + spine_w, px_h), fill=(10, 31, 47, 245))

    front_x = spine_x + spine_w
    front_img = Image.open(front_cover).convert("RGB")
    front = crop_fill(front_img, (px_w - front_x, px_h), focus_x=0.5)
    canvas.paste(front, (front_x, 0))

    draw = ImageDraw.Draw(canvas, "RGBA")
    cream = (250, 242, 224, 255)
    gold = (226, 185, 96, 255)
    navy = (8, 24, 38, 235)

    # Back-cover reading panel.
    pad = round(0.48 * dpi)
    panel_x1 = pad
    panel_x2 = spine_x - pad
    panel_y1 = round(0.62 * dpi)
    panel_y2 = round(6.50 * dpi)
    draw.rounded_rectangle((panel_x1, panel_y1, panel_x2, panel_y2), radius=34, fill=(8, 24, 38, 224), outline=(226, 185, 96, 160), width=2)
    head_font = ImageFont.truetype(str(GEORGIA_BOLD), 58)
    body_font = ImageFont.truetype(str(GEORGIA), 31)
    italic_font = ImageFont.truetype(str(GEORGIA_ITALIC), 32)
    x = panel_x1 + 52
    y = panel_y1 + 52
    draw.text((x, y), "ELA NÃO QUERIA OUTRO AMOR.", font=head_font, fill=gold)
    y += 76
    draw.text((x, y), "QUERIA VOLTAR A EXISTIR.", font=head_font, fill=gold)
    y += 104
    blurb = (
        "Camila cuida da casa, dos filhos, do trabalho e da vida de todo mundo. Ricardo diz que ajuda — mas nunca vê o que precisa ser feito. Depois de onze anos de casamento, uma manhã comum mostra o que ela já não consegue negar: está sozinha, mesmo acompanhada."
    )
    for line in wrap_text(draw, blurb, body_font, panel_x2 - x - 48):
        draw.text((x, y), line, font=body_font, fill=cream)
        y += 45
    y += 28
    blurb2 = (
        "Entre a culpa, as contas e o medo de ferir os filhos, Camila começa a reconstruir a própria vida. E reencontra uma mulher que pintava, ria alto e sonhava sem pedir licença."
    )
    for line in wrap_text(draw, blurb2, body_font, panel_x2 - x - 48):
        draw.text((x, y), line, font=body_font, fill=cream)
        y += 45
    y += 30
    quote = "Um romance sobre carga mental, maternidade, recomeço e a coragem de escolher a si mesma."
    for line in wrap_text(draw, quote, italic_font, panel_x2 - x - 48):
        draw.text((x, y), line, font=italic_font, fill=gold)
        y += 47

    # Leave the standard lower-right back-cover area free for KDP's barcode.
    barcode_w, barcode_h = round(2.0 * dpi), round(1.2 * dpi)
    barcode_x2 = spine_x - round(0.35 * dpi)
    barcode_y2 = px_h - round(0.35 * dpi)
    draw.rounded_rectangle((barcode_x2 - barcode_w, barcode_y2 - barcode_h, barcode_x2, barcode_y2),
                           radius=10, fill=(250, 242, 224, 245))

    # Spine text, vertical in the final flat cover.
    spine_layer = Image.new("RGBA", (px_h, max(1, spine_w)), (0, 0, 0, 0))
    sp_draw = ImageDraw.Draw(spine_layer)
    spine_text = f"{TITLE.upper()}  •  {AUTHOR.upper()}"
    sp_font = fit_font(spine_text, GEORGIA_BOLD, min(80, max(18, spine_w - 30)), px_h - 300, sp_draw)
    bbox = sp_draw.textbbox((0, 0), spine_text, font=sp_font)
    sx = (px_h - (bbox[2] - bbox[0])) // 2
    sy = (spine_w - (bbox[3] - bbox[1])) // 2
    sp_draw.text((sx, sy), spine_text, font=sp_font, fill=cream)
    spine_rot = spine_layer.rotate(270, expand=True)
    canvas.paste(spine_rot, (spine_x, 0), spine_rot)

    cmyk = canvas.convert("CMYK")
    flat_jpg = PRINT / "capa-completa-5.5x8.5-creme-300dpi-cmyk.jpg"
    cmyk.save(flat_jpg, "JPEG", quality=95, dpi=(300, 300))

    pdf_path = PRINT / "capa-completa-5.5x8.5-creme.pdf"
    from reportlab.pdfgen import canvas as pdfcanvas
    pdf = pdfcanvas.Canvas(str(pdf_path), pagesize=(full_w * inch, full_h * inch), pageCompression=1)
    pdf.setTitle(f"Capa completa — {TITLE}")
    pdf.setAuthor(AUTHOR)
    pdf.drawImage(ImageReader(str(flat_jpg)), 0, 0, width=full_w * inch, height=full_h * inch, mask=None)
    pdf.showPage()
    pdf.save()

    preview = ART / "capa-completa-preview-v2.jpg"
    canvas.resize((min(2200, px_w), round(px_h * min(2200, px_w) / px_w)), Image.Resampling.LANCZOS).save(preview, "JPEG", quality=92)
    return pdf_path, preview, spine


def build_source_manuscript() -> Path:
    def read_clean(path: Path) -> str:
        raw = clean_markdown(path.read_text(encoding="utf-8-sig"))
        return "\n".join(line.rstrip() for line in raw.splitlines())

    pieces = [
        reading_front_matter((ROOT / "00-PLANEJAMENTO" / "FRONT_MATTER.md").read_text(encoding="utf-8-sig")),
        *[read_clean(p) for p in CHAPTERS],
        read_clean(ROOT / "00-PLANEJAMENTO" / "POS_TEXTUAIS.md"),
    ]
    text = "\n\n---\n\n".join(pieces) + "\n"
    path = SOURCE / "manuscrito_final.md"
    path.write_text(text, encoding="utf-8")
    (ROOT / "manuscrito_completo.md").write_text(text, encoding="utf-8")
    return path


def build_beta_html() -> Path:
    front = reading_front_matter((ROOT / "00-PLANEJAMENTO" / "FRONT_MATTER.md").read_text(encoding="utf-8-sig"))
    parts = [paragraphs_to_xhtml(front)]
    parts.extend(paragraphs_to_xhtml(path.read_text(encoding="utf-8-sig")) for path in CHAPTERS)
    parts.append(paragraphs_to_xhtml((ROOT / "00-PLANEJAMENTO" / "POS_TEXTUAIS.md").read_text(encoding="utf-8-sig")))
    body = '\n<div class="section-break" aria-hidden="true">• • •</div>\n'.join(parts)
    style = (
        "body{font-family:Georgia,'Times New Roman',serif;max-width:42em;margin:2em auto;padding:0 1.5em;line-height:1.75;color:#1a1a1a}"
        "h1{font-size:2em;text-align:center;margin:2em 0 .4em;line-height:1.3}"
        "h2{font-size:1.35em;margin-top:2.4em;margin-bottom:.6em}"
        "p{margin:0 0 1em;text-align:justify}"
        ".scene,.section-break{text-align:center;margin:2.2em auto;color:#777;letter-spacing:.5em}"
        "blockquote{font-style:italic;color:#444;margin:1.6em 2em}"
        "@media(max-width:600px){body{margin:.5em auto;padding:0 1.1em;font-size:1.08em}}"
    )
    result = (
        '<!DOCTYPE html>\n<html lang="pt-BR">\n<head>\n<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f'<title>{html.escape(TITLE)} — leitura beta</title>\n<style>{style}</style>\n'
        f'</head>\n<body>\n{body}\n</body>\n</html>\n'
    )
    path = ROOT / "05-PUBLICACAO" / "manuscrito_beta.html"
    path.write_text(result, encoding="utf-8")
    return path


def write_metadata(page_count: int, spine: float) -> None:
    readme = f'''# Pacote de publicação — {TITLE}

Arquivos preparados em {date.today().strftime('%d/%m/%Y')} para publicação independente.

## Arquivos para enviar à Amazon KDP

- **Kindle:** `ebook/A_Metade_Que_Me_Faltava_Era_Eu.epub`
- **Capa do Kindle:** `ebook/capa-kindle-1600x2560-v2.jpg`
- **Miolo impresso:** `impresso/miolo-5.5x8.5-creme-sem-sangria.pdf`
- **Capa impressa:** `impresso/capa-completa-5.5x8.5-creme.pdf`

## Configuração exata do impresso

- Tamanho: 5,5 × 8,5 polegadas
- Papel: creme
- Interior: preto e branco, sem sangria
- Página total do miolo: {page_count}
- Lombada calculada: {spine:.4f} polegada
- Acabamento sugerido: fosco

Não altere o número de páginas do miolo sem gerar novamente a capa completa, pois a largura da lombada depende desse total. Antes de publicar, substitua ou confirme os dados pessoais, fiscais, bancários, preço, territórios, ISBN e categorias diretamente na conta KDP.

O livro completo está disponível gratuitamente no site oficial. Não inscreva o eBook no KDP Select enquanto essa leitura integral permanecer pública: o programa exige exclusividade digital.
'''
    (OUT / "LEIA-ME.md").write_text(readme, encoding="utf-8")

    description = '''<p><strong>Camila cuida de tudo. Mas ninguém cuida dela.</strong></p>
<p>Há onze anos, ela organiza a casa, os filhos, o trabalho e até as responsabilidades de Ricardo. Ele diz que ajuda — mas nunca vê o que precisa ser feito.</p>
<p>Até que uma manhã comum, entre febre, lancheiras e leite derramado, mostra o que Camila já não consegue negar: está sozinha, mesmo acompanhada.</p>
<p>Ao escolher o divórcio, ela não encontra uma saída fácil. Encontra culpa, contas apertadas, medo de ferir os filhos e o julgamento de quem acha que mulher deve aguentar. Mas também reencontra os pincéis, a própria voz e uma vida que ainda pode ser sua.</p>
<p>Ao conhecer um homem gentil, Camila enfrenta uma pergunta ainda mais difícil: como amar sem transformar carinho em dependência — e continuar ouvindo a própria vontade?</p>
<p><em>A Metade Que Me Faltava Era Eu</em> é um romance contemporâneo sobre carga mental, maternidade, independência emocional, recomeço e amor-próprio — para toda mulher que já se sentiu invisível dentro da própria casa.</p>
'''
    (META / "descricao-amazon.html").write_text(description, encoding="utf-8")
    (META / "descricao-amazon.txt").write_text(re.sub(r"<[^>]+>", "", description).strip(), encoding="utf-8")

    metadata = f'''# Metadados sugeridos para Amazon KDP

## Identificação

- **Título:** {TITLE}
- **Subtítulo:** {SUBTITLE}
- **Autora:** {AUTHOR}
- **Idioma:** Português (Brasil)
- **Edição:** 1
- **Público:** adulto
- **Conteúdo sexual explícito:** não
- **Violência gráfica:** não

## Posicionamento

- Romance contemporâneo feminino sobre uma mulher sobrecarregada que deixa um casamento desigual e reconstrói a identidade.
- Leitoras interessadas em carga mental, maternidade real, divórcio, autoestima, independência emocional, recomeço e relações saudáveis.

## Sete frases-chave sugeridas

1. romance feminino sobre recomeço
2. livro sobre carga mental da mulher
3. ficção sobre divórcio e autoestima
4. romance sobre maternidade real
5. mulher recomeçando aos 35 anos
6. livro sobre relacionamento desigual
7. livro sobre independência emocional

## Categorias para avaliar no painel

- Ficção / Feminina
- Ficção / Contemporânea
- Ficção / Família e relacionamentos

As categorias disponíveis mudam conforme a loja e o formato. Escolha somente as que aparecem no painel brasileiro e representam de fato a obra.

## Aviso sobre conteúdo gerado com IA

As ilustrações da capa e dos capítulos foram geradas com inteligência artificial e receberam direção, seleção, composição e tratamento editorial. Responda ao campo de transparência da KDP de acordo com a regra vigente no momento do envio. O texto passou por revisão assistida; confirme a origem do manuscrito conforme o processo real de quem o escreveu, independentemente do pseudônimo público.

O livro completo está disponível gratuitamente no site oficial. Enquanto permanecer assim, não selecione KDP Select/exclusividade digital.
'''
    (META / "METADADOS_KDP.md").write_text(metadata, encoding="utf-8")

    checklist = '''# Checklist final antes de clicar em Publicar

- [ ] Confirmar nome literário e titular dos direitos autorais.
- [ ] Não selecionar KDP Select enquanto o texto completo estiver disponível no site.
- [ ] Conferir a descrição, as sete palavras-chave e as categorias no painel.
- [ ] Informar corretamente o uso de conteúdo gerado por IA.
- [ ] Escolher ISBN gratuito da KDP ou informar ISBN próprio para o impresso.
- [ ] Enviar o EPUB e abrir o Kindle Previewer em celular, tablet e e-reader.
- [ ] Enviar o miolo PDF com 5,5 × 8,5 pol., papel creme e sem sangria.
- [ ] Enviar a capa PDF correspondente ao mesmo número de páginas do miolo.
- [ ] Usar o Previewer de impressão e revisar todas as páginas sinalizadas.
- [ ] Pedir uma prova física antes de liberar a venda.
- [ ] Conferir preço, royalties, territórios, conta bancária e dados fiscais.
- [ ] Revisar a página do produto depois que ela entrar no ar.
'''
    (META / "CHECKLIST_UPLOAD.md").write_text(checklist, encoding="utf-8")


def validate_epub(path: Path) -> list[str]:
    issues: list[str] = []
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        if not names or names[0] != "mimetype":
            issues.append("mimetype não é o primeiro arquivo")
        if zf.getinfo("mimetype").compress_type != zipfile.ZIP_STORED:
            issues.append("mimetype está comprimido")
        for name in names:
            if name.endswith((".xhtml", ".opf", ".ncx", ".xml")):
                try:
                    ET.fromstring(zf.read(name))
                except ET.ParseError as exc:
                    issues.append(f"XML inválido em {name}: {exc}")
    return issues


def write_checksums() -> None:
    files = sorted(p for p in OUT.rglob("*") if p.is_file() and p.name != "SHA256SUMS.txt")
    rows = []
    for path in files:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(f"{digest}  {path.relative_to(OUT).as_posix()}")
    (OUT / "SHA256SUMS.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")


def make_zip() -> Path:
    target = ROOT / "PACOTE_PUBLICACAO" / "A_Metade_Que_Me_Faltava_Era_Eu_KDP.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                zf.write(path, Path("AMAZON_KDP") / path.relative_to(OUT))
    return target


def main() -> None:
    ensure_dirs()
    front_cover = build_front_cover()
    art_paths = optimize_art()
    manuscript = build_source_manuscript()
    build_beta_html()
    interior, page_count = build_interior(art_paths)
    epub = build_epub(front_cover, art_paths)
    cover_pdf, preview, spine = build_print_cover(front_cover, page_count)
    write_metadata(page_count, spine)
    issues = validate_epub(epub)
    if issues:
        raise SystemExit("EPUB inválido:\n- " + "\n- ".join(issues))
    write_checksums()
    archive = make_zip()
    report = {
        "title": TITLE,
        "chapters": len(CHAPTERS),
        "interior_pages": page_count,
        "spine_inches": round(spine, 4),
        "epub": str(epub),
        "interior_pdf": str(interior),
        "cover_pdf": str(cover_pdf),
        "cover_preview": str(preview),
        "manuscript": str(manuscript),
        "zip": str(archive),
        "epub_validation": "ok",
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
