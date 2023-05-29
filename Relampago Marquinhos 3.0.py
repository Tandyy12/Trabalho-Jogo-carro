import pygame, random
from pygame.locals import *
from pygame.sprite import *

pygame.init()

##JANELA
largura = 500
altura = 900

screen_tamanho = (largura, altura)
screen = pygame.display.set_mode(screen_tamanho)
pygame.display.set_caption('MANO WILLIAN AS QUINTAS')

#CORES PARA MAPA
cinza = (100, 100, 100)
cinzaasfalto = (56, 49, 49)
azul = (65,105,225)
azulescuro = (0,0,139)
verde = (76, 208, 56)
vermelho = (200, 0, 0)
branco = (255, 255, 255)
amarelo = (255, 232, 0)
preto = (0, 0, 0)
laranja = (255, 140, 0)

#CONTADOR PARA O MENU
batidas = 0


#ESTRADA
pista = 300
linha_larg = 10
linha_tam = 50

#POSIÇÃO PISTA
via_esquerda = 150
via_central = 250
via_direita = 350
#final_rua = 300
#começo_rua = 900
vias = [via_esquerda, via_central, via_direita]

estrada = (100, 0, pista, altura)
borda_esquerda = (70, 0, linha_tam, altura)
borda_direita = (395, 0, linha_tam, altura)

#INICIALIZADOR PARA O MOVIMENTO DA ESTRADA
movimento_estrada_y = 0

#PONTO DE INICIO
jogador_x = 250
jogador_y = 400

clock = pygame.time.Clock()
fps = 120

#CONFIGS JOGO
gameover = False
velocidade = 2
pontuação = 0


def menu_inicial():
    menu = True
    
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu = False

        # Preencha a tela do menu com a cor de fundo
        imagem_fundo = pygame.image.load("C:\\Users\\lleod\\OneDrive\\Área de Trabalho\\Trabalho Jogo\\pista.jpg")
        imagem_fundo = pygame.transform.scale(imagem_fundo, screen_tamanho)
        screen.blit(imagem_fundo, (0, 0))
        
        # Renderize o texto do nome do jogo
        fonte_titulo = pygame.font.Font(pygame.font.get_default_font(), 34)
        titulo_texto = fonte_titulo.render("Mano William as Quintas", True, vermelho)
        titulo_texto_rect = titulo_texto.get_rect()
        titulo_texto_rect.center = (largura // 2, altura // 2 - 300)
        screen.blit(titulo_texto, titulo_texto_rect)
        
        # Renderize as informações do jogo
        fonte_instrucoes = pygame.font.Font(pygame.font.get_default_font(), 24)
        instrucoes_texto1 = fonte_instrucoes.render("Use as setas para se locomover", True, preto)
        instrucoes_texto2 = fonte_instrucoes.render("Pressione Enter para começar", True, preto)
        instrucoes_texto1_rect = instrucoes_texto1.get_rect()
        instrucoes_texto2_rect = instrucoes_texto2.get_rect()
        instrucoes_texto1_rect.center = (largura // 2, altura // 2 + 30)
        instrucoes_texto2_rect.center = (largura // 2, altura // 2 + 60)
        screen.blit(instrucoes_texto1, instrucoes_texto1_rect)
        screen.blit(instrucoes_texto2, instrucoes_texto2_rect)
        
        pygame.display.update()


class Veiculos(pygame.sprite.Sprite):

  def __init__(self, image, x, y):
    pygame.sprite.Sprite.__init__(self)

    #DIMENCIONAR A IMAGEM PARA FICAR CERTO NA ESTRADA
    imagem_tamanho = 45 / image.get_rect().width
    nova_largura = image.get_rect().width * imagem_tamanho
    novo_tamanho = image.get_rect().height * imagem_tamanho
    self.image = pygame.transform.scale(image, (nova_largura, novo_tamanho))

    self.rect = self.image.get_rect()
    self.rect.center = [x, y]


class Jogador_Veiculo(Veiculos):

  def __init__(self, x, y):
    image = pygame.image.load("C:\\Users\\lleod\\OneDrive\\Área de Trabalho\\Trabalho Jogo\\car2.png")
    super().__init__(image, x, y)


#CRIAR UM GRUPO COM AS SPRITES QUE VÃO SER USADAS
jogador_group = pygame.sprite.Group()
veiculos_group = pygame.sprite.Group()

#CRIANDO O CARRO DO JOGADOR
jogador = Jogador_Veiculo(jogador_x, jogador_y)
jogador_group.add(jogador)

#CARREGAR AS IMGENS DOS VEICULOS
path_arquivos = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
veiculos_sprites = []
for path_arquivos in path_arquivos:
  image = pygame.image.load('C:\\Users\\lleod\\OneDrive\\Área de Trabalho\\Trabalho Jogo\\' + path_arquivos)
  veiculos_sprites.append(image)

#CARREGAR EXPLOSÃO
batida = pygame.image.load("C:\\Users\\lleod\\OneDrive\\Área de Trabalho\\Trabalho Jogo\\crash.png")
batida_rect = batida.get_rect()

pygame.mixer.music.load("C:\\Users\\lleod\\OneDrive\\Área de Trabalho\\Trabalho Jogo\\top gear.mp3")
pygame.mixer.music.play()

menu_inicial()
#GAME LOOP
running = True

while running:
  clock.tick(fps)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    #MOVIMENTO DIREITA E ESQUERDA
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT and jogador.rect.center[0] > via_esquerda:
        jogador.rect.x -= 100
      if event.key == pygame.K_UP:
        jogador.rect.y -= 50  
      if event.key == pygame.K_DOWN:
        jogador.rect.y += 50  
      elif event.key == pygame.K_RIGHT and jogador.rect.center[0] < via_direita:
        jogador.rect.x += 100
      

    #checar se ocorreu colisão apos mudar de faixa
    for veiculo in veiculos_group:
      if pygame.sprite.collide_rect(jogador, veiculo):

        gameover = True

        #COLOCAR UM CARRO AO LADO DO OUTRO
        #LOCALIZAÇÃO DA IMAGEM DA EXPLOSÃO
        if event.key == pygame.K_LEFT:
          jogador.rect.left = veiculo.rect.right
          batida_rect.center = [
            jogador.rect.left,
            (jogador.rect.center[1] + veiculo.rect.center[1]) / 2
          ]
        elif event.key == pygame.K_RIGHT:
          jogador.rect.right = veiculo.rect.left
          batida_rect.center = [
            jogador.rect.right,
            (jogador.rect.center[1] + veiculo.rect.center[1]) / 2
          ]

  if pontuação < 15:
    screen.fill(azul)
  if pontuação >= 16 and pontuação < 30:
    screen.fill(verde)
  if pontuação >= 31 and pontuação < 49:
    screen.fill(laranja)
  if pontuação > 50 and pontuação < 52:
    screen.fill(azulescuro)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(('C:\\Users\\lleod\\OneDrive\\Área de Trabalho\\Trabalho Jogo\\deja vu.mp3'))
    pygame.mixer.music.play()   
  elif pontuação > 52:
    screen.fill(preto)
    #pygame.mixer.music.play() REMOVI PQ TAVA PAUSANDO A MÚSICA

  pygame.draw.rect(screen, cinzaasfalto, estrada)

  pygame.draw.rect(screen, cinza, borda_esquerda)
  pygame.draw.rect(screen, cinza, borda_direita)

  #DESENHANDO MARCAS NA PISTA
  movimento_estrada_y += velocidade * 2
  if movimento_estrada_y >= linha_tam * 2:
    movimento_estrada_y = 0
  for y in range(linha_tam * -2, altura, linha_tam * 2):
    pygame.draw.rect(
      screen, branco,
      (via_esquerda + 45, y + movimento_estrada_y, linha_larg, linha_tam))
    pygame.draw.rect(
      screen, branco,
      (via_central + 45, y + movimento_estrada_y, linha_larg, linha_tam))

  jogador_group.draw(screen)

  #ADICIONANDO OS VEICULOS
  if len(veiculos_group) < 2:
    add_veiculo = True
    for veiculo in veiculos_group:
      if veiculo.rect.top < veiculo.rect.height * 1.5:
        add_veiculo = False

    if add_veiculo:
      via = random.choice(vias)

      image = random.choice(veiculos_sprites)
      veiculo = Veiculos(image, via, largura / -2)
      veiculos_group.add(veiculo)

  for veiculo in veiculos_group:
    veiculo.rect.y += velocidade

    if veiculo.rect.top >= altura:
      veiculo.kill()

      pontuação += 1

      if pontuação > 0 and pontuação % 5 == 0:
        velocidade += 1

  veiculos_group.draw(screen)

  fonte = pygame.font.Font(pygame.font.get_default_font(), 16)
  texto = fonte.render('SCORE: ' + str(pontuação), True, branco)
  texto_rect = texto.get_rect()
  texto_rect.center = (50, 400)
  screen.blit(texto, texto_rect)

  if pygame.sprite.spritecollide(jogador, veiculos_group, True):
    gameover = True
    batida_rect.center = [jogador.rect.center[0], jogador.rect.top]

  if gameover:
    screen.blit(batida, batida_rect)

    pygame.draw.rect(screen, vermelho, (0, 50, largura, 100))

    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Game over. Play again? (Enter Y or N)', True, branco)
    text_rect = text.get_rect()
    text_rect.center = (largura / 2, 100)
    screen.blit(text, text_rect)

  pygame.display.update()

  while gameover:

    clock.tick(fps)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        gameover = False
        running = False

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_y:
          gameover = False
          velocidade = 2
          pontuação = 0
          veiculos_group.empty()
          jogador.rect.center = [jogador_x, jogador_y]
          pygame.mixer.music.load("C:\\Users\\lleod\\OneDrive\\Área de Trabalho\\Trabalho Jogo\\top gear.mp3")
          pygame.mixer.music.play()

        elif event.key == pygame.K_n:
          gameover = False
          running = False
pygame.quit()


