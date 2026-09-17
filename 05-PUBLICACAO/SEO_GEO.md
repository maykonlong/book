# 🔎 SEO + GEO — "A Metade Que Me Faltava Era Eu"

> Documentação de tudo o que foi implementado para o livro ser encontrado em **buscadores (Google/Bing)**, **redes sociais** e **IA (ChatGPT, Google AI Overviews, etc.)**.

---

## 1. O que é SEO e GEO (resumo)

- **SEO (Search Engine Optimization):** fazer o site aparecer bem no Google — com título, descrição, dados estruturados, sitemap.
- **GEO (Generative Engine Optimization):** fazer a IA (ChatGPT, Gemini, Perplexity, respostas do Google) **entender e citar** o livro — com conteúdo claro, estruturado e "perguntas/respostas".

---

## 2. O que já foi implementado

### 2.1 No `index.html` (página principal)
- ✅ `<meta name="description">` e `<meta name="keywords">`
- ✅ `<meta name="author">` (Mariana Duarte) e `robots` (index, follow)
- ✅ `canonical` (evita conteúdo duplicado)
- ✅ **Open Graph** (título, descrição, imagem, URL) — para compartilhar bonito no **Facebook/WhatsApp/LinkedIn/Pinterest**
- ✅ **Twitter Card** — para compartilhar bonito no **X/Twitter**
- ✅ **Dados estruturados JSON-LD (schema.org):**
  - `Book` (título, autor, gênero, idioma, descrição, palavras-chave)
  - `FAQPage` (perguntas e respostas — o que a IA usa para responder)
- ✅ **Seção de FAQ** visível na página (perguntas frequentes)

### 2.2 No `ler.html` (leitor)
- ✅ `meta description`, `canonical`, Open Graph e Twitter Card básicos

### 2.3 Arquivos de apoio
- ✅ `sitemap.xml` — lista as páginas para o Google indexar
- ✅ `robots.txt` — autoriza os buscadores e aponta para o sitemap

---

## 3. Palavras-chave usadas (SEO/GEO)

`ficção feminina · autodescoberta · empoderamento feminino · divórcio · recomeço · amor-próprio · carga mental · maternidade · Mariana Duarte · A Metade Que Me Faltava Era Eu`

---

## 4. O que VOCÊ precisa fazer (substituir os placeholders)

1. **Trocar `SEU-DOMINIO.com.br`** pelo seu domínio real em:
   - `index.html` (canonical, Open Graph, JSON-LD)
   - `ler.html` (canonical, Open Graph)
   - `sitemap.xml` e `robots.txt`
2. **Criar a imagem da capa** (`capa.jpg`, ideal 1200×630px) e subir no site — usada no compartilhamento das redes.
3. **Enviar o sitemap** no **Google Search Console** (`search.google.com/search-console`) → Sitemaps → colar a URL do `sitemap.xml`.
4. (Opcional) Cadastrar o livro no **Google Books** e no **schema.org** para reforçar.

---

## 5. Como saber se está funcionando

- **Teste de dados estruturados:** `search.google.com/test/rich-results` (cole a URL do site).
- **Teste de compartilhamento:** jogue a URL no WhatsApp/Facebook e veja se aparece título + imagem.
- **IA:** pergunte ao ChatGPT/Perplexity "sobre o que é o livro A Metade Que Me Faltava Era Eu" depois de indexado.

---

## 6. Próximos passos de SEO (quando publicar)

- [ ] Adicionar o link da **Amazon** (com atributo `rel="sponsored"`).
- [ ] Criar perfis nas redes e linkar no site (Instagram, TikTok).
- [ ] Publicar a **sinopse** também na Amazon, Goodreads e Skoob (mais fontes = mais chances de a IA citar).
- [ ] Pedir avaliações/resenhas (aumentam autoridade).

---

## 7. Nível master (adições avançadas — já implementadas)

- ✅ **JSON-LD enriquecido:** `Book` completo (páginas, público-alvo, temas, oferta, ação de leitura) + `Person` (autora) + `WebSite` + `FAQPage` com **6 perguntas**.
- ✅ **FAQ ampliada** na página (6 perguntas visíveis, casando com o markup).
- ✅ **Seção "Trechos do livro"** — citações marcantes (compartilháveis e citáveis por IA).
- ✅ **`llms.txt`** — padrão de descoberta de conteúdo por IAs/LLMs (llmstxt.org).
- ✅ **`manifest.json`** — PWA (nome, tema, cores) para "instalar" o site.
- ✅ **Favicon** (SVG embutido) e meta tags da **Apple**.
- ✅ **Open Graph com dimensões** (1200×630) e `og:image:alt`.

> Com isso, o livro tem **entidade clara e consistente** (título + autora + temas + público), o que faz o Google e as IAs (ChatGPT, Gemini, Perplexity) conseguirem **referenciar o livro para "toda mulher"** que buscar por recomeço, divórcio e amor-próprio.
