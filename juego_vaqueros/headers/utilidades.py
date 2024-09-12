import pygame

def mostrar_mensaje(pantalla, texto):
    fuente = pygame.font.Font(None, 74)
    texto_render = fuente.render(texto, True, (255, 255, 255))
    pantalla.blit(texto_render, (400 - 150, 300 - 50))
    pygame.display.update()
    pygame.time.delay(2000)

def menu_opciones(pantalla):
    dificultad = 1

    mientras_ejecutando = True
    while mientras_ejecutando:
        pantalla.fill((0, 0, 0))

        fuente = pygame.font.Font(None, 74)
        texto_opciones = fuente.render("Opciones", True, (255, 255, 255))
        pantalla.blit(texto_opciones, (400 - 150, 150))

        fuente_pequeña = pygame.font.Font(None, 36)
        texto_dificultad = fuente_pequeña.render(f"Dificultad: {dificultad}", True, (255, 255, 255))
        pantalla.blit(texto_dificultad, (200, 300))

        texto_instrucciones = fuente_pequeña.render("Presiona UP/DOWN para cambiar dificultad", True, (255, 255, 255))
        pantalla.blit(texto_instrucciones, (200, 350))
        texto_empezar = fuente_pequeña.render("Presiona ENTER para Iniciar", True, (255, 255, 255))
        pantalla.blit(texto_empezar, (200, 400))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    dificultad = min(dificultad + 1, 3)
                if evento.key == pygame.K_DOWN:
                    dificultad = max(dificultad - 1, 1)
                if evento.key == pygame.K_RETURN:
                    mientras_ejecutando = False

    return dificultad
