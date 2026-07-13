# Semana 07 — Física e Cinemática

**Plataforma:** Code.org — Game Lab  
**Foco:** Velocity, detecção de colisão  
**Observação:** Aula prática cancelada por problemas de saúde do professor. Aula teórica focou em dúvidas sobre o Code.org.

---

## Contexto

Essa semana marcou uma mudança de paradigma na forma de pensar movimentação dentro do Game Lab. Até aqui, mover um objeto significava atribuir diretamente sua posição a cada frame — você controlava onde o objeto estava, não como ele chegava lá.

---

## Velocity — A Transição Mais Importante

A migração pra movimentação baseada em velocidade (`velocityX` / `velocityY`) foi o salto conceitual mais relevante do período. A diferença não é só sintática: quando você acumula velocidade em vez de sobrescrever coordenadas, comportamentos orgânicos emergem naturalmente — aceleração, inércia, resposta a forças externas. Você não programa cada nuance do movimento; elas surgem da física acumulada ao longo dos frames.

É o mesmo princípio que motores como Bullet ou PhysX implementam em C++, com broadphase e narrowphase otimizados em cima, mas o raciocínio de base é idêntico. A abstração do Game Lab não muda a física — ela só esconde a integração numérica que acontece por baixo.

Esse modelo também escala: quando você começa a combinar velocidade com forças externas (vento, gravidade, colisões), o comportamento resultante é muito mais rico do que qualquer animação baseada em posição direta conseguiria gerar com a mesma quantidade de código.

---

## Detecção de Colisão

O `isTouching` introduziu a detecção de colisão — o sistema verifica interseção de bounding boxes a cada frame e expõe o resultado como um booleano. Mecânica clássica que fundamenta qualquer sistema de física mais sofisticado.

Identificar coleta de itens, aplicar dano, travar movimento em bordas, ativar eventos por proximidade — tudo parte dessa primitiva. É interessante perceber que mesmo motores comerciais complexos, no fundo, estão fazendo variações muito mais elaboradas dessa mesma checagem básica de sobreposição de volumes.
