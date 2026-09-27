(function () {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('./sw.js').catch(function () {
        // O site continua utilizável quando o navegador não permite a instalação.
      });
    });
  }

  var installPrompt = null;
  var installButton = null;

  window.addEventListener('beforeinstallprompt', function (event) {
    event.preventDefault();
    installPrompt = event;
    if (installButton) installButton.hidden = false;
  });

  window.addEventListener('appinstalled', function () {
    installPrompt = null;
    if (installButton) installButton.hidden = true;
  });

  document.addEventListener('DOMContentLoaded', function () {
    installButton = document.getElementById('install-app');
    if (!installButton) return;
    installButton.hidden = !installPrompt;
    installButton.addEventListener('click', async function () {
      if (!installPrompt) return;
      var pending = installPrompt;
      installPrompt = null;
      installButton.hidden = true;
      await pending.prompt();
    });
  });
}());
