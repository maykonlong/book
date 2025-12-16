@echo off
title Servidor de Edição do Livro
cd /d "%~dp0"
cls

:: -------------------------------
:: 1️⃣ Libera a porta 8000 (se houver)
:: -------------------------------
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo [INFO] Encerrando processo que usa a porta 8000 (PID=%%a)...
    taskkill /F /PID %%a >nul 2>&1
)

:: -------------------------------
:: 2️⃣ Mata processos ngrok “presos”
:: -------------------------------
echo [INFO] Verificando processos ngrok...
tasklist /FI "IMAGENAME eq ngrok.exe" | find /I "ngrok.exe" >nul
if not errorlevel 1 (
    echo [INFO] Encerrando processos ngrok existentes...
    taskkill /F /IM ngrok.exe >nul 2>&1
)

:: -------------------------------
:: 3️⃣ Inicia o servidor Python
:: -------------------------------
echo [INFO] Iniciando servidor local...
start "" "http://localhost:8000"
python server.py
if errorlevel 1 (
    echo [ERRO] Falha ao iniciar o servidor Python. Verifique se o Python está instalado e no PATH.
    pause
    exit /b 1
)

:: -------------------------------
:: 4️⃣ Inicia o ngrok (se ainda não houver sessão)
:: -------------------------------
echo [INFO] Iniciando Ngrok...
start "" ngrok http 8000

pause
