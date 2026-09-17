# 🚀 PASSO A PASSO — PUBLICAR NA AMAZON (KDP)

> Guia prático para publicar **"A Metade Que Me Faltava Era Eu"** na Amazon, em **eBook (Kindle)** e/ou **livro impresso** (impressão sob demanda). Atualizado em 17/09/2026 — confira sempre telas e valores atuais em `kdp.amazon.com`.

---

## 0. O que é e quanto custa

- **KDP** (Kindle Direct Publishing) é a plataforma **gratuita** da Amazon para publicar eBooks e livros impressos.
- Publicar é **grátis**. A Amazon fica com uma porcentagem das vendas (chamada *royalty*).
- Você **mantém os direitos autorais** e pode publicar em outros lugares (exceto se entrar no *KDP Select*, que exige exclusividade digital de 90 dias).

---

## 1. O que você já tem pronto (neste projeto)

| Item | Onde está |
|---|---|
| Manuscrito completo (front matter + 40 capítulos) | `manuscrito_completo.md` |
| Sinopse principal + curta + de 1 frase | `05-PUBLICACAO/PACOTE_EDITORIAL.md` |
| Palavras-chave / categorias / hashtags | `05-PUBLICACAO/PACOTE_EDITORIAL.md` |
| Bio da autora (falta preencher o nome) | `05-PUBLICACAO/PACOTE_EDITORIAL.md` |
| Resumo da história | `05-PUBLICACAO/PACOTE_EDITORIAL.md` |

---

## 2. Pré-requisitos (tenha em mãos)

1. ☐ **Nome da autora / pseudônimo** definido
2. ☐ **Revisão final** do texto (ortografia e gramática)
3. ☐ **Capa** pronta (dimensões na Seção 3)
4. ☐ **CPF ou CNPJ** (para os dados fiscais)
5. ☐ **Conta bancária brasileira** (para receber os royalties)
6. ☐ **E-mail** válido (para criar a conta KDP)

---

## 3. Capa — dimensões corretas

- **eBook**: recomendado **2560 × 1600 px** (proporção 1,6:1), mínimo 1000 px no lado maior. Formato JPG ou TIFF, até 50 MB.
- **Impresso** (ex.: 15 × 23 cm): a Amazon calcula as dimensões finais **com sangria (bleed)** depois que você escolhe o tamanho e o nº de páginas. Use o gerador de capa da própria KDP ou contrate um designer.

---

## 4. Formatação do manuscrito

- **eBook**: exporte o `manuscrito_completo.md` para **.docx** ou **.epub**.
- **Impresso**: use **.docx** ou **PDF** com margens espelhadas e tamanho de página configurado (ex.: 15 × 23 cm) e número de página.

### Como converter o .md para .docx
1. Abra o `manuscrito_completo.md`.
2. Com o **Pandoc** (gratuito): `pandoc manuscrito_completo.md -o manuscrito.docx`
3. No Word, revise títulos, espaçamento e insira quebras de página entre capítulos.

---

## 5. Criar a conta KDP

1. Acesse `kdp.amazon.com`.
2. Clique em **"Cadastre-se" / "Sign up"**.
3. Use uma conta Amazon existente ou crie uma nova.
4. Preencha os dados de **autor/editora**.

---

## 6. Dados fiscais (⚠️ importante para brasileiros)

1. Menu **"Configurações da conta"** → **"Informações fiscais"**.
2. Inicie a **"entrevista fiscal" (tax interview)**.
3. Declare que você **não é dos EUA** (pessoa física ou empresa).
4. Preencha o formulário **W-8BEN** informando o seu **CPF** (ou CNPJ).
5. Reivindique o **benefício do tratado Brasil–EUA** (royalties) → a retenção de imposto americano cai para **0%**.
6. Se preenchido corretamente, a Amazon **não retém** imposto nos EUA.

---

## 7. Dados bancários (como receber)

1. **"Configurações da conta"** → **"Informações de pagamento"**.
2. Adicione sua **conta bancária brasileira** (a KDP paga por depósito/transferência em BRL).
3. Defina a **moeda de pagamento**: BRL.
4. O pagamento ocorre ~**60 dias** após o fim do mês das vendas, quando você atinge o valor mínimo (confira o valor atual na ajuda da KDP).

---

## 8. Criar o eBook (Kindle)

1. Estante → **"+ Criar"** → **"eBook Kindle"**.
2. **Detalhes (metadados):**
   - Idioma: **Português**
   - **Título** e **subtítulo** (copie do pacote editorial)
   - **Autor(a)**
   - **Descrição** (cole a "Sinopse principal" do pacote)
   - Direitos: **"Eu possuo os direitos autorais"**
   - **Palavras-chave**: até 7 (use as do pacote editorial)
   - **Categorias**: escolha 2 (ex.: *Ficção > Mulheres*; *Ficção > Romance > Contemporâneo*)
3. **Conteúdo**: envie o `.docx`/`.epub` + a **capa**.
4. **Preço / royalty**: escolha **35%** ou **70%** (a 70% vale para preço entre ~R$ 2,99 e R$ 49,99 — confirme o intervalo atual).
5. Clique em **Publicar**.

---

## 9. KDP Select / Kindle Unlimited (recomendado para ficção)

- Ao publicar o eBook, marque **KDP Select** (exclusividade digital de 90 dias).
- **Vantagens:** o livro entra no **Kindle Unlimited** (assinantes leem "de graça" e você ganha por **página lida — KENP**), além de ferramentas de promoção (dias gratuitos, oferta relâmpago).
- **Desvantagem:** não pode vender o **eBook** em outras lojas (Apple, Google, Kobo) durante o período. (O impresso pode ser vendido em qualquer lugar.)

---

## 10. Criar o livro impresso (opcional, mas recomendado)

1. Estante → **"+ Criar"** → **"Livro de bolso"** (brochura).
2. **ISBN**: escolha **"ISBN gratuito da KDP"** (ou compre o seu na Agência Brasileira do ISBN — Seção 14).
3. Escolha **tamanho** (ex.: 15 × 24 cm ou 14 × 21 cm), **papel** (creme ou branco) e **acabamento** (brilho ou fosco).
4. Envie o **interior** (PDF/Word) + a **capa** (a KDP gera as dimensões exatas com sangria).
5. **Preço**: a KDP calcula o **custo de impressão**; defina o preço para ter lucro (você recebe ~60% do preço **menos** o custo de impressão).

---

## 11. Revisão e publicação

- Após enviar, o livro entra em **"revisão"** (até ~**72 horas**).
- Você recebe e-mail quando ele fica **"no ar"** (live) na loja Amazon.

---

## 12. Depois de publicar (marketing)

1. Pegue o **link** do livro e divulgue nas redes.
2. Peça **avaliações** a leitores/as iniciais (⚠️ não compre nem troque reviews — é proibido e pode banir a conta).
3. Use os **dias gratuitos** do KDP Select para dar visibilidade.
4. Considere **Amazon Ads** (anúncios por clique) quando já tiver algumas avaliações.
5. Acompanhe as **vendas** no relatório da estante KDP.

---

## 13. Royalties (resumo)

| Formato | O que você recebe |
|---|---|
| eBook **35%** | 35% do preço (qualquer faixa de preço) |
| eBook **70%** | 70% do preço, menos taxa de entrega (por MB do arquivo) |
| **Impresso** | 60% do preço de tabela, menos o custo de impressão |

---

## 14. ISBN e Depósito Legal (Brasil)

- **eBook**: **não** precisa de ISBN no KDP (a Amazon atribui um **ASIN**).
- **Impresso**: **precisa** de ISBN. Use o gratuito da KDP ou compre na **Agência Brasileira do ISBN** (`isbn.cbl.org.br`).
- **Depósito legal** (Lei 10.994/2004): exemplares **impressos** publicados no Brasil devem ser depositados na **Biblioteca Nacional** (`bn.gov.br`). Confira a quantidade e o endereço atuais.

---

## 15. Checklist final

- ☐ Nome / bio da autora preenchidos
- ☐ Texto revisado
- ☐ Capa pronta (eBook 2560×1600; impresso com sangria)
- ☐ Manuscrito convertido para .docx/.epub
- ☐ Sinopse, keywords e categorias definidas (já no pacote editorial)
- ☐ Conta KDP criada
- ☐ W-8BEN preenchido (CPF)
- ☐ Conta bancária BR cadastrada
- ☐ eBook publicado (+ KDP Select, se quiser)
- ☐ Impresso publicado (opcional)
- ☐ Link divulgado

---

## 16. Erros comuns a evitar

- ❌ Não preencher o **W-8BEN** → a Amazon retém ~30% de imposto dos EUA.
- ❌ Enviar capa fora da proporção → fica **cortada/borrada**.
- ❌ Deixar o livro **gratuito** sem estar no KDP Select (o gratuito permanente exige preço em todas as lojas).
- ❌ Comprar ou trocar avaliações → risco de **banimento**.
- ❌ Publicar sem revisar (corrigir depois exige nova revisão e pode "derrubar" o livro por dias).
- ❌ Usar título/capa igual a outro livro → problema de **direitos autorais**.

---

## 17. Links úteis

| Recurso | Link |
|---|---|
| KDP (publicar) | `kdp.amazon.com` |
| Ajuda do KDP (royalties, formatos, pagamento) | `kdp.amazon.com/help` |
| ISBN Brasil (Agência/CBL) | `isbn.cbl.org.br` |
| Depósito legal | `bn.gov.br` |
| Ficha catalográfica (CBL) | `cbl.org.br` |

---

> 💡 **Dica final:** publique primeiro o **eBook** (mais rápido e sem custo de impressão). Depois de validar o texto e a capa, publique o **impresso**. O eBook no **Kindle Unlimited** costuma ser a porta de entrada para leitores de ficção feminina no Brasil.

---

