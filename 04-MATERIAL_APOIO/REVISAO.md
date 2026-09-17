# 🔍 RELATÓRIO DE REVISÃO (1ª passada — coesão e continuidade)

> Data: 17/09/2026 · Escopo: revisão estrutural e de personagens do manuscrito (40 capítulos).

---

## ✅ O que foi verificado e está OK

| Item | Resultado |
|---|---|
| Sequência de capítulos | 1–40, sem falhas nem duplicatas (validado por script) |
| Cabeçalhos (`# CAPÍTULO N`) | Batem com o nome do arquivo em todos os 40 (validado) |
| Nome da filha | **Bia** (corrigido — ver abaixo) |
| Terapeuta | **Dr. Lucas** (homem) — consistente nos caps 14, 15, 18, 31, 32… |
| Médica do PS | **Dra. Helena** (CAP 8) — papel distinto da terapeuta, sem conflito |
| Mães/avós | Dona Sônia (mãe de Camila), Dona Vera (mãe de Ricardo), Dona Lúcia (mãe de Daniel) — três personagens distintas |
| "Dois primeiros cafés" | Resolvido: CAP 31 explicita *"era o segundo café deles. O primeiro… tinha sido um desastre silencioso"* |
| Cronologia das exposições | CAP 29 (exposição do ateliê, onde conhece Daniel) ≠ CAP 40 (exposição maior, final) — ~1 ano de distância |
| Idade de Léo | 8 (Ato I) → 9 (Atos II/III) — coerente |
| Idade de Bia | 4 (Ato I) → 5 (Atos II/III) — coerente |
| Daniel | Professor universitário de literatura (CAP 29) — coerente com a ficha |
| Sobrenome de Camila | "Camila Ferreira Santos" (tirou o sobrenome do ex no divórcio) — coerente |

---

## 🔧 Correção aplicada

**Erro crítico de nome:** a filha de Camila foi chamada de **"Sofia"** em dois capítulos, enquanto o nome canônico (ficha de personagens e todos os demais capítulos) é **"Bia"**.

- ✅ `CAP_24_O_DIA_EM_QUE_LEO_PERGUNTOU_SOBRE_O_PAI.md` — "Sofia" → "Bia" (8 ocorrências) + "Sofia, seis" → "Bia, cinco"
- ✅ `CAP_34_A_PRIMEIRA_VIAGEM_A_QUATRO.md` — "Sofia" → "Bia" (7 ocorrências)

**Observação:** as ocorrências de "Sofia" que restam são legítimas — no CAP 2 ("a festa da Sofia", uma coleguinha de escola) e no CAP 14 ("filosofia", falso positivo de busca).

---

## 📋 Pendências

1. [x] **Revisão ortográfica/gramatical (1ª varredura automática)** — ver "Correções ortográficas" abaixo (recomenda-se ainda uma leitura humana em voz alta)
2. [ ] **Beta readers** (mulheres 28–45, casadas/separadas, mães) — materiais prontos (`BETA_READERS.md` + `manuscrito_beta.html`); falta recrutar e coletar o feedback
3. [ ] Decidir se **expande para 75–85k** (aprofundando capítulos médios — média atual ~1.415 p/cap)
4. [ ] Preencher **nome/bio da autora** no pacote editorial
5. [ ] Formatação final + capa

---

## 🔧 Correções ortográficas aplicadas (varredura automática)

| Arquivo | Erro | Correção |
|---|---|---|
| CAP_15 (A Nova Rotina) | "Camilafez" (falta de espaço) | "Camila fez" |
| CAP_15 (A Nova Rotina) | "impas" | "limpas" |

**Verificações feitas (sem erros encontrados):**
- Palavras repetidas seguidas: **0**
- Espaços duplos: **0**
- Concordância de gênero ("obrigado/obrigada", "sozinho/sozinha"): **todos corretos** (inclusive "a obrigado" no CAP 40, que é particípio com "ter", invariável)
- "vc" no bilhete do Léo (CAP 21): **mantido** — escrita autêntica de criança de 9 anos

> ⚠️ A varredura automática encontra erros óbvios, mas **não substitui** uma leitura humana em voz alta, que capta repetições de estilo, ritmo e nuances que o script não detecta.

---

## 🎨 Estilo — repetições (corrigido)

Varredura de frases recorrentes + correção aplicada:

| Frase | Antes | Depois |
|---|---|---|
| "pela primeira vez" | **51** | **2** (mantidos só os do clímax: CAP 38 e 40) |
| "enfim" (conector usado na variação) | ~8 | 28 (aceitável, espalhado) |

**O que foi feito:** 49 ocorrências repetitivas de "pela primeira vez" foram substituídas por variações contextuais ("enfim", "agora", "desta vez", "depois de onze anos", "em meses", "como há anos não" etc.), preservando apenas os dois momentos de clímax emocional — o *"Pela primeira vez, tudo."* (reencontro com Ricardo) e o *"pela primeira vez na vida"* (encerramento).

**Demais repetições ainda presentes (aceitáveis):** "como se" (~58), "de novo" (~41), "de verdade" (~35), "finalmente" (~31) — são conectores comuns; podem ser suavizados numa leitura final, se desejar.

---

## 🔎 Varredura preventiva de "restos de substituição" (17/09)

Após o bug **"Quatroês"** (substituição parcial `Três → Quatro` que deixou o "ês" sobrando), foi feita uma varredura por padrões semelhantes em todo o projeto:

| Padrão procurado | Resultado |
|---|---|
| "Quatro" + acento (ex.: "Quatroês") | ✅ 0 |
| "oês" (resto de "três") | ✅ 0 |
| "Bia" + acento (resto de "Sofia") | ✅ 0 |
| "filoBia" ("filosofia" corrompida) | ✅ 0 |
| "Sofia" (filha) restante | ✅ 0 — só usos legítimos (coleguinha no CAP 2 e "filosofia") |

**Conclusão:** nenhum outro resíduo de substituição encontrado. O manuscrito está íntegro.



---
