# GUIA DE CONVERSÃO E DIAGRAMAÇÃO

## Arquivos finais desta edição

O projeto inclui um gerador editorial em `tools/build_publication.py`. Ele reúne o manuscrito, trata as artes e cria o pacote de publicação em `PACOTE_PUBLICACAO/AMAZON_KDP/`.

Execute a partir da raiz do repositório:

```powershell
python tools/build_publication.py
```

## Arquivos produzidos

- `ebook/A_Metade_Que_Me_Faltava_Era_Eu.epub`: EPUB 3 com sumário navegável, capa e sete ilustrações.
- `ebook/capa-kindle-1600x2560-v2.jpg`: capa RGB para eBook.
- `impresso/miolo-5.5x8.5-creme-sem-sangria.pdf`: miolo pronto para o formato impresso.
- `impresso/capa-completa-5.5x8.5-creme.pdf`: contracapa, lombada e capa em um único PDF.
- `metadados/`: descrição, palavras-chave, categorias sugeridas e checklist de envio.
- `SHA256SUMS.txt`: assinaturas para confirmar que os arquivos não foram alterados.

## Configuração usada no impresso

- Tamanho de corte: 5,5 × 8,5 polegadas.
- Papel: creme.
- Interior: preto e branco.
- Sangria do miolo: não.
- Total atual: 278 páginas.
- Lombada atual: 0,695 polegada.
- Capa: CMYK, 300 dpi, com sangria externa de 0,125 polegada.

Se o texto ou a paginação mudar, gere novamente o miolo e a capa na mesma execução. A lombada depende do total exato de páginas.

## Kindle

A Amazon aceita EPUB. O formato MOBI não deve ser gerado para um novo envio à KDP. Abra o EPUB no Kindle Previewer e verifique:

- sumário e navegação;
- início de cada capítulo;
- tamanho e posição das imagens;
- itálicos, travessões e separadores de cena;
- leitura em celular, tablet e e-reader.

## Impresso

No painel da KDP, selecione exatamente 5,5 × 8,5 polegadas, papel creme, interior preto e branco e sem sangria. Envie os dois PDFs do diretório `impresso/`, abra o Previewer e depois peça uma prova física.

## Regra de segurança

Não envie a imagem JPG da capa completa como miolo e não envie a capa Kindle no campo do livro impresso. Os nomes de arquivo deixam claro o destino correto de cada item.
