# 🐍 Snake Neon

Jogo da cobrinha desenvolvido em **Python com Pygame**, com visual neon, efeitos de partículas e sons sintetizados por código.

Um projeto de estudo para praticar lógica de programação, criação de interfaces e desenvolvimento de jogos.

## 📸 Demonstração
## 📸 Demonstração

Confira duas imagens do Snake Neon:

![Snake Neon — imagem 1]<img width="1600" height="1200" alt="WhatsApp Image 2026-10-20 at 17 29 31" src="https://github.com/user-attachments/assets/633c839d-edd3-440e-83d1-f210929b8143" />
)

![Snake Neon — imagem 2]<img width="1600" height="1200" alt="WhatsApp Image 2026-10-20 at 17 31 37" src="https://github.com/user-attachments/assets/37739061-ab7e-4119-a40b-d8e951b31ff0" />


<!-- ![Tela do Snake Neon](imagens/snake-neon.png) -->

## 🎮 Funcionalidades

- Tela de abertura com música.
- Cobra com olhos, língua e corpo com escamas.
- Comida com efeito de brilho.
- Partículas ao coletar comida.
- Sons de mudança de direção, alimentação e derrota.
- Aumento de velocidade conforme a cobra cresce.
- Pontuação e recorde salvo em arquivo.
- Tela de fim de jogo com opção de reiniciar.
- Modo sem paredes: a cobra atravessa as bordas da tela.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Uso no projeto |
|------------|----------------|
| Python | Lógica e organização do jogo |
| Pygame | Janela, desenhos, teclado e reprodução de áudio |
| random | Posição da comida, partículas e ruído sonoro |
| math | Cálculos das ondas sonoras |
| array | Armazenamento das amostras de áudio |
| os | Verificação do arquivo de recorde |

## 🧩 Como o jogo foi feito

### 1. Janela e cenário

A janela tem resolução de 800 × 600 pixels.

O cenário utiliza um fundo escuro com uma grade de pontos.
Os elementos são desenhados com formas geométricas do Pygame,
sem depender de imagens externas.

### 2. Movimento da cobra

A cobra se movimenta em uma grade de 20 pixels.

As variáveis `dx` e `dy` definem a direção.
O corpo é representado por uma lista de posições:
a cada movimento, uma nova cabeça é adicionada e,
quando necessário, o último segmento da cauda é removido.

### 3. Comida e crescimento

A comida aparece em posições aleatórias da grade.

Quando a cabeça alcança a comida:

- A cobra cresce um segmento.
- A pontuação aumenta.
- A velocidade aumenta.
- Um som é reproduzido.
- Uma explosão de partículas aparece.

### 4. Colisões

O jogo verifica se a cabeça encostou no próprio corpo.
Quando isso acontece, a tela de fim de jogo é exibida.

As bordas não causam derrota: ao sair por um lado,
a cobra reaparece no lado oposto.

### 5. Visual neon

O brilho é criado com superfícies transparentes
desenhadas atrás dos elementos.

A cabeça possui olhos e língua que acompanham a direção.
O corpo usa segmentos com tamanhos e cores diferentes
para criar o efeito de escamas e afinamento da cauda.

### 6. Sons gerados por código

Os efeitos sonoros são sintetizados com `math` e `array`
e reproduzidos pelo mixer do Pygame.

As frequências e durações variam para criar sons de:

- Mudança de direção.
- Coleta de comida.
- Derrota.
- Melodia de abertura.

Não é necessário baixar arquivos de música ou efeitos.

### 7. Recorde

O recorde é armazenado no arquivo `recorde.txt`.

Quando uma partida termina com uma pontuação maior,
o arquivo é atualizado. Assim, o recorde pode ser
carregado na próxima execução.

## 🚀 Como executar

É necessário ter o Python instalado.

Instale o Pygame:

```bash
python -m pip install pygame
```

Na pasta do projeto, execute:

```bash
python main.py
```
```
cobrinha.py
```

## ⌨️ Controles

| Tecla | Ação |
|-------|------|
| ↑ | Mover para cima |
| ↓ | Mover para baixo |
| ← | Mover para a esquerda |
| → | Mover para a direita |
| Espaço | Iniciar ou reiniciar nas telas de menu |
| Esc | Sair nas telas de abertura e fim de jogo |

## 📚 Aprendizados

Este projeto permite praticar:

- Funções, listas e variáveis.
- Laços de repetição e condições.
- Eventos de teclado.
- Coordenadas e colisões.
- Desenho de elementos na tela.
- Síntese e reprodução de áudio.
- Leitura e gravação de arquivos.

## 🔮 Ideias para próximas versões

- [ ] Pausar a partida.
- [ ] Ativar e desativar o som.
- [ ] Escolher a dificuldade.
- [ ] Criar um modo com paredes.
- [ ] Impedir que a comida apareça dentro da cobra.

## 👨‍💻 Autor

**Édico Gama**

Estudante de Engenharia de Software,
aprendendo e construindo projetos com Python.

[Meu GitHub](https://github.com/edico-gama)
