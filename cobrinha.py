import pygame
import random
import os
import array
import math

# Inicializa o Pygame e o Mixer de Áudio
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=1)

# CONFIGURAÇÕES DE TELA
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Snake Neon")
clock = pygame.time.Clock()

# CORES
AZUL_NEON     = (0, 240, 255)
ROXO_NEON     = (180, 0, 255)
VERDE_NEON    = (0, 255, 100)
VERMELHO_NEON = (255, 0, 90)
AMARELO_NEON  = (255, 220, 0)
BRANCO        = (255, 255, 255)
PRETO         = (10, 10, 10)
CINZA_ESCURO  = (15, 15, 22)

# CONFIGURAÇÕES DO JOGO
tamanho = 20
VELOCIDADE_INICIAL = 10
velocidade_atual = VELOCIDADE_INICIAL

fonte_hud       = pygame.font.SysFont("Arial", 24, bold=True)
fonte_titulo    = pygame.font.SysFont("Arial", 60, bold=True)
fonte_subtitulo = pygame.font.SysFont("Arial", 28)

# ── 🎵 SINTETIZADOR DE SONS E MÚSICA ──────────────────────────────────
def gerar_som_sintetizado(tipo):
    max_amplitude = 2 ** 15 - 1
    amostras = array.array('h')
    
    if tipo == "click":
        duracao = 0.03
        frequencia = 600
        for i in range(int(duracao * 22050)):
            val = math.sin(2 * math.pi * frequencia * (i / 22050))
            amostras.append(int(val * max_amplitude * (1 - i / (duracao * 22050))))
            
    elif tipo == "comer":
        duracao = 0.15
        for i in range(int(duracao * 22050)):
            frequencia = 400 + (i * 3)
            val = math.sin(2 * math.pi * frequencia * (i / 22050))
            amostras.append(int(val * max_amplitude * (1 - i / (duracao * 22050))))
            
    elif tipo == "game_over":
        # Som de explosão/derrota descendente (Perdeu!)
        duracao = 0.8
        for i in range(int(duracao * 22050)):
            progresso = i / (duracao * 22050)
            frequencia = max(40, 400 - int(progresso * 350))
            # Adiciona um ruído para parecer uma explosão retro
            ruido = random.uniform(-0.3, 0.3)
            val = math.sin(2 * math.pi * frequencia * (i / 22050)) + ruido
            val = max(-1, min(1, val)) # limita o som
            amostras.append(int(val * max_amplitude * (1 - progresso)))
            
    elif tipo == "abertura":
        # Gera um loop de uma melodia Neon/Arpejo simples
        notas = [130, 147, 165, 196, 220, 196, 165, 147] # Frequências (Hz)
        tempo_nota = 0.2
        for nota in notas:
            for i in range(int(tempo_nota * 22050)):
                val = math.sin(2 * math.pi * nota * (i / 22050))
                # Onda quadrada suave para estilo chiptune
                val = 0.3 if val > 0 else -0.3
                amostras.append(int(val * max_amplitude * 0.5))
                
    return pygame.mixer.Sound(buffer=amostras)

# Inicializa os sons
som_mover = gerar_som_sintetizado("click")
som_comer = gerar_som_sintetizado("comer")
som_game_over = gerar_som_sintetizado("game_over")
musica_abertura = gerar_som_sintetizado("abertura")

# Volumes
som_comer.set_volume(0.4)
som_mover.set_volume(0.15)
som_game_over.set_volume(0.7)
musica_abertura.set_volume(0.3)

# ── HELPERS GRÁFICOS ──────────────────────────────────────────────────

def desenhar_fundo():
    tela.fill(CINZA_ESCURO)
    for x in range(0, LARGURA, tamanho):
        for y in range(0, ALTURA, tamanho):
            pygame.draw.circle(tela, (30, 30, 50), (x, y), 1)

def desenhar_brilho(surface, cor, rect, raio=12):
    s = pygame.Surface((rect.width + raio*2, rect.height + raio*2), pygame.SRCALPHA)
    pygame.draw.rect(s, (*cor, 45), s.get_rect(), border_radius=raio)
    surface.blit(s, (rect.x - raio, rect.y - raio))

def desenhar_comida(x, y):
    cx = x + tamanho // 2
    cy = y + tamanho // 2
    r  = tamanho // 2 - 1
    rect_comida = pygame.Rect(x, y, tamanho, tamanho)
    desenhar_brilho(tela, VERMELHO_NEON, rect_comida)
    pygame.draw.circle(tela, (100, 0, 30), (cx, cy), r + 5)
    pygame.draw.circle(tela, VERMELHO_NEON, (cx, cy), r)
    pygame.draw.circle(tela, (255, 150, 150), (cx - 3, cy - 3), 3)

def desenhar_cobra(corpo):
    """Cobra com cabeça detalhada e corpo com escamas e rabo que afina (estilo cascavel)."""
    global dx, dy
    
    comprimento_atual = len(corpo)
    
    for i, parte in enumerate(corpo):
        # ── CONFIGURAÇÃO DE TAMANHO DINÂMICO (AFINAMENTO DO CORPO) ──
        # O rabo (i baixo) fica menor e o corpo cresce até chegar perto da cabeça (i alto)
        progresso_tamanho = i / max(comprimento_atual - 1, 1)
        # O tamanho varia de 10 pixels (rabo) até 18 pixels (perto da cabeça)
        tam_dinamico = int(10 + (tamanho - 12) * progresso_tamanho)
        
        # Centraliza o bloco menor dentro do espaço de 20x20 padrão do jogo
        offset = (tamanho - tam_dinamico) // 2
        rect = pygame.Rect(parte[0] + offset, parte[1] + offset, tam_dinamico, tam_dinamico)
        
        # ── DESENHO DA CABEÇA (Mantém o tamanho cheio 20x20) ──
        if i == comprimento_atual - 1:
            rect_cabeca = pygame.Rect(parte[0] + 1, parte[1] + 1, tamanho - 2, tamanho - 2)
            desenhar_brilho(tela, VERDE_NEON, rect_cabeca, raio=12)
            pygame.draw.rect(tela, VERDE_NEON, rect_cabeca, border_radius=8)
            pygame.draw.rect(tela, BRANCO, rect_cabeca, 1, border_radius=8)
            
            direcao = "DIREITA"
            if dx > 0:   direcao = "DIREITA"
            elif dx < 0: direcao = "ESQUERDA"
            elif dy > 0: diecao = "BAIXO"
            elif dy < 0: direcao = "CIMA"
            
            cx, cy = parte[0], parte[1]
            
            if direcao == "DIREITA":
                pygame.draw.line(tela, VERMELHO_NEON, (cx + tamanho, cy + 10), (cx + tamanho + 6, cy + 10), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx + tamanho + 6, cy + 10), (cx + tamanho + 8, cy + 8), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx + tamanho + 6, cy + 10), (cx + tamanho + 8, cy + 12), 2)
                pygame.draw.circle(tela, BRANCO, (cx + 13, cy + 5), 3)
                pygame.draw.circle(tela, PRETO, (cx + 14, cy + 5), 1)
                pygame.draw.circle(tela, BRANCO, (cx + 13, cy + 15), 3)
                pygame.draw.circle(tela, PRETO, (cx + 14, cy + 15), 1)
            elif direcao == "ESQUERDA":
                pygame.draw.line(tela, VERMELHO_NEON, (cx, cy + 10), (cx - 6, cy + 10), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx - 6, cy + 10), (cx - 8, cy + 8), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx - 6, cy + 10), (cx - 8, cy + 12), 2)
                pygame.draw.circle(tela, BRANCO, (cx + 7, cy + 5), 3)
                pygame.draw.circle(tela, PRETO, (cx + 6, cy + 5), 1)
                pygame.draw.circle(tela, BRANCO, (cx + 7, cy + 15), 3)
                pygame.draw.circle(tela, PRETO, (cx + 6, cy + 15), 1)
            elif direcao == "CIMA":
                pygame.draw.line(tela, VERMELHO_NEON, (cx + 10, cy), (cx + 10, cy - 6), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx + 10, cy - 6), (cx + 8, cy - 8), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx + 10, cy - 6), (cx + 12, cy - 8), 2)
                pygame.draw.circle(tela, BRANCO, (cx + 5, cy + 7), 3)
                pygame.draw.circle(tela, PRETO, (cx + 5, cy + 6), 1)
                pygame.draw.circle(tela, BRANCO, (cx + 15, cy + 7), 3)
                pygame.draw.circle(tela, PRETO, (cx + 15, cy + 6), 1)
            elif direcao == "BAIXO":
                pygame.draw.line(tela, VERMELHO_NEON, (cx + 10, cy + tamanho), (cx + 10, cy + tamanho + 6), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx + 10, cy + tamanho + 6), (cx + 8, cy + tamanho + 8), 2)
                pygame.draw.line(tela, VERMELHO_NEON, (cx + 10, cy + tamanho + 6), (cx + 12, cy + tamanho + 8), 2)
                pygame.draw.circle(tela, BRANCO, (cx + 5, cy + 13), 3)
                pygame.draw.circle(tela, PRETO, (cx + 5, cy + 14), 1)
                pygame.draw.circle(tela, BRANCO, (cx + 15, cy + 13), 3)
                pygame.draw.circle(tela, PRETO, (cx + 15, cy + 14), 1)

        # ── DESENHO DO CORPO (EFEITO ESCAMAS NEON) ──
        else:
            # Gradiente de cor: rabo mais escuro, perto da cabeça mais claro
            verde = int(60 + 195 * progresso_tamanho)
            cor_interna = (0, int(verde * 0.4), int(verde * 0.2)) # Tom de fundo da escama
            
            # Desenha a base arredondada do gomo (corpo mais fluido)
            pygame.draw.rect(tela, cor_interna, rect, border_radius=tam_dinamico // 2)
            pygame.draw.rect(tela, (0, verde, 120), rect, 1, border_radius=tam_dinamico // 2)
            
            # Efeito de Escama Central: Um pequeno círculo interno brilhante
            centro_x = rect.x + tam_dinamico // 2
            centro_y = rect.y + tam_dinamico // 2
            raio_escama = max(2, tam_dinamico // 4)
            pygame.draw.circle(tela, VERDE_NEON, (centro_x, centro_y), raio_escama)
            
            # Se for o primeiríssimo gomo (a pontinha do rabo), adiciona um detalhe de "chocalho"
            if i == 0:
                pygame.draw.circle(tela, AMARELO_NEON, (centro_x, centro_y), raio_escama + 1, 1)

# ── PARTÍCULAS ────────────────────────────────────────────────────────
particulas = []

def criar_explosao(x, y, cor):
    for _ in range(18):
        vel_x = random.uniform(-5, 5)
        vel_y = random.uniform(-5, 5)
        tam_p = random.randint(3, 7)
        vida  = random.randint(12, 22)
        particulas.append([x + tamanho//2, y + tamanho//2, vel_x, vel_y, tam_p, vida, cor])

def atualizar_e_desenhar_particulas():
    for p in particulas[:]:
        p[0] += p[2]
        p[1] += p[3]
        p[5] -= 1
        if p[5] <= 0:
            particulas.remove(p)
        else:
            raio = max(1, int(p[4] * (p[5] / 22)))
            pygame.draw.circle(tela, p[6], (int(p[0]), int(p[1])), raio)

# ── RECORDE ───────────────────────────────────────────────────────────
ARQUIVO_RECORDE = "recorde.txt"
if os.path.exists(ARQUIVO_RECORDE):
    with open(ARQUIVO_RECORDE, "r") as f:
        try:    recorde = int(f.read())
        except: recorde = 0
else:
    recorde = 0

# ── ESTADO DO JOGO ────────────────────────────────────────────────────
cobra_x     = LARGURA // 2
cobra_y     = ALTURA  // 2
dx          = tamanho
dy          = 0
cobra_corpo = []
comprimento = 5
comida_x    = random.randrange(0, LARGURA, tamanho)
comida_y    = random.randrange(0, ALTURA,  tamanho)

def reiniciar_jogo():
    global cobra_x, cobra_y, dx, dy, cobra_corpo, comprimento, comida_x, comida_y, particulas, velocidade_atual
    cobra_x          = LARGURA // 2
    cobra_y          = ALTURA  // 2
    dx               = tamanho
    dy               = 0
    cobra_corpo      = []
    comprimento      = 5
    particulas       = []
    velocidade_atual = VELOCIDADE_INICIAL
    comida_x         = random.randrange(0, LARGURA, tamanho)
    comida_y         = random.randrange(0, ALTURA,  tamanho)

# ── 🎬 TELA DE ABERTURA ───────────────────────────────────────────────
def mostrar_tela_abertura():
    # Toca a música da abertura em loop infinito (-1)
    musica_abertura.play(loops=-1)
    
    relogio_piscar = 0
    esperando = True
    while esperando:
        tela.fill(PRETO)
        desenhar_fundo()
        
        # Título centralizado com brilho
        txt_titulo = fonte_titulo.render("SNAKE NEON", True, AZUL_NEON)
        rect_titulo = txt_titulo.get_rect(center=(LARGURA//2, ALTURA//3))
        desenhar_brilho(tela, AZUL_NEON, rect_titulo, raio=20)
        tela.blit(txt_titulo, rect_titulo)
        
        # Texto de instrução piscante
        relogio_piscar += 1
        if (relogio_piscar // 20) % 2 == 0:
            txt_start = fonte_subtitulo.render("Pressione [ESPAÇO] para Jogar", True, VERDE_NEON)
            tela.blit(txt_start, (LARGURA//2 - txt_start.get_width()//2, ALTURA//2 + 50))
            
        txt_creditos = fonte_hud.render("[ESC] Sair", True, ROXO_NEON)
        tela.blit(txt_creditos, (LARGURA//2 - txt_creditos.get_width()//2, ALTURA - 80))
        
        pygame.display.update()
        clock.tick(30)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    musica_abertura.stop() # Para a música antes de iniciar o jogo
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()

def mostrar_tela_game_over(pontuacao_final):
    global recorde

    if som_game_over:
        som_game_over.play()

    if pontuacao_final > recorde:
        recorde = pontuacao_final
        with open(ARQUIVO_RECORDE, "w") as f:
            f.write(str(recorde))

    esperando = True
    while esperando:
        tela.fill(PRETO)

        txt_go  = fonte_titulo.render("GAME OVER", True, VERMELHO_NEON)
        txt_pts = fonte_subtitulo.render(f"Sua Pontuação: {pontuacao_final}", True, BRANCO)
        txt_rec = fonte_subtitulo.render(f"Recorde Máximo: {recorde}", True, ROXO_NEON)
        txt_ins = fonte_hud.render("[ESPAÇO] reiniciar   [ESC] sair", True, AZUL_NEON)

        tela.blit(txt_go,  (LARGURA//2 - txt_go.get_width()//2,  160))
        tela.blit(txt_pts, (LARGURA//2 - txt_pts.get_width()//2, 265))
        tela.blit(txt_rec, (LARGURA//2 - txt_rec.get_width()//2, 315))
        tela.blit(txt_ins, (LARGURA//2 - txt_ins.get_width()//2, 420))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_jogo()
                    esperando = False
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit(); exit()

# ── LOOP PRINCIPAL ────────────────────────────────────────────────────

# Executa a tela de abertura antes de entrar no jogo pela primeira vez
mostrar_tela_abertura()

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            mudou_direcao = False
            if evento.key == pygame.K_UP    and dy == 0: dx = 0;        dy = -tamanho; mudou_direcao = True
            elif evento.key == pygame.K_DOWN  and dy == 0: dx = 0;        dy =  tamanho; mudou_direcao = True
            elif evento.key == pygame.K_LEFT  and dx == 0: dx = -tamanho; dy = 0;        mudou_direcao = True
            elif evento.key == pygame.K_RIGHT and dx == 0: dx =  tamanho; dy = 0;        mudou_direcao = True
            
            if mudou_direcao and som_mover:
                som_mover.play()

    cobra_x += dx
    cobra_y += dy

    # MODO SEM PAREDES
    if cobra_x < 0:
        cobra_x = LARGURA - tamanho
    elif cobra_x >= LARGURA:
        cobra_x = 0
        
    if cobra_y < 0:
        cobra_y = ALTURA - tamanho
    elif cobra_y >= ALTURA:
        cobra_y = 0

    cobra_cabeca = [cobra_x, cobra_y]
    pontuacao    = comprimento - 5

    # Colisão contra o próprio corpo
    if cobra_cabeca in cobra_corpo[:-1]:
        mostrar_tela_game_over(pontuacao)
        continue

    cobra_corpo.append(cobra_cabeca)
    if len(cobra_corpo) > comprimento:
        del cobra_corpo[0]

    # Comeu a comida
    if cobra_x == comida_x and cobra_y == comida_y:
        criar_explosao(comida_x, comida_y, AMARELO_NEON)
        
        if som_comer:
            som_comer.play()
            
        comida_x = random.randrange(0, LARGURA, tamanho)
        comida_y = random.randrange(0, ALTURA,  tamanho)
        comprimento += 1
        velocidade_atual += 0.4

    # ── DESENHO ──
    desenhar_fundo()
    desenhar_comida(comida_x, comida_y)
    desenhar_cobra(cobra_corpo)
    atualizar_e_desenhar_particulas()

    # HUD
    txt_score = fonte_hud.render(f"SCORE: {pontuacao:03d}", True, AZUL_NEON)
    txt_hi    = fonte_hud.render(f"HI:    {recorde:03d}",  True, ROXO_NEON)
    tela.blit(txt_score, (20, 15))
    tela.blit(txt_hi,    (LARGURA - txt_hi.get_width() - 20, 15))

    pygame.display.update()
    clock.tick(int(velocidade_atual))

pygame.quit() 