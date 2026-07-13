#!/bin/bash

cd "/home/seletor/Projeto PDAD"

echo "=== Testador de Versões PDAD ==="
echo ""
echo "1) ProjetoPdad2GCC.py"
echo "2) ProjetoPdadCC.py"
echo "3) ProjetoPdadGCC1.py"
echo "4) ProjPDADF.py"
echo "5) PDADPerf.py"
echo "6) PDADPerfB.py"
echo "7) PDADGFQ.py"
echo "8) PDADG.py"
echo "0) Sair"
echo ""
read -p "Escolha uma opção (1-8 ou 0): " opcao

case $opcao in
    1) SCRIPT="ProjetoPdad2GCC.py" ;;
    2) SCRIPT="ProjetoPdadCC.py" ;;
    3) SCRIPT="ProjetoPdadGCC1.py" ;;
    4) SCRIPT="ProjPDADF.py" ;;
    5) SCRIPT="PDADPerf.py" ;;
    6) SCRIPT="PDADPerfB.py" ;;
    7) SCRIPT="PDADGFQ.py" ;;
    8) SCRIPT="PDADG.py" ;;
    *) echo "Saindo..."; exit 0 ;;
esac

echo ""
echo "🐍 Usando ambiente virtual existente (.venv)..."
echo "🚀 Executando $SCRIPT ..."
echo "=================================================="

if [ -f "$SCRIPT" ]; then
    .venv/bin/python "$SCRIPT"
else
    echo "❌ Erro: Arquivo $SCRIPT não encontrado!"
fi
