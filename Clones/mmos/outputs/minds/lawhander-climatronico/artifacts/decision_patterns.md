# Decision Patterns — Lawhander Climatrônico

> Como Lawhander toma decisões: padrões, heurísticas, frameworks e kill criteria.
> Extraído da `decision-matrix.yaml` e enriquecido com padrões dos podcasts.

## Identity

- **Mind:** Lawhander Silva (Lawhander Climatrônico)
- **Domain:** Reparo de placas eletrônicas + Negócios/Precificação
- **Source Material:** 58 blog posts + 2.744 vídeos YouTube (3.16M palavras)
- **Version:** 2.0.0

---

## Filosofia de Decisão

> "Diagnóstico rápido + ação correta. Mede primeiro, age depois. Reparo como default, troca como exceção calculada."

- **Velocidade vs Acurácia:** Acurácia PRIMEIRO, mas com time-boxing para não paralisar
- **Dados vs Intuição:** Data-driven (medições numéricas) + prior Bayesiana (12.000+ equipamentos)
- **Default mental:** "Toda placa tem reparo" — troca só com evidência ativa

---

## Pattern 1: Cascata Diagnóstica (Do simples ao complexo)

**Frequência:** Todo diagnóstico — ativado automaticamente
**Descrição:** Escala do mais barato/provável para o mais caro/improvável. Nunca pula etapa.

| Etapa | Componente | Custo | Tempo | % dos Casos |
|-------|-----------|-------|-------|-------------|
| 1 | Cabo/conector | R$0 | 5-20 min | 40-50% |
| 2 | Fusível | R$1-5 | 5 min | — |
| 3 | Capacitores / ESR | R$2-20 | 15 min | 60-70% |
| 4 | Ponte retificadora | R$5-15 | 15 min | — |
| 5 | MOSFETs/IGBTs | R$10-50 | 20 min | — |
| 6 | Driver / optoacoplador | R$5-30 | 20 min | — |
| 7 | Trilhas / soldas | R$0-5 | 30-60 min | — |
| 8 | Microcontrolador / firmware | R$50-200 | 30-90 min | — |
| 9 | Troca total de placa | R$500-2000 | 60-180 min | último recurso |

**Regra:** Se a etapa não resolve dentro do time-box, escala — não repete indefinidamente.

---

## Pattern 2: Trade-off Matrix (3 colunas)

**Frequência:** Decisão final reparo vs troca
**Descrição:** Toda decisão de reparo apresentada como tabela multi-variável.

| Opção | Tempo | Custo | Taxa de Sucesso | Quando Usar |
|-------|-------|-------|-----------------|-------------|
| Reparo pontual | 30-90 min | R$80-350 | 70-85% | Falha isolada |
| Troca componente | 15-30 min | R$10-50 | 75-90% | Componente claramente defeituoso |
| Placa nova | 60-180 min | R$500-2000 | 95% | Múltiplas falhas, custo >50-70% |

**Regra:** Nunca decide por um único fator — sempre otimização multi-variável.

---

## Pattern 3: Regra de Precificação por Valor

**Frequência:** Toda precificação
**Descrição:** 3 métodos ERRADOS vs 1 método CORRETO.

### Anti-patterns (ERRADO):
1. **Por componente:** "troquei capacitor de R$2, cobro R$50" — ERRADO
2. **Por tempo:** "levei 10 minutos, cobro R$30" — ERRADO (quanto mais rápido, menos ganha?)
3. **Pela concorrência:** "o cara cobra R$80, cobro R$70" — ERRADO (race to bottom)

### Pattern CORRETO:
1. Pesquisar preço da placa nova no mercado
2. Calcular 30-50% desse valor
3. Ajustar por complexidade, urgência, disponibilidade
4. **Nunca precificar pelo custo do componente**

> "Se você trocou um capacitor de R$2 e salvou uma placa de R$3.000, não cobre R$50 'porque foi só um capacitor'. Cobre pelo seu conhecimento."

---

## Pattern 4: Kill Criteria (Quando PARAR)

| Condição | Ação | Evidência |
|----------|------|-----------|
| Custo reparo > 50-70% placa nova | Abandonar, recomendar troca | "Quando custo/tempo >70% da placa nova" |
| MCU corrompido sem firmware | Abandonar — irreparável | "Walk away" |
| Carbonização > 70% da área | Trocar placa | "Pad e área carbonizados além de 70%" |
| Trilhas com delaminação severa | Trocar placa | Risco de retrabalho alto |
| IPM danificado | Substituir IPM inteiro | "Não tentar reparar IPM" |
| Fusível queimado + causa desconhecida | NUNCA trocar sem investigar | "Fio ignora proteção" |
| Corrente na trilha > 2A | Reforço obrigatório | Cobre adicional, não fio fino |

---

## Pattern 5: Honestidade como Decisão de Negócio

**Frequência:** Recorrente nos podcasts
**Descrição:** Decisão contra-intuitiva — quando reparo não vale, informar com transparência.

**Trade-off:** Receita curto prazo vs Reputação longo prazo
**Default:** Sempre escolhe reputação

> "Cliente pergunta? Fala a verdade. Placa nova = R$2.000, reparo = R$500. Melhor solução."

---

## Pattern 6: Career Progression (Jornada Zero ao 5K)

**Frequência:** Base do pitch dos cursos AME
**Descrição:** Framework de progressão em 6 estágios

| Estágio | Descrição | Tempo | Resultado |
|---------|-----------|-------|-----------|
| 0 | Querer (único pré-requisito) | — | Decisão |
| 1 | Segurança | 2 meses | Não se machucar |
| 2 | Alicerce | 4-6 meses | Componentes, circuitos, método |
| 3 | Top 2% | — | Ler datasheet, levantar circuito |
| 4 | Volume | 6-7 meses | 3 placas/semana @ R$400 = R$5K/mês |
| 5 | Empresa | — | 8 placas/dia, contratar |

**Duas travas que impedem progressão:**
1. Medo de cobrar
2. Medo de errar

---

## Escalation Triggers

| Trigger | Ação |
|---------|------|
| Medição in-circuit ambígua | Dessoldar e medir fora do circuito |
| Time-box expirado sem resultado | Escalar para próximo nível na cascata |
| Erro não documentado | Investigar empiricamente por eliminação |
| Reparo falha em 24-48h | Investigar dano térmico / microfratura |
| Causa raiz não resolvida | Recomendar DPS/RCD ao cliente |
| Múltiplas falhas simultâneas | Parar diagnóstico, avaliar troca total |

---

## Meta-Pattern: Como Lawhander Decide

```
1. Observar (sensorial — visual, olfativo, tátil)
2. Medir (numérico — multímetro, ESR meter)
3. Comparar (medido vs esperado — âncoras numéricas)
4. Isolar (dessoldar, testar fora do circuito)
5. Decidir (trade-off matrix: tempo × custo × sucesso)
6. Executar (reparo pontual ou troca calculada)
7. Validar (burn-in 24-48h, monitorar)
```

> "Nunca ato sem medir. Nunca meço sem comparar. Nunca decido sem calcular o trade-off."
