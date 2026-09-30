# Revisão editorial e técnica — 29/09/2026

> **Passagem anterior, preservada como histórico.** A revisão integral posterior alterou novamente texto, métricas e arquivos. Use [CHECKUP_EDITORIAL_2026-09-29.md](CHECKUP_EDITORIAL_2026-09-29.md) para a edição atual de 328 páginas; as contagens abaixo não são as da entrega mais recente.

Este relatório registra a edição **local** após a nova varredura. É a referência atual para a equipe; relatórios datados de 24 a 27/09 documentam versões anteriores. Não confundir o site local com o GitHub Pages, que ainda depende de envio.

## Método e alcance

- Conferidos os 40 arquivos de capítulo quanto a ordem, abertura e fecho, afirmações de “primeira vez”, datas, idades, trabalho, convivência dos filhos, moradia de Ricardo, pintura, exposições, diário e desfecho. As cenas dos capítulos afetados receberam releitura direta com os capítulos vizinhos.
- Confrontados os fatos com `02-ESTRUTURA/CRONOLOGIA.md`; o README agora define passagens pequena, média, grande e geral, com mapa de risco por capítulo e regra para registrar achados.
- Executados gerador, validador estrutural e EPUBCheck 5.4.0. O leitor local foi aberto no navegador: após chegar ao fim do capítulo 16, a passagem para o 17 mostrou `scrollY=0`; o mesmo ocorreu de 17 para 18.
- Isto **não** equivale a uma leitura humana integral, em voz alta, de todas as 62 mil palavras nem a uma prova física. Nenhuma ferramenta pode garantir que toda leitora reagirá do mesmo modo.

## Correções por categoria

| Categoria | Capítulos | Ajuste realizado |
| --- | --- | --- |
| Ortografia e frase | 10–13, 15, 21, 31 | “E Fi”, “Um dia de cada vez”, “sobressaltada”, frase da escola, “caneta em riste”, “ruptura”, parcelas, jornal, fala de Dona Sônia, atraso de Ricardo, “Se vira”, diário, concordância e Dias das Mães. |
| Fala e referente | 9, 14, 21 | Inserida a fala de Bia antes da resposta de Camila; perguntas de Léo receberam falante; a advogada é procurada pela mãe, não “pelo casal”; a lembrança de Léo e a pergunta “nós vamos voltar” agora correspondem às cenas. A pergunta do terapeuta sobre arte ganhou preparação. |
| Ordem da cena | 10, 11 | A primeira noite após a saída de Ricardo deixou de ser contada duas vezes; medo, choro, mensagem de Fernanda e sono ficaram numa única sequência. No capítulo 11, a reflexão sobre a casa permaneceu no escritório, sem salto súbito para o carro. |
| Cronologia e convivência | 12, 15–18, 25, 39 | Removida combinação impossível de quinta-feira com dia 8 de abril; visitas antes do cap. 16 são sem pernoite; cap. 16 é o primeiro fim de semana inteiro; terça de trabalho no cap. 18 virou domingo livre; Ricardo sai do apart-hotel antes do cap. 25; exposição ocorre no sábado seguinte; diário aberto no 38 continua no 39, e conversa com Daniel ocorre uma semana depois. |
| Repetição de “primeira vez” | 15–18, 20 | Cinema, livros, cabelo, sábado inteiro, banho e pintura agora são experiências distintas e progressivas. A alegria de comprar para si no cap. 17 reconhece o caderno já comprado no 16. Retirada afirmação de que só no cap. 20 dormiu sem peso pela primeira vez. |
| Economia e arte | 17 | Kit de aquarela básico passa a custar R$ 120 e a primeira aula é reservada após conferir se cabe no dinheiro dos bolos; evita matrícula sem cálculo num semestre inteiro em meio ao aperto. |
| Leitor online | `ler.html` | Removida rolagem suave que mantinha o capítulo seguinte no fim durante a transição; reposição imediata do topo ou do marcador salvo e proteção contra carregamentos concorrentes. |

## Estado verificado dos arquivos

- 40 capítulos; **62.325 palavras de história** sem os dois cabeçalhos de cada capítulo; **62.556 com cabeçalhos** segundo `tools/validate_release.py`; **63.040 no manuscrito consolidado** com abertura e pós-texto.
- Miolo impresso reconstruído: **320 páginas**, 5,5 × 8,5 pol., papel creme, sem sangria. Capa recalculada para lombada de **0,800 pol.** A paginação anterior de 324 páginas não serve para upload desta edição.
- EPUBCheck 5.4.0: **0 erros fatais, 0 erros, 0 avisos**. `python tools/validate_release.py`: **APROVADO**. Checksums e ZIP foram refeitos após o relatório EPUBCheck e passaram no validador.
- Beta HTML, manuscrito consolidado, EPUB, PDF, capa e ZIP foram gerados da mesma fonte. A versão pública no GitHub não foi alterada nesta rodada.

## Portões que continuam abertos

1. Leitura da equipe-alvo, com observação por capítulo de trechos confusos, quedas de ritmo e vontade de seguir. Uma pessoa detectar contradição factual já basta para abrir correção; preferências de estilo pedem comparação entre leitoras.
2. Conferência visual no Kindle Previewer, no Previewer de impressão da KDP e numa prova física. O teste técnico não substitui essas etapas.
3. Decisões reais de ISBN/ficha catalográfica, dados da conta KDP e declaração de conteúdo gerado por IA. Se a ficha alterar a paginação, miolo, capa, hashes e ZIP devem ser refeitos.
4. Envio ao GitHub depois de revisar o `git status` e separar material não relacionado. O diretório `INSTAGRAM/` preexistente não foi alterado nesta revisão.

O texto está mais coerente e tecnicamente sincronizado, mas **não há promessa honesta de “zero erro” nem de best-seller** antes da leitura independente e das provas de publicação.
