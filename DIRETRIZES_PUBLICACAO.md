# DIRETRIZES DE FORMATAÇÃO E PUBLICAÇÃO

## Especificação final

Esta é a configuração aprovada da primeira edição independente de **A Metade Que Me Faltava Era Eu**.

| Item | Especificação |
|---|---|
| Formato | Brochura |
| Tamanho final | 5,5 × 8,5 polegadas (13,97 × 21,59 cm) |
| Miolo | Preto e branco em papel creme |
| Sangria | Sem sangria |
| Extensão | 278 páginas, incluindo página final em branco |
| Fonte do corpo | Georgia incorporada |
| Capítulos | 40, sempre iniciados em nova página |
| Ilustrações | Sete aberturas: capítulos 1, 8, 12, 17, 27, 34 e 40 |
| Capa Kindle | JPG RGB, 1600 × 2560 px |
| Capa impressa | PDF de uma página + JPG CMYK de conferência, 300 dpi |
| Lombada calculada | 0,695 pol. para 278 páginas em papel creme |

## Arquivos oficiais

- Miolo: `PACOTE_PUBLICACAO/AMAZON_KDP/impresso/miolo-5.5x8.5-creme-sem-sangria.pdf`
- Capa completa: `PACOTE_PUBLICACAO/AMAZON_KDP/impresso/capa-completa-5.5x8.5-creme.pdf`
- eBook: `PACOTE_PUBLICACAO/AMAZON_KDP/ebook/A_Metade_Que_Me_Faltava_Era_Eu.epub`
- Capa Kindle: `PACOTE_PUBLICACAO/AMAZON_KDP/ebook/capa-kindle-1600x2560-v2.jpg`

## Regras editoriais mantidas

- Diálogos com travessão.
- Quebras de cena padronizadas e centralizadas.
- Itálico reservado a pensamentos, mensagens e ênfases narrativas necessárias.
- Linguagem direta, afetiva e acessível, sem apagar a personalidade da narração.
- Ilustrações usadas apenas em viradas importantes, para criar conexão sem interromper o ritmo.
- Títulos, nomes, idades e cronologia devem seguir `02-ESTRUTURA/CRONOLOGIA.md` e `02-ESTRUTURA/ESTRUTURA_CAPITULOS.md`.

## Regra para qualquer alteração futura

Qualquer mudança no manuscrito exige executar novamente `python tools/build_publication.py` e depois `python tools/validate_release.py`. Se a quantidade de páginas mudar, a largura da lombada muda e a capa impressa deve ser regenerada antes do envio.
