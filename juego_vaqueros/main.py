import pygame
import random
from headers.personaje import Personaje, Enemigo
from headers.utilidades import mostrar_mensaje, menu_opciones


pygame.init()

NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255) 

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

pygame.display.set_caption("Duelo de Disparos")
pygame.mixer.init() 

reloj = pygame.time.Clock()
FPS = 60

# Configuracion del eje de movimiento 
inicio = 200
fin = 500
espacio = 50  

posiciones = list(range(inicio, fin + 1, espacio))
velocidad_bala = 5

sonido_grito = pygame.mixer.Sound('sonidos/grito.wav') 
sonido_victoria = pygame.mixer.Sound('sonidos/victoria.wav') 

# Tamaño del jugador y enemigo
ancho_deseado = 40
alto_deseado = 30

imagen_fondo = pygame.image.load('imagenes/fondo_oeste.png') 
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA)) 
imagen_jugador = pygame.image.load('imagenes/vaquero_blanco.png')
imagen_jugador = pygame.transform.scale(imagen_jugador, (ancho_deseado, alto_deseado))
imagen_enemigo = pygame.image.load('imagenes/vaquero_negro.png')
imagen_enemigo = pygame.transform.scale(imagen_enemigo, (ancho_deseado, alto_deseado))

ancho_jugador = imagen_jugador.get_width()
alto_jugador = imagen_jugador.get_height()
ancho_enemigo = imagen_enemigo.get_width()
alto_enemigo = imagen_enemigo.get_height()

def juego(dificultad):
    jugador = Personaje(posiciones[0], ALTO_PANTALLA - 3 * alto_jugador, imagen_jugador, velocidad_bala)
    enemigos = [Enemigo(posiciones[random.randint(0, len(posiciones) - 1)], alto_enemigo * 3, dificultad, imagen_enemigo) for _ in range(dificultad)]
    
    juego_terminado = False
    
    while not juego_terminado:
        pantalla.blit(imagen_fondo, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    jugador.mover('izquierda', posiciones)
                if evento.key == pygame.K_RIGHT:
                    jugador.mover('derecha', posiciones)
                if evento.key == pygame.K_SPACE and jugador.puede_disparar:
                    jugador.disparar()

        for enemigo in enemigos:
            enemigo.mover(posiciones)
            enemigo.disparar()
        
        jugador.mover_bala("arriba", 0)
        for enemigo in enemigos:
            enemigo.mover_bala("abajo", dificultad)

        enemigos_a_eliminar = []
        for enemigo in enemigos:
            if enemigo.bala and enemigo.bala.colliderect(pygame.Rect(jugador.x, jugador.y, ancho_jugador, alto_jugador)):
                pygame.mixer.Sound.play(sonido_grito) 
                mostrar_mensaje(pantalla, "Game Over")
                juego_terminado = True
                break 
        
        if jugador.bala:
            for enemigo in enemigos:
                if jugador.bala.colliderect(pygame.Rect(enemigo.x, enemigo.y, ancho_enemigo, alto_enemigo)):
                    pygame.mixer.Sound.play(sonido_victoria) 
                    enemigos_a_eliminar.append(enemigo)

        for enemigo in enemigos_a_eliminar:
            enemigos.remove(enemigo)
        
        if not enemigos:
            mostrar_mensaje(pantalla, "¡Ganaste!")
            juego_terminado = True

        jugador.dibujar(pantalla)
        for enemigo in enemigos:
            enemigo.dibujar(pantalla)
            if enemigo.bala:
                pygame.draw.rect(pantalla, BLANCO, enemigo.bala)
        
        if jugador.bala:
            pygame.draw.rect(pantalla, BLANCO, jugador.bala)

        pygame.display.update()
        reloj.tick(FPS)

while True:
    dificultad = menu_opciones(pantalla)
    juego(dificultad)
