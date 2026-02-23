# 📚 LOCAL MEMORY BRIDGE — Pattern Learning System

**Status:** ✅ Ativo | **Versão:** 1.0.0 | **Data:** 2026-02-14

## O Que Faz

O Memory Bridge **aprende seus padrões de comando** e **sugere próximos passos** baseado no histórico.

### Exemplo Prático

**Sessão 1:**
```
@dev *task create-component
@dev *task create-test
@dev *task run-lint
@qa *test
```

**Sessão 2 — Memory aprende:**
```
@dev *task create-component
  → Memory sugere: *task create-test (90% confiança)
@dev *task create-test
  → Memory sugere: *task run-lint (85% confiança)
```

## Arquitetura

```
.aios-core/core/synapse/memory/
├── local-memory-bridge.js      ← Motor de aprendizado
├── memory-integration.js        ← Integração com Synapse
└── (fornecido pelo framework)

.synapse/
├── learned-patterns.json        ← Padrões aprendidos (atualizado automaticamente)
├── sessions/                    ← Sessões do Synapse
└── MEMORY-BRIDGE.md            ← Este arquivo
```

## Como Usar

### 1️⃣ Automático (Transparente)

Você não precisa fazer nada. O Memory Bridge:
- ✓ Aprende cada comando que você executa
- ✓ Armazena em `.synapse/learned-patterns.json`
- ✓ Usa padrões em futuras sugestões

### 2️⃣ Manual (CLI Commands)

```bash
# Registrar comando específico
node .aios-core/core/synapse/memory/local-memory-bridge.js record "*create-story" "@dev"

# Sugerir próximos comandos
node .aios-core/core/synapse/memory/local-memory-bridge.js suggest "*task" "@dev"

# Ver comandos mais usados
node .aios-core/core/synapse/memory/local-memory-bridge.js most-used

# Ver estatísticas por agente
node .aios-core/core/synapse/memory/local-memory-bridge.js stats

# Limpar padrões com > 30 dias
node .aios-core/core/synapse/memory/local-memory-bridge.js cleanup
```

### 3️⃣ Integração com Synapse

O Memory Bridge é automaticamente consultado pelo Synapse para:
- Injetar contexto de padrões aprendidos
- Aumentar confiança de sugestões
- Personalizar comportamento por agente

## Estrutura de Dados

### `learned-patterns.json`

```json
{
  "commands": {
    "@dev:*task": {
      "count": 23,
      "lastUsed": "2026-02-14T15:30:00Z",
      "nextCommands": {
        "*run-lint": 18,
        "*test": 12,
        "*build": 5
      },
      "contexts": ["{...}", "{...}"]
    }
  },
  "workflows": {},
  "agents": {},
  "timestamp": "2026-02-14T15:30:00Z"
}
```

## Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| **Learning** | Aprende sequências de comandos automaticamente |
| **Suggestions** | Sugere próximos comandos com % de confiança |
| **Frequency** | Rastreia uso por agente e comando |
| **History** | Mantém histórico de contextos |
| **Cleanup** | Remove padrões > 30 dias automaticamente |
| **Export** | Exporta contexto para Synapse injection |

## Métricas

Após algumas semanas de uso, você terá:

```
📚 Learned 147 patterns from 1,230 executions
  @dev: 450 commands
  @qa: 320 commands
  @architect: 280 commands
  @pm: 180 commands

Top 3 Workflows:
  1. @dev: *task → *run-lint → *test (180x)
  2. @qa: *test → *coverage → *report (95x)
  3. @architect: *design → *validate → *docs (60x)
```

## Dados Armazenados

### Completamente Local ✅
- Tudo fica em `.synapse/learned-patterns.json`
- Nenhum dado enviado para servidor
- Você tem controle total
- Pode deletar/resetar quando quiser

### Privacidade ✅
- Apenas registra comandos (não conteúdo)
- Contexto é genérico (não sensível)
- JSON puro — sem encoding ou criptografia

## Resetar Memory

Quer começar do zero?

```bash
# Apagar arquivo de padrões
rm .synapse/learned-patterns.json

# Memory Bridge vai reconstruir automaticamente na próxima execução
```

## Atualizações Futuras

Funcionalidades planejadas:
- [ ] Export/import de padrões (backup)
- [ ] Análise de "padrões ineficientes"
- [ ] Alertas de anomalias
- [ ] Integração com Analytics
- [ ] Modelo preditivo de tempo de execução

---

**Criado:** 2026-02-14 | **Versão Synapse:** 4.0.4 | **Desenvolvedor:** Gage (DevOps)
