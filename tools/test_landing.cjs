// Testes locais, sem navegador, rede, alterações no marcador ou bibliotecas externas.
// Rode: node tools/test_landing.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(scripts.length, 1, 'Uma única lógica de interação na landing');
const code = scripts[0][1];
const schema = JSON.parse(html.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/)[1]);
let passed = 0;
function check(name, fn) { fn(); passed++; console.log('OK ' + name); }
const clean = (text) => text.replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();

check('Todos os destinos internos existem, sem IDs duplicados', () => {
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((m) => m[1]);
  assert.equal(ids.length, new Set(ids).size);
  for (const match of html.matchAll(/href="#([^"]+)"/g)) assert(ids.includes(match[1]), match[1]);
});
check('Trecho vem logo depois da abertura; 13 temas preservados', () => {
  const sections = [...html.matchAll(/<section\b[^>]*>/g)].map((m) => m[0]);
  assert(sections[0].includes('id="inicio"'));
  assert(sections[1].includes('id="trecho"'));
  assert.equal((html.match(/<li class="inside-card">/g) || []).length, 13);
  assert(html.includes('<details class="themes-more">'));
});
check('Todas as perguntas e respostas visíveis correspondem ao JSON-LD', () => {
  const visible = [...html.matchAll(/<details><summary>(.*?)<\/summary><p>(.*?)<\/p><\/details>/g)];
  const structured = schema['@graph'].find((n) => n['@type'] === 'FAQPage').mainEntity;
  assert.equal(visible.length, structured.length);
  visible.forEach((m, i) => {
    assert.equal(clean(m[1]), structured[i].name);
    assert.equal(clean(m[2]), structured[i].acceptedAnswer.text);
  });
});
check('Citação da landing é fiel ao capítulo 7', () => {
  const quote = html.match(/<blockquote>\s*<p>(.*?)<\/p>/s)[1];
  const plain = clean(quote).replace(/&quot;/g, '"').replace(/^[“]|[”]$/g, '');
  const chapter = clean(fs.readFileSync(path.join(root, '03-MANUSCRITO/CAP_07_A_GOTA_DAGUA.md'), 'utf8'));
  assert(chapter.includes(plain));
});
check('Capas e artes leves, com dimensões e carregamento adequado', () => {
  const images = [...html.matchAll(/<img\b[^>]+>/g)].map((m) => m[0]);
  assert.equal(images.length, 3);
  let bytes = 0;
  images.forEach((image, i) => {
    assert(/width="\d+"/.test(image) && /height="\d+"/.test(image));
    assert(/alt="[^"]+"/.test(image));
    assert(i === 0 ? image.includes('fetchpriority="high"') : image.includes('loading="lazy"'));
    bytes += fs.statSync(path.join(root, image.match(/src="\.\/([^"]+)"/)[1])).size;
  });
  assert(bytes < 750000, 'Orçamento total das imagens da landing');
});
check('Dados de palavras/páginas sincronizados também no llms.txt', () => {
  const book = schema['@graph'].find((n) => n['@type'] === 'Book');
  const llms = fs.readFileSync(path.join(root, 'llms.txt'), 'utf8');
  assert(llms.includes(book.wordCount.toLocaleString('pt-BR') + ' palavras'));
  assert(llms.includes(book.numberOfPages + ' páginas'));
  assert(llms.includes('ler.html?inicio=1'));
});
check('Sem scripts de terceiros, rastreadores ou cache do romance', () => {
  assert(!/<script[^>]+src="https?:/i.test(html));
  assert(!code.includes('localStorage.setItem'));
  const worker = fs.readFileSync(path.join(root, 'sw.js'), 'utf8');
  const cached = worker.match(/const SHELL_FILES = \[([\s\S]*?)\];/)[1];
  assert(!/03-MANUSCRITO|\.md|\.epub|\.pdf/.test(cached));
});

function makeApp(options = {}) {
  const events = new Map();
  function element(label) {
    return { hidden: true, textContent: '', href: './ler.html?inicio=1', disabled: false,
      dataset: { resumeLabel: label || 'Continuar leitura' },
      querySelector() { return null; },
      addEventListener(type, callback) { events.set(this.id + ':' + type, callback); },
      focus() { this.focused = true; }, select() { this.selected = true; } };
  }
  const ids = {};
  ['secondary-read', 'resume-note', 'mobile-read', 'share-book', 'share-status', 'share-fallback', 'share-url'].forEach((id) => { ids[id] = element(); ids[id].id = id; });
  const primary = element('Continuar de onde parei');
  const links = [primary, ids['mobile-read'], element('Continuar')];
  let copied = null;
  let shareCall = null;
  const box = { heroBottom: 600, closingTop: 5000 };
  const hero = { getBoundingClientRect: () => ({ bottom: box.heroBottom }) };
  const closing = { getBoundingClientRect: () => ({ top: box.closingTop }) };
  const browserEvents = {};
  const observers = [];
  const fakeWindow = { innerHeight: 844, isSecureContext: options.secure !== false,
    addEventListener(type, handler) { browserEvents[type] = handler; } };
  function Observer(callback) { observers.push(callback); this.observe = () => {}; }
  if (!options.noObserver) fakeWindow.IntersectionObserver = Observer;
  const navigator = {};
  if (!options.noClipboard) navigator.clipboard = { async writeText(value) {
    if (options.clipboardDenied) throw new Error('permission denied');
    copied = value;
  } };
  if (options.nativeShare) navigator.share = async (value) => {
    shareCall = value;
    if (options.shareError) { const error = new Error('share failed'); error.name = options.shareError; throw error; }
  };
  const storage = options.storage || {};
  const context = vm.createContext({ window: fakeWindow, navigator, IntersectionObserver: Observer,
    localStorage: { getItem(key) { if (options.storageBlocked) throw new Error('blocked'); return storage[key] || null; } },
    document: { getElementById(id) { assert(ids[id], id); return ids[id]; },
      querySelectorAll(selector) { assert.equal(selector, '[data-read-link]'); return links; },
      querySelector(selector) { if (selector === '.hero') return hero; if (selector === '.final-section') return closing; throw new Error(selector); } } });
  vm.runInContext(code, context, { timeout: 1000 });
  return { ids, primary, links, box, browserEvents, observers,
    clickShare: () => events.get('share-book:click')(), copied: () => copied, shared: () => shareCall };
}
const v2 = 'metade-leitor-progresso-v2';
const v1 = 'metade-leitor-progresso-v1';
check('Nova visitante começa na capa; não recebe marcador inexistente', () => {
  const app = makeApp();
  assert.equal(app.primary.href, './ler.html?inicio=1');
  assert(app.ids['resume-note'].hidden);
  assert(app.ids['mobile-read'].hidden);
});
for (const [c, label] of [[0,'páginas iniciais'],[1,'páginas iniciais'],[2,'capítulo 1'],[19,'capítulo 18'],[41,'capítulo 40'],[42,'páginas finais'],[44,'páginas finais']]) {
  check('Marcador v2 ' + c + ' retoma ' + label, () => {
    const app = makeApp({ storage: { [v2]: JSON.stringify({ c, y: 1200 }) } });
    assert(app.links.every((a) => a.href === './ler.html'));
    assert(app.ids['resume-note'].textContent.includes(label));
    assert.equal(app.ids['secondary-read'].href, './ler.html?inicio=1');
  });
}
check('Marcador legado usa o capítulo correto sem gravar dados', () => {
  const app = makeApp({ storage: { [v1]: JSON.stringify({ c: 18 }) } });
  assert(app.ids['resume-note'].textContent.includes('capítulo 18'));
});
check('V2 válido tem prioridade sobre marcador antigo', () => {
  const app = makeApp({ storage: { [v1]: '{"c":6}', [v2]: '{"c":19}' } });
  assert(app.ids['resume-note'].textContent.includes('capítulo 18'));
});
check('Voltar pelo histórico atualiza o marcador sem recarregar a landing', () => {
  const storage = {};
  const app = makeApp({ storage });
  storage[v2] = '{"c":19}';
  app.browserEvents.pageshow();
  assert.equal(app.primary.href, './ler.html');
  assert(app.ids['resume-note'].textContent.includes('capítulo 18'));
});
check('Avanço em outra aba e limpeza de dados atualizam os botões', () => {
  const storage = { [v2]: '{"c":2}' };
  const app = makeApp({ storage });
  storage[v2] = '{"c":6}';
  app.browserEvents.storage({ key: v2 });
  assert(app.ids['resume-note'].textContent.includes('capítulo 5'));
  delete storage[v2];
  app.browserEvents.storage({ key: null });
  assert.equal(app.primary.href, './ler.html?inicio=1');
  assert(app.ids['resume-note'].hidden);
  assert.equal(app.ids['secondary-read'].href, '#historia');
});
for (const invalid of ['{', 'null', '[]', '{"c":45}', '{"c":-1}', '{"c":"3"}', '{"c":2.5}']) {
  check('Marcador inválido não impede a leitura: ' + invalid, () => {
    const app = makeApp({ storage: { [v2]: invalid } });
    assert.equal(app.primary.href, './ler.html?inicio=1');
    assert(app.ids['resume-note'].hidden);
  });
}
check('Armazenamento bloqueado mantém página e indicação funcionais', () => {
  const app = makeApp({ storageBlocked: true });
  assert.equal(app.primary.href, './ler.html?inicio=1');
  assert(!app.ids['share-book'].hidden);
});
for (const noObserver of [false, true]) check('Botão móvel acompanha a rolagem' + (noObserver ? ' sem IntersectionObserver' : ''), () => {
  const app = makeApp({ noObserver });
  const update = noObserver ? app.browserEvents.scroll : app.observers[0];
  assert(app.ids['mobile-read'].hidden);
  app.box.heroBottom = -10;
  update(); assert(!app.ids['mobile-read'].hidden);
  app.box.closingTop = 500;
  update(); assert(app.ids['mobile-read'].hidden);
  app.box.heroBottom = 500;
  update(); assert(app.ids['mobile-read'].hidden);
});

(async () => {
  for (const options of [{}, {nativeShare:true}, {nativeShare:true, shareError:'AbortError'}, {nativeShare:true, shareError:'NotAllowedError'}, {clipboardDenied:true}, {noClipboard:true}, {secure:false}]) {
    const app = makeApp(options);
    assert.equal(app.copied(), null, 'Nunca compartilha ao carregar');
    assert.equal(app.shared(), null);
    await app.clickShare();
    assert.equal(app.ids['share-book'].disabled, false);
    if (options.shareError === 'AbortError') {
      assert.equal(app.copied(), null);
      assert(app.ids['share-status'].hidden);
    } else if (options.nativeShare && !options.shareError) {
      assert.equal(app.shared().url, 'https://maykonlong.github.io/book/');
    } else if (options.clipboardDenied || options.noClipboard || options.secure === false) {
      assert(!app.ids['share-fallback'].hidden);
      assert(app.ids['share-url'].focused && app.ids['share-url'].selected);
    } else {
      assert.equal(app.copied(), 'https://maykonlong.github.io/book/');
      assert(!app.ids['share-status'].hidden);
    }
    passed++; console.log('OK Compartilhamento simulado: ' + JSON.stringify(options));
  }
  console.log('\n' + passed + ' verificações da landing aprovadas. Compartilhamento testado com simulações, sem enviar mensagens.');
})().catch((error) => { console.error(error); process.exitCode = 1; });
