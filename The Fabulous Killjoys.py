import pygame
from random import randint

# Dimensiones de la pantalla
ANCHO = 800
ALTO = 600
BLANCO = (255, 255, 255)
VERDE_BANDERA = (0, 122, 0)
ROJO = (255, 0, 0)
NEGRO = (0, 0, 0)

# imagenes para elementos
fondo = pygame.image.load('Fondo_Menu.jpg')
fondoAcercade = pygame.image.load('Fondo_Acercade.jpg')
btn = pygame.image.load('jugar.png')
imgbtnAcercade = pygame.image.load('button_acerca-de.png')
imgEnemigo = pygame.image.load('Draculoid.png')
imgBala = pygame.image.load('bala.png')
imgPersonaje = pygame.image.load('Personaje_.png')
pygame.mixer.init()
perdio = pygame.image.load('Fondo_Perdio.jpg')
gano = pygame.image.load('VICTORIA.jpg')


def crearEnemigos(lista):
    contador = 0
    for n in range(20):
        enemigo = pygame.sprite.Sprite()
        enemigo.image = imgEnemigo
        enemigo.rect = imgEnemigo.get_rect()
        enemigo.rect.left = enemigo.rect.width + contador
        enemigo.rect.top = 60
        contador += 50
        lista.append(enemigo)


def dibujarEnemigos(ventana, listaEnemigos):
    for enemigo in listaEnemigos:
        ventana.blit(enemigo.image, enemigo.rect)


def crearBalaRight(ventana, listaBalas):
    for bala in listaBalas:
        ventana.blit(bala.image, bala.rect)


def actualizarBalas(listaBalas):
    for bala in listaBalas:
        bala.rect.top -= 15


    for n in range(len(listaBalas) - 1, -1, -1):
        bala = listaBalas[n]
        if bala.rect.top <= - bala.rect.height:
            listaBalas.remove(bala)

def colisiones(listaBalas, listaEnemigos):
    contador = 0
    for bala in listaBalas:
        xb, yb, anchob, altob = bala.rect
        for enemigo in listaEnemigos:
            xe, ye, anchoe, altoe = enemigo.rect
            if xe <= xb <= xe + anchoe:
                if ye <= yb <= ye + altoe:
                    listaEnemigos.remove(enemigo)
                    contador += 1
        if (0 < xb < ANCHO) or (0 < yb < ALTO):
            listaBalas.remove(bala)

    return contador


def checarCapturas(listaEnemigos, spritePersonaje):
    capturas = 0
    xp, yp, anchop, altop = spritePersonaje.rect
    for enemigo in listaEnemigos:
        xe, ye, anchoe, altoe = enemigo.rect
        if xp <= xe <= xp + anchop:
            if ye + altoe >= yp:
                capturas+=1
    return capturas


def moverEnemigos(listaEnemigos):
    enemigoex = listaEnemigos[0]

    for enemigo in listaEnemigos:
        enemigo.rect.top += 10
    for n in range(len(listaEnemigos) - 1, -1, -1):
        foe = listaEnemigos[n]
        if foe.rect.top <= - foe.rect.height:
            listaEnemigos.remove(foe)
    if enemigoex.rect.top > ALTO:
        crearEnemigos(listaEnemigos)



def escribirPuntuaciones(nombre, puntuacion, resultado):
    listaEscribir = []
    dataSheet = open('puntuaciones.txt', 'w')
    anotacion = nombre + '   ' + str(puntuacion) + '   ' + resultado + ' \n'
    dataSheet.write(anotacion)
    dataSheet.close()


def TheFabulousKilljoys(nombre):
    pygame.init()
    pygame.mixer.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))  # Crea la ventana de dibujo
    reloj = pygame.time.Clock()  # Para limitar los fps
    termina = False
    estado = 'menu'
    pygame.mixer.music.load('Party Poison.mp3')
    pygame.mixer.music.play(-1, 0.0)
    listaEnemigos = []
    crearEnemigos(listaEnemigos)
    listaBalas = []

    # BTNJUGAR-------
    spritebtn = pygame.sprite.Sprite()
    spritebtn.image = btn
    spritebtn.rect = btn.get_rect()
    spritebtn.rect.left = ANCHO // 2 - spritebtn.rect.width // 2
    spritebtn.rect.top = ALTO // 2 - spritebtn.rect.height // 2 + 100

    # BTNACERCADE---------------
    spriteAcercade = pygame.sprite.Sprite()
    spriteAcercade.image = imgbtnAcercade
    spriteAcercade.rect = imgbtnAcercade.get_rect()
    spriteAcercade.rect.left = ANCHO // 2 - spriteAcercade.rect.width // 2
    spriteAcercade.rect.top = 3 * (ALTO // 4) - spriteAcercade.rect.height // 2

    # PERSONAJE------------------------
    spritePersonaje = pygame.sprite.Sprite()
    spritePersonaje.image = imgPersonaje
    spritePersonaje.rect = imgPersonaje.get_rect()
    spritePersonaje.rect.left = ANCHO//2 - spritePersonaje.rect.width
    spritePersonaje.rect.top = ALTO - spritePersonaje.rect.height

    puntuacion = 0
    while not termina:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                termina = True
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    estado = 'menu'
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if estado == 'menu':
                    x, y = pygame.mouse.get_pos()
                    xb, yb, anchob, altob = spritebtn.rect
                    xa, ya, anchoa, altoa = spriteAcercade.rect
                    if (xb + anchob >= x >= xb) and (yb + altob >= y >= yb):
                        efect = pygame.mixer.Sound('shoot.wav')
                        efect.play()
                        estado = 'juego'
                        pygame.mixer.music.load('Na Na Na.mp3')
                        pygame.mixer.music.play(-1, 0.0)
                    elif (xa + anchoa >= x >= xa) and (ya + altoa >= y >= ya):
                        efect = pygame.mixer.Sound('shoot.wav')
                        efect.play()
                        estado = 'Acerca de'

            if evento.type == pygame.KEYDOWN:
                if estado == 'juego':
                    if evento.key == pygame.K_a:
                        spritePersonaje.rect.left -= 10
                    elif evento.key == pygame.K_d:

                        spritePersonaje.rect.left += 10
                    elif evento.key == pygame.K_w:

                        spritePersonaje.rect.top -= 10
                    elif evento.key == pygame.K_s:

                        spritePersonaje.rect.top += 10
                    elif evento.key == pygame.K_SPACE:

                        efect = pygame.mixer.Sound('shoot.wav')
                        efect.play()
                        bala = pygame.sprite.Sprite()
                        bala.image = imgBala
                        bala.rect = imgBala.get_rect()
                        bala.rect.left = spritePersonaje.rect.left + spritePersonaje.rect.width//2
                        bala.rect.top = spritePersonaje.rect.top - bala.rect.height
                        listaBalas.append(bala)
                elif estado == 'Acerca de':
                    if evento.key == pygame.K_SPACE:
                        efect = pygame.mixer.Sound('shoot.wav')
                        efect.play()
                        estado = 'juego'
                    elif evento.key == pygame.K_ESCAPE:
                        efect = pygame.mixer.Sound('shoot.wav')
                        efect.play()
                        estado = 'menu'
                elif estado == ('victoria' or 'derrota' or 'Acerca de'):
                    if evento.key == pygame.K_SPACE:
                        efect = pygame.mixer.Sound('shoot.wav')
                        efect.play()
                        estado = 'juego'
                    elif evento.key == pygame.K_ESCAPE:
                        efect = pygame.mixer.Sound('shoot.wav')
                        efect.play()
                        estado = 'menu'

            if estado == 'menu':
                ventana.blit(fondo, (0, 0))
                ventana.blit(spritebtn.image, spritebtn.rect)
                ventana.blit(spriteAcercade.image, spriteAcercade.rect)
            elif estado == 'juego':
                ventana.fill(NEGRO)
                ventana.blit(spritePersonaje.image, spritePersonaje.rect)
                dibujarEnemigos(ventana, listaEnemigos)
                crearBalaRight(ventana, listaBalas)
                moverEnemigos(listaEnemigos)
                actualizarBalas(listaBalas)
                bajas = colisiones(listaBalas, listaEnemigos)
                puntuacion += bajas
                capturas = checarCapturas(listaEnemigos, spritePersonaje)
                if bajas >= 10:
                    estado = 'victoria'
                if capturas >= 1:
                    estado = 'derrota'
            elif estado == 'victoria':
                resultado = 'Gano'
                escribirPuntuaciones(nombre, puntuacion, resultado)
                ventana.fill(BLANCO)
                ventana.blit(gano, (0, 0))
            elif estado == 'derrota':
                resultado = 'perdio'
                escribirPuntuaciones(nombre, puntuacion, resultado)
                ventana.fill(NEGRO)
                ventana.blit(perdio, (0, 0))
                pygame.mixer.music.load('08 Interlude.mp3')
                pygame.mixer.music.play(-1, 0.0)
            elif estado == 'Acerca de':
                ventana.fill(NEGRO)
                ventana.blit(fondoAcercade, (0, 0))
        pygame.display.flip()
        reloj.tick(40)
    pygame.quit()


def main():

    nombre = (input('Escribe aqui abajo tu nombre, alias, gamertag o como prefieras :)\n'))
    TheFabulousKilljoys(nombre)
    print("Gracias por jugar vuelve pronto :)")

main()
