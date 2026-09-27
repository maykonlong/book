# Estado atual e portões de publicação — 26/09/2026

Este documento substitui checklists antigos como referência rápida. **Pronto para leitura da equipe não significa pronto para clicar em “Publicar”.** A base do manuscrito desta rodada é o commit `cd09ccf`; as atualizações documentais posteriores não alteram a história.

## O que já pode ser usado agora

- 40 capítulos em sequência; 62.724 palavras de história; fechamento do primeiro volume com Camila solteira, feliz e inteira.
- `05-PUBLICACAO/manuscrito_beta.html` e [leitor online](https://maykonlong.github.io/book/ler.html) para a equipe, com [roteiro de leitura](../05-PUBLICACAO/ENTREGA_LEITURA_EQUIPE.md).
- Site público, 10 artes integradas e pacote KDP candidato: EPUB, capa Kindle, miolo impresso de 322 páginas, capa correspondente, metadados, hashes e ZIP.
- `python tools/validate_release.py` passou na versão atual; o EPUBCheck registrado no pacote tem 0 erros e 0 avisos.

## O que depende do retorno da equipe

1. Coletar observações por capítulo/trecho sobre clareza, ritmo, naturalidade, continuidade e força do final. Procurar padrões; não reescrever por uma preferência isolada.
2. Decidir cada alteração e registrar o motivo. Revisar concordância e cronologia nas bordas dos capítulos afetados.
3. Se o texto mudar, reconstruir site, beta, EPUB, PDF, capa, ZIP e hashes com `python tools/build_publication.py`; rodar `python tools/validate_release.py` e inspeção visual outra vez. Não misturar versões.

## O que falta antes do envio definitivo ao KDP

- Conferir nome literário, dados de autoria/direitos e declaração de conteúdo gerado por IA conforme o processo real de criação.
- Definir o ISBN da brochura (gratuito da KDP ou próprio) e conferir/incluir a ficha catalográfica da edição brasileira segundo o [guia de direitos e ISBN](../05-PUBLICACAO/GUIA_ISBN_DIRETOS_AUTORAIS.md). Se isso mudar páginas, refazer miolo e capa.
- Abrir o EPUB no Kindle Previewer e o PDF/capa no Previewer de impressão; conferir índice, imagens, margens, metadados e avisos.
- Pedir e aprovar uma prova física, especialmente legibilidade da contracapa, corte, lombada e cores.
- No painel, decidir preço, categorias, territórios e dados fiscais/bancários. Inserir link de compra real no site somente depois de a página existir.

## Exclusividade digital: decisão ainda não tomada

O livro completo está no GitHub Pages e também no repositório público, inclusive EPUB, PDF e histórico. **Não selecionar KDP Select nesse estado.** Para considerar Select, resolver a distribuição digital pública, revisar histórico/cópias e obter orientação da KDP sobre a exposição anterior. Se optar por KDP sem Select, o plano futuro propõe uma prévia até o capítulo 8, implementada somente quando houver links reais de compra. Consulte [PLANO_PREVIA_AMAZON_E_PRECO.md](../05-PUBLICACAO/PLANO_PREVIA_AMAZON_E_PRECO.md).

## Referência técnica

O [relatório de validação](RELATORIO_VALIDACAO_FINAL.md) e o [pente-fino](PENTE_FINO_2026-09-26.md) documentam o que foi examinado e o que ainda exige leitura humana. Planos iniciais, logs de expansão e números de versões anteriores são históricos; este documento e os arquivos gerados atuais prevalecem para a rodada da equipe.
