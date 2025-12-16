@echo off
title Servidor do Livro
cd /d "%~dp0"
cls
echo ==========================================
echo      SERVIDOR DE EDICAO DO LIVRO
echo ==========================================
echo.
echo [INFO] Iniciando servidor local...
echo [INFO] Acesso: http://localhost:8000
echo.
echo DICA: Para compartilhar com outros, use um tunel como ngrok
echo       Exemplo: ngrok http 8000
echo.
echo Pressione CTRL+C para parar o servidor.
echo.

:: Abre o navegador localmente
start "" "http://localhost:8000"

:: Inicia o Tunel Ngrok (Acesso Externo)
echo [INFO] Iniciando Ngrok...
start "Ngrok Tunnel" cmd /k "ngrok http 8000"

:: Inicia o servidor Python (Servidor Principal)
echo [INFO] Iniciando Servidor Python...
python server.py
pause
