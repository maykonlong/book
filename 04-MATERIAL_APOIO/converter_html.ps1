# Converte manuscrito_completo.md em um HTML limpo e formatado (para beta readers).
# Uso: abra o HTML no navegador e use "Imprimir > Salvar como PDF" para gerar o PDF.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$md = Get-Content (Join-Path $root 'manuscrito_completo.md') -Raw -Encoding UTF8

# Limpeza: remove referências de rodapé soltas e escapa caracteres HTML
$md = $md -replace '\[\^\d+\]', ''
$md = $md -replace '&', '&amp;'
$md = $md -replace '<', '&lt;'
$md = $md -replace '>', '&gt;'

# Converte marcação inline: **bold** e *itálico*
function Convert-Inline([string]$t) {
    $t = $t -replace '\*\*(.+?)\*\*', '<strong>$1</strong>'
    $t = $t -replace '\*(.+?)\*', '<em>$1</em>'
    return $t
}

# Processa linha a linha (títulos em linhas consecutivas são tratados separadamente)
$lines = $md -split "`r?`n"
$out = @()
$para = @()

foreach ($line in $lines) {
    $t = $line.TrimEnd("`r").Trim()
    if ($t -eq '') {
        if ($para.Count -gt 0) { $out += '<p>' + (Convert-Inline ($para -join ' ')) + '</p>'; $para = @() }
        continue
    }
    if ($t -eq '---') {
        if ($para.Count -gt 0) { $out += '<p>' + (Convert-Inline ($para -join ' ')) + '</p>'; $para = @() }
        $out += '<hr>'
        continue
    }
    if ($t -match '^# (.+)$') {
        if ($para.Count -gt 0) { $out += '<p>' + (Convert-Inline ($para -join ' ')) + '</p>'; $para = @() }
        $out += '<h1>' + (Convert-Inline $Matches[1]) + '</h1>'
        continue
    }
    if ($t -match '^## (.+)$') {
        if ($para.Count -gt 0) { $out += '<p>' + (Convert-Inline ($para -join ' ')) + '</p>'; $para = @() }
        $out += '<h2>' + (Convert-Inline $Matches[1]) + '</h2>'
        continue
    }
    if ($t -match '^&gt;\s*(.*)$') {
        if ($para.Count -gt 0) { $out += '<p>' + (Convert-Inline ($para -join ' ')) + '</p>'; $para = @() }
        $out += '<blockquote>' + (Convert-Inline $Matches[1]) + '</blockquote>'
        continue
    }
    $para += $t
}
if ($para.Count -gt 0) { $out += '<p>' + (Convert-Inline ($para -join ' ')) + '</p>' }

$body = ($out -join "`n")

$html = @"
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>A Metade Que Me Faltava Era Eu</title>
<style>
body { font-family: Georgia, 'Times New Roman', serif; max-width: 42em; margin: 2em auto; padding: 0 1.5em; line-height: 1.75; color: #1a1a1a; }
h1 { font-size: 2em; text-align: center; margin: 1em 0 0.4em; line-height: 1.3; }
h2 { font-size: 1.35em; margin-top: 2.4em; margin-bottom: 0.6em; }
p { margin: 0 0 1em; text-align: justify; }
hr { border: none; text-align: center; margin: 2.2em auto; }
hr::before { content: '* * *'; color: #999; letter-spacing: 0.6em; }
blockquote { font-style: italic; color: #444; margin: 1.6em 2em; }
em { font-style: italic; }
strong { font-weight: bold; }
</style>
</head>
<body>
$body
</body>
</html>
"@

$outPath = Join-Path $root '05-PUBLICACAO\manuscrito_beta.html'
Set-Content -Path $outPath -Value $html -Encoding UTF8
Write-Output ("OK: " + $outPath)
Write-Output ("Tamanho: " + (Get-Item $outPath).Length + " bytes")

