import pygame
import random
import sys

#inciar pygame
pygame.init()

#conf pantalla
ancho_pantalla, alto_pantalla = 800, 600
pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
pygame.display.set_caption("Esquiva los Asteroides")

#conf colores
blanco = (255, 255, 255)
negro = (0, 0, 0)
rojo = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)

#triempo y fps
reloj = pygame.time.Clock()
fps = 60
duracion_nivel = 60  # Duración de cada nivel en segundos

#fuente
fuente = pygame.font.Font(None, 36)

#variables juego
nivel_actual = 1
velocidades_asteroides = [10, 15, 20] 
juego_pausado = False  
tiempo_inicio_juego = 0  

#funciones
def objetos_texto(texto, fuente, color=negro):
    superficieTexto = fuente.render(texto, True, color)
    return superficieTexto, superficieTexto.get_rect()

def boton(mensaje, x, y, ancho, alto, color_inactivo, color_activo, accion=None):
    raton = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    pygame.draw.rect(pantalla, color_activo if x + ancho > raton[0] > x and y + alto > raton[1] > y else color_inactivo, (x, y, ancho, alto))
    superficieTexto, rectTexto = objetos_texto(mensaje, fuente)
    rectTexto.center = (x + (ancho / 2), y + (alto / 2))
    pantalla.blit(superficieTexto, rectTexto)

    if click[0] == 1 and x + ancho > raton[0] > x and y + alto > raton[1] > y and accion is not None:
        pygame.time.wait(300)  # Pequeña espera para evitar dobles clics/acciones
        accion()

def detectar_colision(pos_jugador, pos_asteroide, tamaño_jugador, tamaño_asteroide):
    p_x, p_y = pos_jugador
    a_x, a_y = pos_asteroide
    if (a_x >= p_x and a_x < (p_x + tamaño_jugador)) or (p_x >= a_x and p_x < (a_x + tamaño_asteroide)):
        if (a_y >= p_y and a_y < (p_y + tamaño_jugador)) or (p_y >= a_y and p_y < (a_y + tamaño_asteroide)):
            return True
    return False

def salir_juego():
    pygame.quit()
    sys.exit()

def mostrar_temporizador(nivel_actual, tiempo_transcurrido):
    tiempo_restante = duracion_nivel - (tiempo_transcurrido % duracion_nivel)
    texto_temporizador = fuente.render(f"Tiempo: {int(tiempo_restante)}s Nivel: {nivel_actual}", True, blanco)
    pantalla.blit(texto_temporizador, (10, 10))

def menu_pausa():
    global juego_pausado
    while juego_pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
                
        pantalla.fill(negro)
        textoGrande = pygame.font.Font('freesansbold.ttf', 55)
        superficieTexto, rectTexto = objetos_texto("Juego Pausado", textoGrande, blanco)
        rectTexto.center = ((ancho_pantalla / 2), (alto_pantalla / 3))
        pantalla.blit(superficieTexto, rectTexto)

        boton("Reanudar", 150, 450, 100, 50, verde, rojo, alternar_pausa)
        boton("Salir al Menú", 550, 450, 100, 50, verde, rojo, menu_inicio)

        pygame.display.update()
        reloj.tick(15)

def alternar_pausa():
    global juego_pausado
    juego_pausado = not juego_pausado

def menu_inicio():
    intro = True

    while intro:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
                
        pantalla.fill(blanco)
        textoGrande = pygame.font.Font('freesansbold.ttf', 55)
        superficieTexto, rectTexto = objetos_texto("Esquiva Asteroides", textoGrande, azul)
        rectTexto.center = ((ancho_pantalla / 2), (alto_pantalla / 3))
        pantalla.blit(superficieTexto, rectTexto)

        boton("¡Jugar!", 150, 450, 100, 50, verde, rojo, juego)
        boton("Salir", 550, 450, 100, 50, verde, rojo, salir_juego)

        pygame.display.update()
        reloj.tick(15)

#juego
def juego():
    global nivel_actual, juego_pausado, tiempo_inicio_juego
    tamaño_jugador = 50
    pos_jugador = [ancho_pantalla / 10, alto_pantalla / 2]
    velocidad_jugador = 10

    tamaño_asteroide = 50
    asteroides = []
    tiempo_inicio_juego = pygame.time.get_ticks()
    puntaje = 0
    juego_pausado = False
    nivel_actual = 1

    while True:
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - tiempo_inicio_juego) / 1000

        if tiempo_transcurrido >= duracion_nivel * nivel_actual:
            nivel_actual = min(nivel_actual + 1, 3)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir_juego()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    alternar_pausa()

        if juego_pausado:
            menu_pausa()
            continue

        pantalla.fill(negro)

        if random.random() < 0.02:
            asteroides.append([ancho_pantalla, random.randint(0, alto_pantalla - tamaño_asteroide)])
        for asteroide in asteroides:
            asteroide[0] -= velocidades_asteroides[nivel_actual - 1]
            if asteroide[0] < 0:
                asteroides.remove(asteroide)
                puntaje += 1
            pygame.draw.rect(pantalla, rojo, (asteroide[0], asteroide[1], tamaño_asteroide, tamaño_asteroide))
            if detectar_colision(pos_jugador, asteroide, tamaño_jugador, tamaño_asteroide):
                menu_inicio()  # Volver al menú principal después de colisionar

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] and pos_jugador[1] > 0:
            pos_jugador[1] -= velocidad_jugador
        if teclas[pygame.K_DOWN] and pos_jugador[1] < alto_pantalla - tamaño_jugador:
            pos_jugador[1] += velocidad_jugador
        pygame.draw.rect(pantalla, blanco, (pos_jugador[0], pos_jugador[1], tamaño_jugador, tamaño_jugador))

        mostrar_temporizador(nivel_actual, tiempo_transcurrido)

        pygame.display.update()
        reloj.tick(fps)

menu_inicio()