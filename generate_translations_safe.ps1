# generate_translations_safe.ps1
# This script creates language folders (English, Spanish, French) and copies all markdown chapters
# from the original Portuguese folder (03-MANUSCRITO) into each folder, prefixing a placeholder
# header that indicates a translation is needed. It avoids interactive prompts and excessive output
# to prevent the Antigravity environment from hanging.

$src = "c:\Users\Acer\Projetos\Book\1\03-MANUSCRITO"

$langs = @(
    @{ Name = "manuscrito_ingles"; Header = "# English version - translation needed" },
    @{ Name = "manuscrito_espanhol"; Header = "# Versión en español - traducción necesaria" },
    @{ Name = "manuscrito_frances"; Header = "# Version française - traduction nécessaire" }
)

foreach ($lang in $langs) {
    $dst = Join-Path "c:\Users\Acer\Projetos\Book\1" $lang.Name
    if (-not (Test-Path $dst)) { New-Item -ItemType Directory -Path $dst | Out-Null }
    Get-ChildItem -Path $src -Filter "*.md" | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $newContent = "$($lang.Header)`n`n$content"
        $targetFile = Join-Path $dst $_.Name
        Set-Content -Path $targetFile -Value $newContent -Encoding utf8 -Force
    }
}

# No console output to avoid blocking the monitoring process.
