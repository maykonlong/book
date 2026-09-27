# Leitor instalável

O site pode ser adicionado à tela inicial como um webapp. Ao tocar no ícone, ele abre `ler.html` e tenta retomar o capítulo e a posição guardados **neste navegador ou app**. Uma leitora nova começa pela capa e pela carta. O botão “Começar a ler” do site abre a capa; para quem já leu, a chamada principal passa a “Continuar de onde parei”, com opção de recomeçar.

O progresso usa `localStorage`, não conta de usuário. Não há sincronização entre celulares, navegadores ou perfis; a limpeza dos dados do site pode apagar o marcador.

O service worker (`sw.js`) guarda apenas `index.html`, `ler.html`, o manifesto e os ícones para o app abrir. **Nenhum capítulo, manuscrito, EPUB ou PDF é pré-carregado ou salvo pelo service worker.** O leitor busca cada arquivo de texto na rede com `cache: 'no-store'`. Sem internet, a estrutura pode abrir, mas a leitura mostra uma mensagem de conexão; o marcador continua no aparelho.

Para instalar, use o botão “Instalar o leitor” quando o navegador o oferecer. Em navegadores sem esse botão, use o menu “Instalar app” ou “Adicionar à Tela de Início”. A disponibilidade do comando depende do navegador e do aparelho.

Quando o site virar prévia para a Amazon, revisar também o leitor, os arquivos públicos e este service worker. O PWA não resolve, por si só, a distribuição integral já existente no repositório e no histórico.

## Teste de manutenção

1. Execute `python tools/build_pwa_icons.py` se alterar as cores ou o símbolo; os arquivos de 180, 192 e 512 px são versionados.
2. Execute `python tools/validate_release.py` e confira `manifest.json` e `sw.js` no navegador.
3. Num perfil novo, instale e abra pelo ícone: a capa deve aparecer. Avance, role o capítulo, feche e abra pelo ícone: o capítulo e a posição devem voltar.
4. Em modo offline, confirme que a estrutura mostra o aviso de conexão e que os caches do site não contêm arquivos de capítulos.
