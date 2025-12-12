$map = @{
    'you' = 'você'; 'You' = 'Você'; 'your' = 'seu'; 'Your' = 'Seu';
    'woman' = 'mulher'; 'Woman' = 'Mulher'; 'man' = 'homem'; 'Man' = 'Homem';
    'child' = 'criança'; 'Child' = 'Criança'; 'kids' = 'filhos'; 'Kids' = 'Filhos';
    'mother' = 'mãe'; 'Mother' = 'Mãe'; 'father' = 'pai'; 'Father' = 'Pai';
    'divorce' = 'divórcio'; 'Divorce' = 'Divórcio';
    "I'm" = 'eu estou'; 'I am' = 'eu sou';
    'sorry' = 'desculpa'; 'Sorry' = 'Desculpa';
    'okay' = 'tudo bem'; 'Okay' = 'Tudo bem';
    'thanks' = 'obrigada'; 'Thanks' = 'Obrigada';
    'please' = 'por favor'; 'Please' = 'Por favor';
    'yes' = 'sim'; 'Yes' = 'Sim';
    'no' = 'não'; 'No' = 'Não'
}
Get-ChildItem -Path . -Recurse -Filter *.md | ForEach-Object {
    $content = Get-Content $_ -Raw -Encoding utf8
    foreach ($k in $map.Keys) {
        $pattern = "\\b$k\\b"
        $content = $content -replace $pattern, $map[$k]
    }
    Set-Content -Path $_ -Value $content -Encoding utf8
}
