# APC-2026-1
Estudante de APC

Olá , Meu nome é Gabriel de Oliveira . Sou aluno do 6° semestre de Engenharia Mecatrônica.

Gostaria muito de virar profissional em linguagens de programação em quântica e me tornar um ótimo programador com essa matéria.

Semana 2 : No Octostudio gostei muito da experiência de fazer uma pequena balada , a forma como flui a programação em Blocos é muito interessante

Semana 3 : No LMC tive a proposta de fazer o PC tem um estouro de memoria onde o exponencial de 3 fizesse o trabalho dos números subirem o mais rápido possível.

---

# Game Lab + APC — Semanas 04 a 16

---

## Semanas 04–06 — Construindo a Base Visual e Interativa

O ponto de entrada foi o ambiente do Game Lab e seu sistema de coordenadas. Posicionar formas na tela a partir de um referencial X/Y definido é, no fundo, o mesmo modelo mental que uso quando penso em espaço de clip no Vulkan: você tem um espaço, define onde o objeto existe dentro dele, e opera sobre isso. O substrato muda dependendo do contexto — aqui era uma engine educacional, lá é uma pipeline com vertex shaders — mas a lógica de posicionamento no espaço é a mesma. Isso acelerou bastante a absorção do conteúdo inicial.

A partir daí, o foco foi em aprender a modificar propriedades dos objetos desenhados em tempo de execução — tamanho, cor, escala — e a trabalhar com variáveis como mecanismo de persistência de estado. Esse segundo ponto parece óbvio, mas é exatamente o que separa um programa estático de um sistema com memória. E "memória de estado" é o que diferencia um renderizador passivo de um loop de jogo funcional. Perceber essa conexão enquanto fazia os exercícios foi o tipo de insight que vale registrar. A aleatoriedade entrou logo depois — sistemas que precisam parecer orgânicos sem ser completamente caóticos dependem de variância controlada injetada no estado. O ambiente abstrai a implementação, mas o raciocínio por trás é o mesmo.

A segunda parte dessas semanas foi dedicada a sprites — objetos com imagem acoplada, posicionáveis e manipuláveis no espaço do jogo. Do ponto de vista de engine, um sprite é um quad texturizado com metadados de transformação. Manipular escala, rotação e coordenadas diretamente no código foi o exercício mais direto do período: são as mesmas operações que uma matriz de transformação model-view realiza. O ambiente abstrai o math, mas o que está acontecendo por baixo é multiplicação de matrizes afins. Texto renderizado na tela completou o módulo — fonte, tamanho, posição — útil pra HUD e feedback de estado ao jogador.

O ponto de inflexão de todo esse bloco foi compreender o **draw loop** — o ciclo de renderização repetitivo que roda várias vezes por segundo. Entender que animação é simplesmente estado sendo redesenhado quadro a quadro num ciclo contínuo é o modelo mental correto pra qualquer renderizador. Não tem mistério: é um loop executando com estado atualizado a cada iteração. Quem já pensou em como um swap chain funciona reconhece a estrutura imediatamente. O que o Game Lab faz é tornar isso visível de forma concreta e imediata.

Com o loop estabelecido como base, movimentação de sprites e captura de input fecharam o ciclo dessas semanas. Atualizar posição a cada frame cria a ilusão de movimento contínuo — cinemática discreta no nível mais básico. Input de teclado e mouse adicionou a camada de interatividade: evento entra, lógica booleana processa, estado atualiza, próximo frame reflete a mudança. Um event loop simplificado, mas com a mesma estrutura de qualquer sistema reativo.

---

## Semana 07 — Introdução à Física e Cinemática

A aula teórica foi dedicada a dúvidas sobre o Code.org. A aula prática não aconteceu por problemas de saúde do professor.

O conteúdo da semana marcou uma mudança de paradigma na forma de pensar movimentação. Até aqui, mover um objeto significava atribuir diretamente sua posição a cada frame. A transição pra movimentação baseada em velocidade — acumulando `velocityX` e `velocityY` em vez de sobrescrever coordenadas — foi o salto conceitual mais relevante do período. Quando você acumula velocidade, comportamentos orgânicos emergem naturalmente: aceleração, inércia, resposta a forças externas. Você não precisa programar cada nuance do movimento; elas surgem da física acumulada. É o mesmo princípio que motores como Bullet ou PhysX implementam em C++, com broadphase e narrowphase otimizados em cima, mas o raciocínio de base é idêntico.

A detecção de colisão entrou logo na sequência — o sistema verifica interseção de bounding boxes a cada frame e expõe o resultado como booleano. Mecânica clássica que fundamenta qualquer sistema de física mais sofisticado. Identificar coleta de itens, receber dano, travar movimento em bordas — tudo parte dessa primitiva.

---

## Semana 08 — Física Avançada, Modularização e Projeto Final

A aula prática foi conduzida pelos monitores, com objetivo de concluir as atividades do Code.org. A aula teórica revisou aplicações gerais da ciência da computação e suas interseções com diferentes áreas.

Com a base de colisão estabelecida, a semana avançou pra respostas físicas entre objetos: `bounce`, `bounceOff`, `collide`, `displace`. Cada uma define um comportamento diferente ao contato — um objeto para, quica, empurra ou é deslocado pelo outro. São as primitivas de resposta a colisão que qualquer motor de física usa como base. Combinadas com gravidade simulada como aceleração negativa acumulada na componente Y da velocidade, o resultado é fisicamente plausível sem precisar resolver equações diferenciais explicitamente. O ambiente abstrai a integração numérica, mas o comportamento resultante é reconhecível pra quem já pensou em simulação de corpos rígidos.

Modularização via funções fechou a parte técnica: agrupar lógicas repetitivas em funções com responsabilidade única. Código não modular não escala e não é maintível. É pré-requisito pra qualquer coisa que precise crescer além de um protótipo descartável — sem filosofia.

O projeto final integrou tudo: desenho, sprites, loops, física, interatividade e funções num jogo completo, planejado e publicado do zero. Foi o momento de verificar se o aprendizado das semanas anteriores havia se consolidado ou só passado pela superfície. O jogo está na pasta `Semana04-08`.

---

## Semanas 09–11 — Lógica de Baixo Nível em C

### Semana 09

Entrada no C com exercícios introdutórios a partir do ambiente disponibilizado. C não foi novidade conceitual, mas a revisão tem valor real: quando você está pensando em otimização de inferência, em comportamento de driver de GPU, ou em como uma instrução se traduz em operações sobre registradores, a base é essa. C é o nível onde as abstrações começam a desaparecer e o que resta é manipulação direta de dados e memória. Trabalhar isso de forma sistemática é sempre um investimento válido. PDF com resoluções na pasta `Semana09`.

### Semanas 10–11

Aprofundamento em operadores aritméticos e lógicos, com foco na prova escrita. Arquivo: `exercicios_operadores_c.md`. O conteúdo em si não é novo, mas o domínio profundo sobre operadores — especialmente os bitwise — é o que diferencia quem programa de quem entende o que o programa está fazendo na memória. O reforço sistemático justifica o tempo investido.

---

## Semanas 12–13 — Algoritmos de Ordenação e Análise de Dados Reais

A teoria foi trabalhada através de visualizações interativas de algoritmos de ordenação — [VisuAlgo](https://visualgo.net/en/sorting), [USFCA](https://www.cs.usfca.edu/~galles/visualization/ComparisonSort.html) e [Toptal](https://www.toptal.com/developers/sorting-algorithms). Ver o comportamento quadrático de um bubble sort quebrando com volume enquanto um merge sort mantém consistência é mais convincente do que qualquer tabela de complexidade no papel. Visualização interativa acelera a internalização de por que O(n log n) é o teto prático pra comparação por chave.

A parte prática foi a aplicação direta num dataset real: o PDAD. O `moradores.xlsx` foi convertido pra `.csv` pra funcionar corretamente no JupyterLab. Trabalhei com dados de moradores e domicílios por Região Administrativa, extraindo métricas de escolaridade e gênero. Ter contexto pré-existente sobre o dataset — já havia trabalhado com o PDAD no projeto final da APC — reduziu drasticamente o tempo de exploração inicial e permitiu ir direto pra parte analítica. A pasta `Semana12-13` contém os exercícios completos e três relatórios de exemplo do exercício 4. Os demais podem ser gerados rodando o código.

---

## Semana 14 — Avaliação P1 e Tkinter

Aula teórica (15/06): aplicação da P1. Aula prática: correção da prova seguida de introdução ao Tkinter.

Arquivos produzidos durante os exercícios práticos:
`01_janela_basica.py` · `02_widgets.py` · `03_layout_grid.py` · `04_eventos_bind.py` · `05_dialogos.py` · `06_grafico.py`

Tkinter não é minha área de interesse principal — meu foco está em níveis mais baixos da stack. Mas entender estruturação de layout com Grid, ciclo de vida de widgets e gestão de eventos de janela tem valor prático real pra criar dashboards de monitoramento e ferramentas internas. Não é onde quero investir tempo profundo, mas ser autossuficiente nisso faz parte do perfil que quero construir como engenheiro.

---

## Semanas 15–16 — Projeto Final: Pipeline PDAD 2024

**Datasets utilizados:**
- `PDAD_2024-Moradores.csv` — aproximadamente 25.000 registros, uma linha por morador
- `PDAD_2024-Domicilios.xlsx` — uma linha por domicílio
- Fonte: [pdad.ipe.df.gov.br](https://pdad.ipe.df.gov.br)

O projeto foi a aplicação mais completa do semestre em termos de integração de conceitos. A proposta foi construir um pipeline completo: leitura de dados brutos → processamento estatístico por Região Administrativa → exportação de relatório estruturado em `.txt`.

**Métricas geradas:**
- Média de idade — por RA e geral
- Percentual de mulheres — por RA e geral
- Distribuição de gênero — por RA e geral
- Distribuição de escolaridade — por RA e geral

Processar 25.000 registros num pipeline que vai de dados brutos até um relatório legível envolve as mesmas decisões de design que qualquer pipeline de dados em produção: como ler, como tratar inconsistências, como agregar com a granularidade certa, como formatar a saída de forma útil pra quem vai consumir o resultado.

É a mesma lógica que aplico quando processo outputs de benchmarks de inferência no meu setup: dados crus entram, você define as métricas relevantes, transforma e exporta num formato que permita tomada de decisão sem ambiguidade. O dataset e o domínio mudam — o padrão de raciocínio não. Essa consistência entre domínios diferentes é o que torna o conteúdo de APC genuinamente relevante pra mim, além da avaliação.
