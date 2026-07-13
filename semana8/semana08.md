# Semana 08 — Física Avançada, Modularização e Projeto Final

**Plataforma:** Code.org — Game Lab  
**Foco:** Respostas físicas a colisão, funções, projeto final  
**Observação:** Aula prática conduzida pelos monitores (professor ainda afastado). Aula teórica revisou aplicações gerais da ciência da computação.

---

## Respostas Físicas a Colisão

Com a detecção de colisão estabelecida na semana anterior, essa semana avançou para as respostas físicas entre objetos: `bounce`, `bounceOff`, `collide`, `displace`. Cada função define um comportamento diferente ao contato — um objeto para, quica, empurra ou é deslocado pelo outro.

São as primitivas de resposta a colisão que qualquer motor de física usa como base, com mais ou menos complexidade empilhada em cima dependendo do caso de uso. A diferença entre `bounce` e `bounceOff`, por exemplo, mapeia diretamente pra conceitos de conservação de momentum e coeficiente de restituição — o Game Lab abstrai os cálculos, mas o comportamento resultante segue a mesma física.

Combinadas com gravidade simulada — modelada como aceleração negativa acumulada na componente Y da velocidade — o resultado é fisicamente plausível sem precisar resolver equações diferenciais explicitamente. O ambiente faz a integração por baixo; o que cabe ao programador é entender quais forças estão sendo aplicadas e como elas interagem.

---

## Modularização via Funções

Funções pra agrupar lógicas repetitivas com responsabilidade única. Código não modular não escala, não é maintível e acumula débito técnico que compromete qualquer evolução futura do projeto.

Não tem muito a filosofar aqui — é pré-requisito pra qualquer coisa que precise crescer além de um protótipo descartável. A forma como você nomeia e delimita funções já documenta o código; o nome certo elimina a necessidade de comentário.

---

## Projeto Final

O projeto final integrou tudo que foi construído ao longo das semanas 04 a 08: desenho, sprites, loops, física, interatividade e funções, num jogo completo planejado e publicado do zero.

Foi o momento de verificar se o aprendizado havia se consolidado de verdade ou só passado pela superfície. Integrar conceitos que foram introduzidos em momentos diferentes num sistema coeso exige que você entenda como eles se relacionam — não só como cada um funciona isoladamente.

O jogo está na pasta `Semana04-08/`.
