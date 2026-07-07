
🐍 Cobrinha Neon — Descrição do Projeto

***Cobrinha Neon** é uma releitura moderna, estilizada e imersiva do clássico jogo da cobrinha (*Blockade/Snake*). O projeto combina a jogabilidade nostálgica e viciante do fliperama clássico com uma estética visual **Cyberpunk/Neon**, trazendo gráficos vibrantes com efeitos de brilho difuso (*glow*), sistemas de partículas dinâmicas e áudio sintetizado em tempo real.

O jogador controla uma cobra que se move em um plano infinito (com a física de atravessar paredes e reaparecer no lado oposto). O objetivo é consumir os alimentos que surgem na tela para acumular pontos. A cada alimento ingerido, a velocidade do jogo aumenta progressivamente e a cauda da cobra cresce, tornando a movimentação pelo cenário cada vez mais desafiadora.

 ✨ Diferenciais e Recursos Visuais

* **Abertura e Game Over Temáticos:** Telas exclusivas de introdução (com textos piscantes) e encerramento com salvamento automático de recordes (*High Score*).
* **Anatomia Detalhada da Cobra:** A cabeça possui olhos dinâmicos que olham para a direção do movimento e uma língua bífida animada. O corpo possui um formato anatômico orgânico (estilo cascavel) que afina em direção à cauda e exibe texturas de escamas brilhantes.
* **Efeitos de Brilho (*Glow*):** Elementos essenciais como a cabeça, a comida e o título utilizam camadas de transparência para simular luzes de neon reais.
* **Sistema de Partículas:** Explosões de poeira neon colorida geradas aleatoriamente no momento em que a comida é coletada.

---

 🛠️ Tecnologias e Bibliotecas Utilizadas

O desenvolvimento do jogo foi feito inteiramente em **Python**, prezando pela leveza e pela eliminação completa de dependências de arquivos de mídia externos.

 1. Linguagem Principal

* **Python 3:** Linguagem base devido à sua legibilidade, forte ecossistema para desenvolvimento de scripts e prototipagem rápida de jogos.

 2. Bibliotecas e Módulos

* **Pygame (e Pygame.mixer):** O motor gráfico e de áudio do projeto. Utilizado para renderizar as formas geométricas primitivas, gerenciar a janela do jogo, controlar a taxa de quadros por segundo (`clock.tick`), capturar os eventos do teclado e reproduzir os canais de som.
* **Math (Nativo):** Utilizado para gerar funções trigonométricas (como as ondas senoidais: `math.sin`) fundamentais na síntese de áudio matemática de frequências em Hertz.
* **Array (Nativo):** Utilizado para manipulação eficiente de memória estruturada em baixo nível, permitindo criar *buffers* binários de áudio de 16 bits para o mixer de som.
* **Random (Nativo):** Responsável por toda a imprevisibilidade do jogo, desde o posicionamento aleatório da comida até a velocidade, tamanho e direção das partículas geradas nas explosões.
* **OS (Nativo):** Utilizado para manipulação do sistema de arquivos de forma segura entre diferentes sistemas operacionais (Windows, Mac, Linux), gerando e atualizando o arquivo de persistência de recordes `recorde.txt`.

 3. Técnicas Especiais Implementadas

* **Sintetizador Chiptune (Áudio em Tempo Real):** O jogo dispensa arquivos `.mp3` ou `.wav`. Os efeitos de cliques de movimento, os *blips* de pontuação, as músicas da abertura e o efeito de explosão/derrota do Game Over são gerados **calculando ondas sonoras via código direto na memória RAM**.
* **Blitting com Canal Alpha (SRCALPHA):** Criação de superfícies transparentes para a renderização de gradientes geométricos, simulando o efeito de iluminação fluorescente (Neon).
