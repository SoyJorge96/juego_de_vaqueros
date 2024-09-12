import pygame
import random

ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
velocidad_bala = 5

pygame.mixer.init() 

# Cargar sonidos
sonido_disparo = pygame.mixer.Sound('sonidos/disparo.wav')  
pygame.mixer.music.load('sonidos/viejo_oeste.mp3') 
pygame.mixer.music.set_volume(0.5) 
pygame.mixer.music.play(-1)  


class Personaje:
    def __init__(self, x, y, imagen, velocidad_movimiento):
        self.x = x
        self.y = y
        self.imagen = imagen
        self.ancho = imagen.get_width()
        self.alto = imagen.get_height()
        self.bala = None
        self.puede_disparar = True
        self.velocidad_movimiento = velocidad_movimiento
        self.tiempo_entre_disparos = 1000 
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()

    def mover(self, direccion,posiciones):
        idx = posiciones.index(self.x)
        if direccion == 'izquierda':
            if idx > 0:
                self.x = posiciones[idx - 1]
        elif direccion == 'derecha':
            if idx < len(posiciones) - 1:
                self.x = posiciones[idx + 1]

    def disparar(self):
        if self.puede_disparar:
            pygame.mixer.Sound.play(sonido_disparo) 
            self.bala = pygame.Rect(self.x + self.ancho // 2 - 2, self.y, 4, 10)
            self.puede_disparar = False
            self.tiempo_ultimo_disparo = pygame.time.get_ticks()

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, (self.x, self.y))

    def mover_bala(self, direccion, dificultad):
        if self.bala:
            if direccion == "arriba":
                self.bala.y -= velocidad_bala
            elif direccion == "abajo":
                self.bala.y += ((velocidad_bala * dificultad)/2)

            if self.bala.y < 0 or self.bala.y > ALTO_PANTALLA:
                self.bala = None
                self.puede_disparar = True

class Enemigo(Personaje):
    def __init__(self, x, y, dificultad, imagen):
        velocidad = 1 - dificultad / 3 
        super().__init__(x, y, imagen, velocidad)
        self.tiempo_entre_disparos = 1000  
        self.tiempo_entre_movimientos = 1000  
        self.tiempo_ultimo_disparo = pygame.time.get_ticks()
        self.tiempo_ultimo_movimiento = pygame.time.get_ticks()

    def mover(self,posiciones):
        if pygame.time.get_ticks() - self.tiempo_ultimo_movimiento > self.tiempo_entre_movimientos:
            self.x = random.choice(posiciones)
            self.tiempo_ultimo_movimiento = pygame.time.get_ticks()
            
    def disparar(self):
        if pygame.time.get_ticks() - self.tiempo_ultimo_disparo > self.tiempo_entre_disparos:
            super().disparar()
            self.tiempo_ultimo_disparo = pygame.time.get_ticks()

