# A Metade Que Me Faltava Era Eu

Romance contemporâneo em primeira edição independente, assinado com o nome literário **Mariana Duarte**. Camila sai de um casamento em que carregava sozinha a casa, os filhos e a própria esperança. O primeiro volume da trilogia encerra seu arco com uma escolha por autonomia: ela termina solteira, feliz e inteira. O segundo livro não é necessário para compreender este desfecho.

## Estado da edição — 26/09/2026

| Item | Situação |
| --- | --- |
| História | 40 capítulos, 62.724 palavras de história; pronta para leitura da equipe |
| Manuscrito consolidado | 63.364 palavras com cabeçalhos e textos iniciais/finais |
| Site e leitor | [GitHub Pages](https://maykonlong.github.io/book/) no ar, com leitura integral durante a fase de testes |
| Artes | 10 ilustrações narrativas presentes no leitor, EPUB e miolo |
| eBook | EPUB e capa Kindle preparados; EPUBCheck: 0 erros e 0 avisos |
| Impresso | Miolo de 324 páginas, 5,5 × 8,5 pol., e capa calculada para essa paginação |
| Validação local | `python tools/validate_release.py` — aprovado na versão de 26/09/2026 |
| Ainda falta | retorno da equipe, decisões finais de autoria/ISBN/ficha, Previewers da KDP e prova física |

O relatório técnico e os limites da revisão estão em [RELATORIO_VALIDACAO_FINAL.md](04-MATERIAL_APOIO/RELATORIO_VALIDACAO_FINAL.md). O estado de cada pendência está em [STATUS_ATUAL.md](04-MATERIAL_APOIO/STATUS_ATUAL.md). Nenhum teste automático garante ausência absoluta de erros ou reação comercial das leitoras.

## Para a equipe de leitura

Use o [roteiro da rodada](05-PUBLICACAO/ENTREGA_LEITURA_EQUIPE.md), o [manuscrito beta](05-PUBLICACAO/manuscrito_beta.html) ou o [leitor online](https://maykonlong.github.io/book/ler.html). O questionário está em [BETA_READERS.md](05-PUBLICACAO/BETA_READERS.md). Registre capítulo e trecho ao apontar uma incoerência; para ritmo e emoção, descreva em que momento a vontade de continuar aumentou ou diminuiu.

## Fontes e saídas

| Caminho | Função |
| --- | --- |
| `03-MANUSCRITO/` | 40 capítulos — fonte principal da história |
| `00-PLANEJAMENTO/`, `01-PERSONAGENS/`, `02-ESTRUTURA/` | voz, temas, personagens, mapa e cronologia |
| `index.html`, `ler.html`, `assets/` | site e leitura online |
| `PACOTE_PUBLICACAO/AMAZON_KDP/` | EPUB, capas, PDF, metadados, checklist e hashes |
| `tools/build_publication.py` | reconstrói as versões de publicação após mudança no texto |
| `tools/validate_release.py` | verifica estrutura, sincronização, links, artes e integridade |

Depois de qualquer alteração aprovada na história ou nos dados bibliográficos, execute `python tools/build_publication.py` e `python tools/validate_release.py`. Confira o EPUB no Kindle Previewer e o impresso no Previewer da KDP. Se a paginação mudar, refaça a capa e seus checksums/ZIP. Os arquivos atuais são **candidatos de publicação**, não uma autorização para enviar o impresso sem a conferência final.

## Decisão comercial em aberto

O livro integral está disponível no leitor e nos arquivos deste repositório **público**. Não selecione KDP Select enquanto essa distribuição digital continuar. Para o lançamento, veja o [plano de prévia e venda](05-PUBLICACAO/PLANO_PREVIA_AMAZON_E_PRECO.md): ele é um plano futuro, não uma restrição já aplicada ao site. Retirar um botão do leitor não retira EPUB, manuscrito e histórico do Git do acesso público.

O nome literário público é Mariana Duarte. Os dados civis, fiscais e bancários devem ser inseridos somente nos canais apropriados da KDP e dos órgãos responsáveis, nunca neste repositório.
