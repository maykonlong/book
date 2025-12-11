$files = Get-ChildItem "c:\Users\Acer\Projetos\Book\1\03-MANUSCRITO\CAP_*.md" | Sort-Object Name
$chaptersList = [System.Collections.Generic.List[Object]]::new()

foreach ($file in $files) {
    # Ler conteúdo como string única
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    
    # Extrair título (segunda linha ou padrão)
    $lines = $content -split "`r`n"
    $title = "Capítulo"
    
    # Tenta achar linha com ##
    foreach ($line in $lines) {
        if ($line.Trim().StartsWith("## ")) {
            $title = $line.Replace("##", "").Trim()
            break
        }
    }
    # Se não achou, tenta primeira linha com #
    if ($title -eq "Capítulo") {
        foreach ($line in $lines) {
            if ($line.Trim().StartsWith("# ")) {
                $title = $line.Replace("#", "").Trim()
                break
            }
        }
    }

    # Criar objeto limpo
    $obj = [PSCustomObject]@{
        id = $file.BaseName
        title = $title
        content = $content
    }
    
    $chaptersList.Add($obj)
}

# Converter para JSON
$json = $chaptersList | ConvertTo-Json -Depth 2

# Criar string JS
$jsContent = "const bookData = $json;"

# Salvar com UTF8 NO BOM (importante para web)
[System.IO.File]::WriteAllText("c:\Users\Acer\Projetos\Book\1\js\book-content.js", $jsContent, [System.Text.Encoding]::UTF8)

Write-Host "Gerado com sucesso: " $chaptersList.Count " capítulos."
