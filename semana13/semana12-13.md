# Semanas 12–13 — Algoritmos de Ordenação e Dados Reais

**Ferramentas:** JupyterLab, Python  
**Dataset:** PDAD 2024 (moradores e domicílios — DF)  
**Foco:** Complexidade algorítmica, ordenação, análise exploratória

---

## Teoria — Complexidade e Visualização

A abordagem teórica foi através de visualizações interativas dos algoritmos de ordenação:

- [VisuAlgo](https://visualgo.net/en/sorting)
- [USFCA](https://www.cs.usfca.edu/~galles/visualization/ComparisonSort.html)
- [Toptal](https://www.toptal.com/developers/sorting-algorithms)

Visualizações interativas aceleram a internalização de por que O(n log n) é o teto prático pra comparação por chave de uma forma que tabelas de complexidade no papel não conseguem replicar. Ver o comportamento quadrático de um bubble sort quebrando com volume enquanto um merge sort mantém consistência é mais convincente e mais memorável do que decorar a equação.

O ponto central aqui não é qual algoritmo é "melhor" — é entender que a escolha de estrutura de dados e algoritmo tem impacto direto e mensurável em performance conforme o volume escala. Isso é relevante em qualquer contexto que envolva processamento de dados em quantidade: pipelines de dados, sistemas de busca, inferência em batch.

---

## Prática — PDAD no JupyterLab

A atividade prática aplicou os algoritmos num dataset real: o PDAD (Pesquisa Distrital por Amostra de Domicílios). O arquivo `moradores.xlsx` foi convertido para `moradores.csv` pra funcionar corretamente no JupyterLab via [jupyter.org/try-jupyter](https://jupyter.org/try-jupyter/lab/index.html).

Trabalhei com os dados de moradores e domicílios segmentados por Região Administrativa, extraindo métricas de escolaridade e gênero.

Ter contexto pré-existente sobre o dataset foi uma vantagem significativa — já havia trabalhado com o PDAD no projeto final. Isso reduziu drasticamente o tempo de exploração inicial e permitiu ir direto pra parte analítica, que é onde o valor real está.

---

## O que foi dado messas semanas 

- Arquivo com os exercícios completos
- Três relatórios de exemplo referentes ao exercício 4

Os demais relatórios podem ser gerados rodando o código com os parâmetros correspondentes no Git do Professor
