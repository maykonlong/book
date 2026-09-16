# GUIA DE CONVERSÃO E DIAGRAMAÇÃO
## Do Markdown ao ePub / MOBI / PDF

O manuscrito está em 27 arquivos Markdown em **03-MANUSCRITO/**. Para publicar, é preciso unificá-los e convertê-los.

---

## 1. Unificar o manuscrito (PowerShell)

Os arquivos já estão numerados (CAP_01 a CAP_27), então a ordem alfabética é a ordem correta. Execute a partir da pasta `book`:

```powershell
$capitulos = Get-ChildItem "03-MANUSCRITO\CAP_*.md" | Sort-Object Name
$capitulos | Get-Content | Set-Content "manuscrito_completo.md"
```

## 2. Converter com Pandoc (recomendado)

### ePub (Kobo, Google Play, Apple Books, etc.)
```bash
pandoc manuscrito_completo.md -o livro.epub \
  --metadata title="A Metade Que Me Faltava Era Eu" \
  --metadata author="[Seu Nome]" \
  --metadata lang="pt-BR"
```

### PDF (via LaTeX — exige instalação de um TeX, ex.: MiKTeX)
```bash
pandoc manuscrito_completo.md -o livro.pdf \
  -V geometry:a5paper -V geometry:margin=2cm \
  -V mainfont="DejaVu Serif" -V lang=pt-BR
```

### MOBI (Kindle) — via Calibre
1. Abra o ePub no **Calibre** (https://calibre-ebook.com).
2. Selecione o livro → **Converter livros** → formato **MOBI**.

## 3. Sem instalar nada (alternativas online)
- **Amazon Kindle Create** (kindle.amazon.com): importa DOCX/PDF e gera o KPF para a loja.
- **Reedsy Book Editor** (reedsy.com): editor online grátis que exporta ePub/PDF.
- **Google Docs → Arquivo → Baixar → EPUB** (exportação nativa).

## 4. Antes de converter — ajustes no texto
- [x] Travessões já padronizados ("—").
- [x] Itálicos de pensamento já aplicados.
- [ ] Substituir `---` (separadores de cena) por `***` ou `* * *` centralizado, se quiser padronizar.
- [ ] Conferir que cada capítulo começa em nova página (no Word/InDesign).

## 5. Especificações alvo (do `DIRETRIZES_PUBLICACAO.md`)
- Página **A5** (14 × 21 cm); margens 2 cm (interna 2,5 cm).
- Fonte serifada 11 pt; entrelinha 1,15.
- Total estimado: ~160–180 páginas.
