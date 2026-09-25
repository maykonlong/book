# SEO, GEO E AEO — IMPLEMENTAÇÃO OFICIAL

## Endereço público

- Página principal: https://maykonlong.github.io/book/
- Leitor: https://maykonlong.github.io/book/ler.html
- Sitemap: https://maykonlong.github.io/book/sitemap.xml

Não há mais placeholders de domínio no site.

## O que cada sigla significa

- **SEO:** ajuda mecanismos de busca a rastrear, entender e apresentar as páginas.
- **AEO:** organiza respostas claras para perguntas reais das leitoras.
- **GEO:** reforça informações consistentes e citáveis para sistemas de busca com IA.

Nenhuma técnica garante posição, citação ou venda. O resultado depende também de autoridade, links, procura pelo livro, qualidade do conteúdo e tempo de indexação.

## O que foi implementado

### Conteúdo e conversão

- Uma única promessa clara no topo: **“Você cuida de todo mundo. Mas quem cuida de você?”**
- CTA principal visível: **“Começar a ler grátis”**.
- Identificação do problema antes da sinopse.
- Sinopse curta, temas, trecho real do livro, autora, perguntas frequentes e CTA final.
- Remoção de depoimentos, resultados e prazos de leitura sem comprovação.
- Amazon apresentada apenas como futura publicação; nenhum link ou preço foi inventado.
- Linguagem acessível para leitoras adultas com diferentes níveis de escolaridade.

### SEO técnico

- Título e descrição próprios em `index.html` e `ler.html`.
- URL canônica apontando para o GitHub Pages real.
- `robots` permitindo indexação e prévia grande de imagem.
- Open Graph e Twitter Card com imagem horizontal original.
- HTML semântico, um `h1` principal, subtítulos claros e links descritivos.
- `sitemap.xml` apenas com URLs reais e data de alteração verdadeira.
- `manifest.json` com caminhos relativos, adequado ao subdiretório `/book/`.
- Contraste de texto e estados de foco melhorados.
- Layout responsivo e suporte a `prefers-reduced-motion`.

### Dados estruturados

O JSON-LD contém:

- `Book`: título, autora, capa final, idioma, gênero, descrição, público, temas, ano, palavras, páginas da edição impressa e ação de leitura.
- `Person`: identidade da autora.
- `WebSite` e `WebPage`: relação entre o site, a página e o livro.
- `FAQPage`: perguntas que também aparecem de forma visível na página.

Foram removidos:

- data de publicação não confirmada;
- editora inexistente;
- preço zero e disponibilidade de uma edição que ainda não está à venda;
- número de páginas antes de a edição impressa ser fechada;
- alegações de comportamento de leitoras sem dados.

### AEO e GEO

- Perguntas com respostas curtas e diretas: tema, gênero, público, carga mental, final e acesso.
- Nome do livro, autora e descrição usados de forma consistente.
- Explicação simples de “carga mental”, termo central da obra.
- `llms.txt` com resumo e links oficiais como arquivo complementar.
- `OAI-SearchBot` permitido no arquivo `robots.txt`.

`llms.txt` é complementar e não substitui SEO técnico. O Google informa que esse arquivo não interfere no ranqueamento. Para recursos de IA do Google, valem as mesmas bases do SEO comum: rastreabilidade, conteúdo útil, texto visível e dados consistentes.

## Observação sobre FAQ

A seção de perguntas continua útil para leitoras, mecanismos de busca e sistemas de resposta. Porém, não se deve prometer o antigo resultado visual de FAQ no Google: esse recurso foi descontinuado em 2026. O conteúdo permanece porque melhora compreensão e responde a dúvidas de compra e leitura.

## Próximos passos externos

- [ ] Verificar a propriedade no Google Search Console.
- [ ] Enviar `https://maykonlong.github.io/book/sitemap.xml` no Search Console.
- [ ] Solicitar indexação da página principal e do leitor.
- [ ] Testar o JSON-LD no Rich Results Test e no Schema Markup Validator.
- [ ] Conferir a prévia da imagem ao compartilhar no WhatsApp, Facebook e LinkedIn após a publicação.
- [ ] Cadastrar uma URL real da Amazon quando a edição estiver publicada e só então adicionar `Offer`, preço, ISBN e `rel="sponsored"` quando aplicável.
- [ ] Criar perfis oficiais da autora apenas quando houver URLs reais.
- [ ] Buscar resenhas legítimas; nunca criar depoimentos fictícios.

## Fontes oficiais de referência

- Google — recursos de IA e seu site: https://developers.google.com/search/docs/appearance/ai-features
- Google — atualizações da Pesquisa: https://developers.google.com/search/updates
- Google — criação de sitemap: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Google — dados estruturados de livro: https://developers.google.com/search/docs/appearance/structured-data/book
- OpenAI — orientação para editores e desenvolvedores: https://help.openai.com/en/articles/12627856-publishers-and-developers-faq

## Regra para futuras alterações

Toda informação comercial adicionada ao site deve ser verificável: preço, formato, ISBN, data de lançamento, disponibilidade, avaliações e links de compra. Até existir uma página real de venda, o objetivo principal da landing page é gerar identificação e levar a leitora ao primeiro capítulo.
