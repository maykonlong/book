# PowerShell script to generate language versions of the manuscript
# This script creates three folders (manuscrito_inglês, manuscrito_espanhol, manuscrito_frances)
# and copies each chapter file from the original Portuguese folder (03-MANUSCRITO) into them.
# For each copy it adds a simple placeholder header indicating that the content should be translated.
# The original Portuguese files remain untouched.

$sourceDir = "c:\Users\Acer\Projetos\Book\1\03-MANUSCRITO"
$targetLangs = @(
    @{ Name = "manuscrito_inglês"; Header = "# English version – translation needed" },
    @{ Name = "manuscrito_espanhol"; Header = "# Versión en español – traducción necesaria" },
    @{ Name = "manuscrito_frances"; Header = "# Version française – traduction nécessaire" }
)

foreach ($lang in $targetLangs) {
    $targetDir = Join-Path "c:\Users\Acer\Projetos\Book\1" $lang.Name
    if (-not (Test-Path $targetDir)) { New-Item -ItemType Directory -Path $targetDir | Out-Null }
    Get-ChildItem -Path $sourceDir -Filter "*.md" | ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        $newContent = "$($lang.Header)`n`n$content"
        $targetFile = Join-Path $targetDir $_.Name
        Set-Content -Path $targetFile -Value $newContent -Encoding utf8
    }
}

Write-Host "Folders created and placeholder files generated. Replace the placeholder headers with actual translations when ready."
