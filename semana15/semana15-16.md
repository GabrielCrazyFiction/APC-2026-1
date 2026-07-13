# Semanas 15–16 — Projeto Final: Pipeline PDAD 2024

**Linguagem:** Python  
**Bibliotecas:** pandas, matplotlib, tkinter  
**Dataset:** PDAD 2024 — Governo do Distrito Federal  
**Fonte:** [pdad.ipe.df.gov.br](https://pdad.ipe.df.gov.br)

---

## Datasets utilizados

| Arquivo | Descrição |
|---|---|
| `PDAD_2024-Moradores.csv` | ~25.000 registros — uma linha por morador |
| `PDAD_2024-Domicilios.xlsx` | Uma linha por domicílio |

---

## O que foi construído

O projeto foi um pipeline completo de processamento de dados:

```
Leitura de dados brutos
        ↓
Limpeza e padronização
        ↓
Processamento estatístico por Região Administrativa
        ↓
Exportação de relatório estruturado em .txt
```

---

## Métricas geradas

As seguintes estatísticas foram calculadas tanto por Região Administrativa quanto de forma geral para o DF:

- Média de idade
- Percentual de mulheres
- Distribuição de gênero
- Distribuição de escolaridade

---

## Análise técnica

O projeto foi a aplicação mais completa do semestre em termos de integração de conceitos. Processar 25.000 registros num pipeline que vai de dados brutos até um relatório estruturado e legível envolve as mesmas decisões de design que qualquer pipeline de dados em produção: como ler com eficiência, como tratar inconsistências sem perder dados válidos, como agregar com a granularidade certa, e como formatar a saída de forma útil pra quem vai consumir o resultado.

A lógica é a mesma que aplico quando processo outputs de benchmarks de inferência no meu setup: dados crus entram, você define quais métricas são relevantes pra responder as perguntas que importam, transforma com a granularidade certa, e exporta num formato que permita tomada de decisão sem ambiguidade. O dataset e o domínio mudam — o padrão de raciocínio não.

Ter contexto prévio sobre o PDAD (já havia trabalhado com ele nas semanas 12-13) ajudou a tomar decisões de tratamento mais informadas — saber de antemão quais campos têm valores nulos esperados, quais regiões têm amostras menores e como isso afeta médias, quais colunas do dicionário de dados mapeiam pro que.

---

## Estrutura do relatório gerado

O relatório final em `.txt` organiza as métricas primeiro no nível do DF como um todo, depois por Região Administrativa — o que permite tanto uma visão macro quanto a identificação de disparidades regionais em escolaridade, composição de gênero e faixa etária.
