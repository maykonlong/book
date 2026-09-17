# 📖 LEITOR ONLINE (index.html)

> Um "reader" web que lê os capítulos `.md` **direto do repositório** e os exibe como um livro, **salvando no navegador onde a leitora parou** — sem alterar o manuscrito.

## O que é

O `index.html` (na raiz do projeto) é um leitor de livro:
- Carrega cada capítulo `.md` via `fetch()` (lê de lá direto, sem duplicar o texto).
- Renderiza o markdown (títulos, itálico, negrito, epígrafe, `---` de cena) como HTML.
- Salva o progresso (capítulo + posição de rolagem) no **localStorage** do navegador.

## Recursos

- ☰ **Índice** lateral com os 41 capítulos (capa + 40)
- Navegação **← / →** (botões e setas do teclado)
- **A− / A+** (tamanho da fonte)
- 🌙 **modo claro/escuro**
- Barra de **progresso de leitura** no topo
- **"Continuar de onde parou"** automático ao reabrir

## Como ativar (GitHub Pages — grátis)

1. No repositório do GitHub: **Settings → Pages**
2. Em "Source": **Deploy from a branch**
3. Branch: **main** · pasta: **/ (root)**
4. Salve. Em ~1 minuto o leitor fica em:
   `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`

## Testar localmente (opcional)

```bash
npx serve .
# abre http://localhost:3000
```

## Observações importantes

- ⚠️ **Não funciona** abrindo o `index.html` com duplo clique (`file://`) — o navegador bloqueia `fetch()` de arquivos locais (CORS). Precisa de **HTTP** (GitHub Pages ou servidor local).
- O manuscrito (`.md`) **não é alterado** — o reader só lê os arquivos.
- Se adicionar/renomear capítulos, atualize a lista `CHAPTERS` no início do `index.html`.
