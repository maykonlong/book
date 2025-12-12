# Script to generate book-content-{lang}.js files for each language
# Reads .md files from each manuscript folder and generates a JS file

param(
    [string]$Language = "all"  # pt, en, es, fr, or all
)

function ConvertTo-JsonEscaped {
    param([string]$text)
    
    # Escape special characters for JSON
    $text = $text -replace '\\', '\\'
    $text = $text -replace '"', '\"'
    $text = $text -replace "`r`n", '\r\n'
    $text = $text -replace "`n", '\n'
    $text = $text -replace "`t", '\t'
    
    return $text
}

function Generate-BookContent {
    param(
        [string]$Lang,
        [string]$FolderPath,
        [string]$OutputFile
    )
    
    Write-Host "Generating $OutputFile for language $Lang..." -ForegroundColor Cyan
    
    # Get all .md files sorted
    $files = Get-ChildItem -Path $FolderPath -Filter "*.md" | Sort-Object Name
    
    if ($files.Count -eq 0) {
        Write-Host "WARNING: No .md files found in $FolderPath" -ForegroundColor Yellow
        return
    }
    
    # Start JS file
    $jsContent = "const bookData = [`r`n"
    
    foreach ($file in $files) {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        
        # Extract title from first ## in file
        $titleMatch = [regex]::Match($content, '##\s+(.+)')
        $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value.Trim() } else { $file.BaseName }
        
        # Escape content for JSON
        $escapedContent = ConvertTo-JsonEscaped -text $content
        
        # Add to JS array
        $jsContent += "    {`r`n"
        $jsContent += "        `"id`": `"$($file.BaseName)`",`r`n"
        $jsContent += "        `"title`": `"$title`",`r`n"
        $jsContent += "        `"content`": `"$escapedContent`"`r`n"
        $jsContent += "    },`r`n"
    }
    
    # Remove last comma and close array
    $jsContent = $jsContent.TrimEnd(",`r`n") + "`r`n];`r`n"
    
    # Save file
    $jsContent | Out-File -FilePath $OutputFile -Encoding UTF8 -NoNewline
    
    Write-Host "Generated: $OutputFile with $($files.Count) chapters" -ForegroundColor Green
}

# Language configuration
$languages = @{
    "pt" = @{
        folder = "03-MANUSCRITO"
        output = "js\book-content-pt.js"
    }
    "en" = @{
        folder = "manuscrito_ingles"
        output = "js\book-content-en.js"
    }
    "es" = @{
        folder = "manuscrito_espanhol"
        output = "js\book-content-es.js"
    }
    "fr" = @{
        folder = "manuscrito_frances"
        output = "js\book-content-fr.js"  
    }
}

# Determine which languages to process
$langsToProcess = if ($Language -eq "all") {
    $languages.Keys
}
else {
    @($Language)
}

# Process each language
foreach ($lang in $langsToProcess) {
    if ($languages.ContainsKey($lang)) {
        $config = $languages[$lang]
        $folderPath = Join-Path $PSScriptRoot $config.folder
        $outputPath = Join-Path $PSScriptRoot $config.output
        
        if (Test-Path $folderPath) {
            Generate-BookContent -Lang $lang -FolderPath $folderPath -OutputFile $outputPath
        }
        else {
            Write-Host "ERROR: Folder not found: $folderPath" -ForegroundColor Red
        }
    }
    else {
        Write-Host "ERROR: Invalid language: $lang" -ForegroundColor Red
    }
}

Write-Host "Done!" -ForegroundColor Green
