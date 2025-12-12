# replace_pt2.ps1
# PowerShell script to replace common English words with Portuguese equivalents
# in all markdown files under the Portuguese manuscript folder (03-MANUSCRITO).
# Uses case‑insensitive regex so we don't need separate capitalized keys.

$folder = Join-Path -Path $PSScriptRoot -ChildPath '03-MANUSCRITO'

$map = @{
    'you'     = 'você'
    'your'    = 'seu'
    'woman'   = 'mulher'
    'man'     = 'homem'
    'child'   = 'criança'
    'kids'    = 'filhos'
    'mother'  = 'mãe'
    'father'  = 'pai'
    'divorce' = 'divórcio'
    "I'm"     = 'eu estou'
    'I am'    = 'eu sou'
    'sorry'   = 'desculpa'
    'okay'    = 'tudo bem'
    'thanks'  = 'obrigada'
    'please'  = 'por favor'
    'yes'     = 'sim'
    'no'      = 'não'
}

Get-ChildItem -Path $folder -Recurse -Filter *.md | ForEach-Object {
    $content = Get-Content $_ -Raw -Encoding utf8
    foreach ($k in $map.Keys) {
        $pattern = "(?i)\\b$([regex]::Escape($k))\\b"
        $content = $content -replace $pattern, $map[$k]
    }
    Set-Content -Path $_ -Value $content -Encoding utf8
}
