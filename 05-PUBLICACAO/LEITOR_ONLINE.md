# Site + leitor online (index.html + ler.html)

> **Já publicado nesta fase de testes:** [página inicial](https://maykonlong.github.io/book/) e [leitor](https://maykonlong.github.io/book/ler.html). O leitor lê os capítulos `.md` **direto do repositório público** e salva no navegador onde a leitora parou. O texto completo está acessível; este documento não muda a estratégia futura de venda.

## Estrutura

- **`index.html`** → página de apresentação do livro (capa, sinopse, tagline, botão "Ler online", futuros links de venda/redes sociais).
- **`ler.html`** → o leitor de livro.

## O que é o leitor (`ler.html`)

O `ler.html` (na raiz do projeto) é um leitor de livro:
- Carrega cada capítulo `.md` via `fetch()` (lê de lá direto, sem duplicar o texto).
- Renderiza o markdown (títulos, itálico, negrito, versículos em destaque e `---` de cena) como HTML.
- Salva o progresso (capítulo + posição de rolagem) no **localStorage** do navegador.

## Recursos

- ☰ **Índice** lateral com 45 entradas (abertura, versículo inicial, 40 capítulos, dois pós-textos e consagração final)
- Navegação **← / →** (botões e setas do teclado)
- **A− / A+** (tamanho da fonte)
- 🌙 **modos claro, sépia e escuro**
- Barra de **progresso de leitura** no topo
- **"Continuar de onde parou"** automático ao reabrir

## Configuração atual do GitHub Pages

O endereço público já é `https://maykonlong.github.io/book/`. Na configuração do repositório, a publicação usa a branch `main` e a raiz do projeto. Depois de enviar alterações, confira o site publicado e os capítulos alterados antes de anunciar a atualização; a propagação pode demorar.

## Testar localmente (opcional)

```bash
npx serve .
# abre http://localhost:3000
```

## Observações importantes

- ⚠️ **O leitor não funciona** abrindo com duplo clique (`file://`) — o navegador bloqueia `fetch()` de arquivos locais (CORS). Precisa de **HTTP** (GitHub Pages ou servidor local).
- O manuscrito (`.md`) **não é alterado** — o reader só lê os arquivos.
- Se adicionar/renomear capítulos, atualize a lista `CHAPTERS` no início do `ler.html`.
- **KDP Select:** não basta esconder o botão de leitura. Este repositório público também contém manuscrito, EPUB, PDFs e histórico. Consulte `05-PUBLICACAO/PLANO_PREVIA_AMAZON_E_PRECO.md` antes de qualquer mudança de distribuição.
