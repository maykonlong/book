// Função de inicialização
const startApp = () => {
    // Evita inicialização duplicada se o evento disparar depois
    if (window.appInitialized) return;
    window.appInitialized = true;

    // --- ESTADO GLOBAL ---
    let state = {
        currentChapter: 0,
        currentScroll: 0,
        theme: 'light',
        fontSize: 18,
        fontFamily: 'sans'
    };

    // --- ELEMENTOS ---
    const els = {
        container: document.getElementById('reader-container'),
        content: document.getElementById('content'),
        headerTitle: document.getElementById('chapter-title'),
        sidebar: document.getElementById('sidebar'),
        overlay: document.getElementById('overlay'),
        chapterList: document.getElementById('chapter-list'),
        statusStats: document.getElementById('status-stats'),
        statusPage: document.getElementById('status-page'),
        settingsModal: document.getElementById('settings-modal'),
        btnMenu: document.getElementById('menu-btn'),
        btnSettings: document.getElementById('settings-btn'),
        btnCloseSidebar: document.getElementById('close-sidebar'),

        // Settings
        btnsTheme: document.querySelectorAll('.theme-btn'),
        rngFont: document.getElementById('font-size-range'),
        lblFontVal: document.getElementById('font-val'),
        selFont: document.getElementById('font-family-select')
    };

    // --- INICIALIZAÇÃO ---
    function init() {
        // Verifica se é a primeira vez (antes de carregar o estado)
        const isFirstAccess = !localStorage.getItem('lume_scroll_simple');

        loadState();
        applySettings();
        buildSidebar();

        renderChapter(state.currentChapter).then(() => {
            setTimeout(() => {
                restorePosition();
                updateStatus();

                // Se for primeiro acesso, abre as configurações para boas-vindas
                if (isFirstAccess) {
                    setTimeout(() => {
                        els.settingsModal.classList.add('open');
                        els.overlay.classList.add('visible');
                    }, 800);
                }
            }, 150);
        });

        setupListeners();
    }

    // --- RENDERIZAÇÃO ---
    async function renderChapter(index) {
        if (!bookData || !bookData[index]) return;

        els.content.style.opacity = '0';
        els.container.scrollTop = 0;

        const title = bookData[index].title || `Capítulo ${index + 1}`;
        els.headerTitle.textContent = title;

        let md = bookData[index].content;
        let html = marked.parse(md);

        // Nav Buttons
        let navHtml = '<div class="chapter-nav">';
        if (index > 0) {
            navHtml += `<button class="nav-internal-btn" id="btn-prev-chap">← Capítulo Anterior</button>`;
        }
        if (index < bookData.length - 1) {
            const nextTitle = bookData[index + 1].title ? bookData[index + 1].title.substring(0, 20) + '...' : 'Próximo';
            navHtml += `<button class="nav-internal-btn" style="font-weight:600" id="btn-next-chap">Próximo: ${nextTitle} →</button>`;
        } else {
            navHtml += `<div style="font-style:italic; opacity:0.7; margin-top:20px;">Fim do Livro</div>`;
        }
        navHtml += '</div>';

        els.content.innerHTML = html + navHtml;

        if (els.statusStats) updateStats(md);

        const btnPrev = document.getElementById('btn-prev-chap');
        if (btnPrev) btnPrev.onclick = () => changeChapter(index - 1);

        const btnNext = document.getElementById('btn-next-chap');
        if (btnNext) btnNext.onclick = () => changeChapter(index + 1);

        state.currentChapter = index;
        saveState();
        updateMenu();

        await waitForImages();

        els.content.style.opacity = '1';
    }

    function changeChapter(newIndex) {
        state.currentChapter = newIndex;
        state.currentScroll = 0;
        renderChapter(newIndex);
    }

    // --- UTILS ---
    function updateStats(text) {
        const clean = text.replace(/[#*_`]/g, '').trim();
        const words = clean.split(/\s+/).length;
        const chars = clean.length;
        const pags = Math.ceil(chars / 1500);
        els.statusStats.textContent = `${words} palavras • ${chars} carac. • ~${pags} págs impressas`;
    }

    function updateStatus() {
        if (els.statusPage) {
            const scrollTop = els.container.scrollTop;
            const scrollHeight = els.container.scrollHeight - els.container.clientHeight;
            const pct = scrollHeight > 0 ? Math.round((scrollTop / scrollHeight) * 100) : 0;
            els.statusPage.textContent = `${pct}%`;
        }
    }

    // --- LISTENERS ---
    function setupListeners() {
        els.btnMenu.onclick = () => { els.sidebar.classList.add('open'); els.overlay.classList.add('visible'); };
        els.btnCloseSidebar.onclick = () => { els.sidebar.classList.remove('open'); els.overlay.classList.remove('visible'); };
        els.overlay.onclick = () => {
            els.sidebar.classList.remove('open');
            els.settingsModal.classList.remove('open');
            els.overlay.classList.remove('visible');
        };
        els.btnSettings.onclick = () => {
            els.settingsModal.classList.toggle('open');
            if (els.settingsModal.classList.contains('open')) els.overlay.classList.add('visible');
            else els.overlay.classList.remove('visible');
        };

        els.container.addEventListener('scroll', () => {
            savePosition();
            updateStatus();
        });

        els.btnsTheme.forEach(btn => btn.onclick = () => {
            state.theme = btn.dataset.theme;
            applySettings();
            saveState();
        });

        els.rngFont.oninput = (e) => {
            state.fontSize = e.target.value;
            applySettings();
        };
        els.rngFont.onchange = () => saveState();

        if (els.selFont) {
            els.selFont.onchange = (e) => {
                state.fontFamily = e.target.value;
                applySettings();
                saveState();
            };
        }
    }

    // --- STATE ---
    function saveState() { localStorage.setItem('lume_scroll_simple', JSON.stringify(state)); }
    function loadState() {
        try {
            const saved = JSON.parse(localStorage.getItem('lume_scroll_simple'));
            if (saved) state = { ...state, ...saved };
        } catch (e) { }
    }

    function savePosition() {
        state.currentScroll = els.container.scrollTop;
        if (state.currentScroll < 0) state.currentScroll = 0;
    }

    function restorePosition() {
        els.container.scrollTop = state.currentScroll;
    }

    function applySettings() {
        document.documentElement.setAttribute('data-theme', state.theme);

        els.btnsTheme.forEach(btn => {
            if (btn.dataset.theme === state.theme) btn.classList.add('active');
            else btn.classList.remove('active');
        });

        document.documentElement.style.setProperty('--font-size', state.fontSize + 'px');
        els.rngFont.value = state.fontSize;
        if (els.lblFontVal) els.lblFontVal.textContent = state.fontSize;

        const f = state.fontFamily === 'serif' ? 'var(--font-serif)' : 'var(--font-sans)';
        document.documentElement.style.setProperty('--current-font', f);
        if (els.selFont) els.selFont.value = state.fontFamily;
    }

    function updateMenu() {
        document.querySelectorAll('.chapter-item').forEach((li, i) => {
            if (i === state.currentChapter) li.classList.add('active');
            else li.classList.remove('active');
        });
    }

    function buildSidebar() {
        els.chapterList.innerHTML = '';
        bookData.forEach((cap, i) => {
            const li = document.createElement('li');
            li.className = 'chapter-item';
            li.textContent = cap.title;
            li.onclick = () => {
                changeChapter(i);
                els.sidebar.classList.remove('open');
                els.overlay.classList.remove('visible');
            };
            els.chapterList.appendChild(li);
        });
    }

    function waitForImages() {
        return Promise.all(Array.from(document.images).map(img => {
            if (img.complete) return Promise.resolve();
            return new Promise(resolve => { img.onload = img.onerror = resolve; });
        }));
    }

    // Start
    init();
};

// Verifica se o DOM já está pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', startApp);
} else {
    startApp();
}
