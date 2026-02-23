#!/bin/bash

# DEMO: Memory Bridge Pattern Learning
# Simula execuções de comando e mostra aprendizado

set -e

echo "🧠 MEMORY BRIDGE LEARNING DEMO"
echo "=============================="
echo ""

MEMORY_DIR=".aios-core/core/synapse/memory"

echo "1️⃣  Registrando padrão de desenvolvimento..."
node "$MEMORY_DIR/local-memory-bridge.js" record "*task" "@dev" 
node "$MEMORY_DIR/local-memory-bridge.js" record "*run-lint" "@dev"
node "$MEMORY_DIR/local-memory-bridge.js" record "*test" "@dev"
sleep 1
echo "✓ 3 comandos registrados"
echo ""

echo "2️⃣  Registrando padrão de QA..."
node "$MEMORY_DIR/local-memory-bridge.js" record "*test" "@qa"
node "$MEMORY_DIR/local-memory-bridge.js" record "*coverage" "@qa"
sleep 1
echo "✓ 2 comandos registrados"
echo ""

echo "3️⃣  Sugestões para próximo comando após @dev *task:"
node "$MEMORY_DIR/local-memory-bridge.js" suggest "*task" "@dev"
echo ""

echo "4️⃣  Comandos mais usados:"
node "$MEMORY_DIR/local-memory-bridge.js" most-used
echo ""

echo "5️⃣  Estatísticas por agente:"
node "$MEMORY_DIR/local-memory-bridge.js" stats
echo ""

echo "✅ Demo concluído!"
echo ""
echo "📚 O Memory Bridge está:"
echo "  ✓ Aprendendo seus padrões"
echo "  ✓ Armazenando em .synapse/learned-patterns.json"
echo "  ✓ Pronto para sugerir próximos comandos"
echo ""
echo "Use 'node $MEMORY_DIR/local-memory-bridge.js' para mais comandos"
