# A Metade Que Me Faltava Era Eu

Romance contemporâneo em primeira edição independente, assinado com o nome literário **Mariana Duarte**. Camila sai de um casamento em que carregava sozinha a casa, os filhos e a própria esperança. O primeiro volume da trilogia encerra seu arco com uma escolha por autonomia: ela termina solteira, feliz e inteira. O segundo livro não é necessário para compreender este desfecho.

## Estado da edição — 29/09/2026

| Item | Situação |
| --- | --- |
| História | 40 capítulos, 63.505 palavras de história; candidata à nova rodada da equipe |
| Manuscrito consolidado | 64.227 palavras com cabeçalhos e textos iniciais/finais |
| Site e leitor | [GitHub Pages](https://maykonlong.github.io/book/) no ar; leitor instalável que retoma o progresso, sem livro inteiro offline |
| Artes | 10 ilustrações narrativas presentes no leitor, EPUB e miolo |
| eBook | EPUB e capa Kindle preparados; EPUBCheck: 0 erros e 0 avisos |
| Impresso | Miolo de 328 páginas, 5,5 × 8,5 pol., e capa recalculada para essa paginação |
| Validação local | `python tools/validate_release.py` — aprovado em 29/09/2026 |
| Ainda falta | retorno da equipe, decisões finais de autoria/ISBN/ficha, Previewers da KDP e prova física |

O [checkup integral](04-MATERIAL_APOIO/CHECKUP_EDITORIAL_2026-09-29.md) registra os 40 capítulos e a revisão por categoria da edição **2026-09-29-checkup-integral**. O [relatório mais curto do mesmo dia](04-MATERIAL_APOIO/RELATORIO_REVISAO_2026-09-29.md) descreve a passagem anterior. O estado de cada pendência está em [STATUS_ATUAL.md](04-MATERIAL_APOIO/STATUS_ATUAL.md). Nenhum teste automático garante ausência absoluta de erros ou reação comercial das leitoras.

## Para a equipe de leitura

Use o [roteiro da rodada](05-PUBLICACAO/ENTREGA_LEITURA_EQUIPE.md), o [manuscrito beta](05-PUBLICACAO/manuscrito_beta.html) ou o [leitor online](https://maykonlong.github.io/book/ler.html). O questionário está em [BETA_READERS.md](05-PUBLICACAO/BETA_READERS.md). Registre capítulo e trecho ao apontar uma incoerência; para ritmo e emoção, descreva em que momento a vontade de continuar aumentou ou diminuiu.

O [leitor instalável](05-PUBLICACAO/PWA_LEITOR.md) abre no ponto salvo no mesmo navegador ou app. Precisa de internet para carregar os capítulos e não sincroniza o marcador entre aparelhos.

A abertura ganhou uma página com Eclesiastes 3:1 antes do capítulo 1. Os agradecimentos incluem uma gratidão a Deus; a página final reúne Salmos 90:17 e uma oração de consagração. As referências e a edição bíblica utilizada estão em [FONTES_BIBLICAS.md](05-PUBLICACAO/FONTES_BIBLICAS.md).

## Fontes e saídas

| Caminho | Função |
| --- | --- |
| `03-MANUSCRITO/` | 40 capítulos — fonte principal da história |
| `00-PLANEJAMENTO/`, `01-PERSONAGENS/`, `02-ESTRUTURA/` | voz, temas, personagens, mapa e cronologia |
| `index.html`, `ler.html`, `assets/` | site e leitura online |
| `PACOTE_PUBLICACAO/AMAZON_KDP/` | EPUB, capas, PDF, metadados, checklist e hashes |
| `tools/build_publication.py` | reconstrói as versões de publicação após mudança no texto |
| `tools/validate_release.py` | verifica estrutura, sincronização, links, artes e integridade |
| `tools/test_landing.cjs` | testes da landing, retomada, FAQ, temas e indicação, sem dependências externas |

Depois de qualquer alteração aprovada na história ou nos dados bibliográficos, execute `python tools/build_publication.py` e `python tools/validate_release.py`. Confira o EPUB no Kindle Previewer e o impresso no Previewer da KDP. Se a paginação mudar, refaça a capa e seus checksums/ZIP. Os arquivos atuais são **candidatos de publicação**, não uma autorização para enviar o impresso sem a conferência final.

## Landing editorial — atualização de 29/09/2026

A landing foi reorganizada para celular: capa e ação de leitura na primeira tela, trecho fiel do capítulo 7 logo após a abertura, sinopse com as artes existentes e três situações em destaque. Os outros dez temas ficam em um controle nativo expansível, acessível também sem JavaScript. Os 13 temas continuam no HTML e nos dados estruturados; as respostas do FAQ visível e do JSON-LD são iguais. A página não antecipa a escolha final de Camila, não inventa depoimentos e mantém a leitura completa gratuita durante esta fase. O lançamento comercial ainda é uma decisão futura.

A indicação só ocorre após ação da visitante: compartilhamento nativo, cópia do endereço ou campo selecionável quando o navegador não permite copiar. Não há envio automático, rastreadores ou cadastros. A retomada consulta o marcador atual `v2` e o legado `v1`, sem alterar a posição salva; atualiza os botões ao voltar pelo histórico ou ao receber mudança de outra aba. O app continua sem guardar o romance inteiro offline.

Antes de publicar qualquer alteração da landing, rode `node tools/test_landing.cjs` e `python tools/validate_release.py`. Os testes de compartilhamento são simulações locais, não envios reais. Confira no navegador a primeira visita, a retomada, início pela capa, navegação por teclado, expansão/recolhimento dos temas, FAQ, botão móvel e falta de rolagem lateral. Nesta rodada, a inspeção visual cobriu 320, 390, 768 e 1440 px. Em 390 × 844, a página fechada passou de cerca de 14,3 mil para 5,7 mil pixels de altura, mantendo os 13 temas acessíveis. Isso mede a redução de rolagem, não aumento garantido de vendas.

Somente a apresentação do site mudou nesta rodada: manuscrito, EPUB, PDF, capas e ZIP KDP não foram reescritos. As informações de 63.505 palavras e 328 páginas também foram sincronizadas no `llms.txt`. Qualquer futura edição dessas métricas precisa manter livro, site e esse arquivo em acordo.

## Protocolo obrigatório de revisão para pessoas e IAs

O objetivo é encontrar erros **antes** de atualizar site, EPUB, PDF e pacote KDP. Leia `01-PERSONAGENS/`, `02-ESTRUTURA/CRONOLOGIA.md` e `02-ESTRUTURA/ESTRUTURA_CAPITULOS.md` antes de editar. Os 40 arquivos de `03-MANUSCRITO/` são a fonte da narrativa; `manuscrito_completo.md`, leitor e arquivos de publicação são saídas geradas. Preserve a linguagem direta, a dignidade das personagens e o final deste volume: Camila solteira, feliz e inteira. Não insira uma lembrança ou um “primeiro” sem localizar a cena anterior que o sustenta. Não altere a trama para fabricar suspense; prefira pergunta legítima, decisão pendente ou consequência concreta. Não prometa que uma revisão automática prova perfeição literária.

### 1. Etapa pequena — frase, fala e parágrafo

Não trate preferências como erros: “com Camila” e “com a Camila” são construções válidas; a última foi escolhida nos convites à leitora pelo tom próximo. Não acrescente artigos em vocativos nem substitua todas as ocorrências de nomes automaticamente.

Trabalhe em um trecho por vez e releia o parágrafo anterior e o seguinte. Verifique ortografia, acentos, concordância, tempo verbal, pontuação de diálogo, sujeito de cada ação, referente de “ele/ela/eles/nós”, palavras faltando ou sobrando e imagens que geram outro sentido. Leia a fala em voz alta: a criança deve soar como criança; Camila e as demais mulheres devem falar de modo natural para o público, sem palavras que peçam dicionário. Corte repetição que não acrescente emoção. Sinalize palavras vagas ou rebuscadas para trocar por verbos e imagens concretas. Exemplo de regressão a impedir: “E Fi ficaram”, “ia atrás quinze minutos”, “fechou diário”, “caneta em riste”, “amava pequeno”, “ruptura”, “sobressaltada”.

### 2. Etapa média — cena e capítulo

Para **cada um dos 40 capítulos**, anote antes de editar: quando acontece (mês, dia da semana, tempo desde a saída de Ricardo), onde, quem está presente, onde dormem as crianças, idade delas, estado do dinheiro e do divórcio, o que Camila já sabe/faz, e qual fato muda até a última linha. Leia sem pular do começo ao fim. Cada mudança de lugar ou tempo precisa de ponte; uma personagem não pode estar no carro e no escritório ao mesmo tempo. Confira a ordem das ações, a voz dos diálogos, a lógica emocional, o ritmo no meio e a transição para o próximo capítulo. “Primeira vez” exige busca nos capítulos anteriores. Uma lembrança exige cena comprovável; no cap. 7 Léo **toca a testa febril da mãe**, mas **não acorda o pai**. Se um capítulo repetir um acontecimento, deve mostrar evolução, não apresentá-lo como inédito. Não encerre todos os capítulos com a mesma lição em outras palavras.

Use este mapa de verificação; não substitui a leitura integral de cada capítulo:

| Capítulos | Âncora a conferir | Risco principal |
| --- | --- | --- |
| 1–5 | rotina, 8º aniversário de Léo, tentativa de terapia, Fernanda | ordem janeiro; fatos lembrados depois |
| 6–10 | viagem, febre/leite, decisão, conversa com filhos, saída de Ricardo | Carnaval; Léo não acorda o pai; cap. 10 tem uma só primeira noite |
| 11–14 | advogada em março, contas em abril, família, primeira terapia | local de cada cena; dias e idades; terapia não pressupõe fala inexistente |
| 15–18 | visitas sem pernoite, primeiro fim de semana completo, pintura, pequenas vitórias | horário de trabalho; não repetir “primeira vez”; corte de cabelo antes do cap. 16 |
| 19–22 | trabalho, grupo, apresentação de Léo, Natal | apresentação precede a pergunta de dezembro; Ricardo não comparece |
| 23–26 | 9º aniversário, pergunta sobre o pai, kitnet de Ricardo, primeira exposição | casa do pai e sequência dos sábados; primeiro evento de arte |
| 27–30 | segunda exposição, Daniel, tentativa de Ricardo, divórcio, um ano | aproximação gradual; acordo e nome de Camila; um ano desde a saída |
| 31–34 | Dia das Mães, férias de julho, crianças conhecem Daniel, viagem | idade dos filhos; 11 anos são de casamento, não de maternidade |
| 35–38 | briga, presente, mãe de Daniel, conversa sobre ter filhos, reencontro com Ricardo | desejo de Daniel foi preparado antes; não resolver diferença por conveniência |
| 39–40 | diário, término respeitoso, exposição final, Joana | diário já foi aberto no 38; conversa no café é na semana seguinte; final sem novo romance |

### 3. Etapa grande — arcos e continuidade entre capítulos

Controle também a situação dos objetos e compromissos: quem já viu os quadros; quando o quadro vendido é retirado; quem prometeu passeio; onde estão carro, chaves e crianças; se uma mensagem pode ser privada e receber respostas ao mesmo tempo. Confira o dinheiro sem transformar o romance em conselho: 30% é o pedido/acordo desta família, não uma regra geral. Não confunda pensão dos filhos com parcela do imóvel. Não use uma frase carinhosa dos filhos como prova de que a separação não os afeta.

Compare pares de capítulos vizinhos **e** todos os capítulos que retomam um fato. Faça uma linha de eventos com evidência (capítulo e frase), sem deduzir que algo ocorreu fora da página só porque seria conveniente. A régua atual é: 3 anos de namoro + 11 de casamento; Léo completa 8 no cap. 2 e 9 no cap. 23; Bia tem 4 no início e 5 no segundo ano; Camila faz 35 na segunda quinzena de março do Ano 0 e 36 no Ano 1. Ricardo sai numa quinta-feira após duas semanas tensas; antes do cap. 16 as visitas das crianças são sem pernoite, depois começam fins de semana alternados. Camila trabalha durante a semana. O apart-hotel é temporário; antes do cap. 25 Ricardo já alugou uma kitnet. A primeira exposição é no cap. 26, a segunda no 27. Cap. 38 abre o diário; cap. 39 continua a leitura e, na semana seguinte, Camila termina com Daniel. Confira finanças, escola, asma/bombinha de Léo, terapia, arte, guarda, nomes, deslocamentos, estações e idades. Quando houver dúvida, corrija também `02-ESTRUTURA/CRONOLOGIA.md` ou registre a decisão pendente; não deixe dois cânones incompatíveis.

### 4. Etapa geral — leitura fria, site e publicação

Depois dos ajustes locais, releia o romance na ordem 1–40, incluindo carta, página bíblica inicial, agradecimentos e fecho. Faça duas passagens separadas: uma pela experiência da leitora (clareza, identificação, curiosidade, cenas sem pressa, final satisfatório) e outra técnica (fatos, links, artes, paginação, nome literário, metadados). Teste no leitor `ler.html` os botões anterior/próximo, índice, acesso direto por `?cap=`, retorno ao ponto salvo e principalmente **16→17 e 17→18 iniciando no topo**; teste celular e desktop. O leitor não deve guardar o livro inteiro offline. Execute `python tools/build_publication.py` e depois `python tools/validate_release.py`; confira o diff para impedir alterações acidentais e atualize contagem de palavras/páginas e a capa impressa se a lombada mudar. Abra o EPUB no Kindle Previewer e o PDF/capa no Previewer KDP; peça prova física antes de liberar o impresso. A aprovação final do texto precisa de leitura humana da equipe, não só dos scripts.

### Registro de achados e regra de conclusão

Além do validador, execute `python tools/inspect_publication.py --render`: compara o texto dos 40 capítulos com EPUB e PDF, verifica dimensões, fontes e margens e gera amostras para inspeção visual. Reexecute EPUBCheck após reconstruir; só depois refaça hashes e ZIP. Atualize `numberOfPages` e `wordCount` do site. Registre uma cópia identificada da edição e seu SHA-256 antes de enviá-la à equipe. Não declare verificação no Kindle Previewer ou prova física se apenas scripts foram executados.

Para cada problema, registre **capítulo + trecho + tipo** (linguagem, concordância, cronologia, continuidade, cena, ritmo, leitor/site ou publicação), o fato canônico, a correção e como foi conferida. Classifique como bloqueante (contradição factual, capítulo quebrado, arquivo fora de sincronia), importante (frase confusa, cena corrida, transição fraca) ou polimento (preferência de estilo). Depois de corrigir, releia a cena e os dois lados da transição; procure todas as outras menções do mesmo fato no repositório. Só considere a rodada encerrada quando não houver achado bloqueante conhecido, os testes passarem e as pendências subjetivas estiverem explicitadas para a equipe.

### GitHub ao concluir cada atualização

Em 29/09/2026, o autor autorizou manter este repositório atualizado ao finalizar o trabalho. Ao concluir alterações solicitadas no livro, validar e sincronizar as saídas, revisar o `git status`, separar arquivos não relacionados e fazer commit e push para `maykonlong/book`. Conferir o SHA remoto e, quando houver mudanças no leitor/site, o deploy do GitHub Pages. Nunca forçar push, sobrescrever trabalho remoto ou incluir credenciais/dados civis. Se faltar acesso ou houver conflito, preservar o trabalho e informar o impedimento. Essa autorização não publica o livro na Amazon e não abrange outros repositórios.

## Decisão comercial em aberto

O livro integral está disponível no leitor e nos arquivos deste repositório **público**. Não selecione KDP Select enquanto essa distribuição digital continuar. Para o lançamento, veja o [plano de prévia e venda](05-PUBLICACAO/PLANO_PREVIA_AMAZON_E_PRECO.md): ele é um plano futuro, não uma restrição já aplicada ao site. Retirar um botão do leitor não retira EPUB, manuscrito e histórico do Git do acesso público.

O nome literário público é Mariana Duarte. Os dados civis, fiscais e bancários devem ser inseridos somente nos canais apropriados da KDP e dos órgãos responsáveis, nunca neste repositório.
