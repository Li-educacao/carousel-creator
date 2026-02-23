# Quer saber como funciona o circuito de feedback? Então se liga! #AME

- **Video ID:** mWL7dl6sMfU
- **URL:** https://www.youtube.com/watch?v=mWL7dl6sMfU
- **Duration:** 4 min
- **Views:** 1,611
- **Published:** 2020-09-25T15:00:11Z
- **Category:** medium

---

## Transcript

A fonte  chaveada ela tem basicamente o que? Ela vai ter um transformador, um primário... vou desenhar assim Vai ter diferentes secundários... vou desenhar aqui três secundários Do primário vai vir +310V, certo? E aqui vai vir para um IGBT E vai pro GND, certo? Tem um IGBT aqui que vai chavear, é um chaveador né... no caso lá... nas placas de ar-condicionado de maneira geral Tem um encapsulamento, certo? Onde um pino do CI chaveador Um dos pinos dele vai no primário, e dentro dele tem um drive de acionamento do gate, aí tem umas pinagens aqui do drive... Os outros pinos do CI... mas internamente basicamente o CI é isso... um drive pra acionamento do IGBT E aí temos o circuito, basicamente é isso mas tem mais coisas aqui Mas o IGBT você não vê na placa porque está dentro do CI chaveador Beleza, a gente vai falar sobre o circuito de feedback, que circuito é esse que faz a leitura, que diz pra esse CI chaveador Que ele tem que chavear corretamente aquela fonte chaveada... quando ele vai chavear o IGBT, fechar essa chavezinha do IGBT Pra oscilar a tensão aqui, oscilar a corrente... e utilizar a característica do transformador que vai se evidenciar Na variação de tensão aqui da bobina do primário, quando variar aqui vão gerar os secundários Ou ele pega um secundário só pro feedback ou ele vai ler um 5V, um 15V, um 12V... vamos supor que ele pegue um secundário E aí ele manda um diodo... bem simples... esse diodo não é um diodo é um optoacoplador, onde ele vem aqui É um opto...  ele tem acionamento por luz aqui é um LED quando aciona aqui ele manda o sinal do opto E esse sinal do opto ele vem pra algum pino do chaveador... pra dizer o que Lawhander? Como assim? Então eu tenho: um IGBT que aciona o primário, que vai gerar as tensões dos secundários. Uma tensão gerada numa bobina geralmente Ou é dedicada ou pega a leitura de um nível de tensão, manda pro circuito claro, vai pro optoacoplador Que manda um feedback e aqui é o sinal de feedback Manda o sinal de feedback para o CI chaveador