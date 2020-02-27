import pygame, keyboard

from lib.cartas import *
from lib.spritesheet import Spritesheet as ss


class PartidaConGraficos(Partida):

    def __init__(self, screen, imagen):
        super().__init__()
        self.screen = screen
        self.imagen = imagen
        self.ganador = None
        self.turno = 0

    def generar_supuestos_graficos(self, jugadores):
        white = (255, 255, 255)
        black = (0, 0, 0)
        y = 1
        self.screen.fill(black)

        text_font = pygame.font.Font('fonts/roboto.ttf', 24)
        text = text_font.render("Turno :" + str(self.turno), False, (255, 255, 255))

        for jugador in jugadores:
            cond = self.jugadores.index(jugador) < len(self.jugadores)//2
            if cond:
                x = 20
            else:
                x = 600

            text_font = pygame.font.Font('fonts/roboto.ttf', 24)
            text = text_font.render(jugador.nombre(), False, (255, 255, 255))

            if y <= len(self.jugadores)//2:
                carta_y = 50 + (110 * y)
                self.screen.blit(text, (x, 20 + 110 * y))
            else:
                carta_y = 50 + 770 - (110 * y)
                self.screen.blit(text, (x, 20 + 770 - (110 * y)))

            for carta in jugador.obtener_cartas():
                palo = ss(self.imagen).get_images((0, 0), (32, 32), 4)
                img = palo[Mazo.PALOS.index(carta.palo)]
                font = pygame.font.Font('fonts/roboto.ttf', 12)
                text = font.render(str(carta.valor), False, black)
                pygame.draw.rect(screen, white, (x, carta_y, 40, 64))
                self.screen.blit(img, (x + 4, carta_y + 16))
                self.screen.blit(text, (x + 2, carta_y + 2))
                x += 50

            y += 1

    def obtener_ganador(self):
        return self.ganador

    def repartir_cartas(self):
        self.ganador = None
        if len(self.jugadores) < 2 or len(self.jugadores) > 10:
            print("No se puede jugar con ese número de jugadores")
            return

        nc = self.mazo.ncartas() // len(self.jugadores)

        for jugador in self.jugadores:
            jugador.recibir(self.mazo.sacar(nc))

        for jugador in self.jugadores:
            if self.mazo.ncartas() == 0:
                break
            jugador.recibir(self.mazo.sacar())

        for jugador in self.jugadores:
            jugador.mano.elimina_duplicados()
            if jugador.mano.ncartas() == 0:
                self.ganador = jugador
                break
        self.generar_supuestos_graficos(self.jugadores)

    def jugar(self):
        ja = 0
        while ja < len(self.jugadores):
            js = ja + 1
            if js >= len(self.jugadores):
                js = 0
            self.jugadores[ja].mano.barajar()
            carta = self.jugadores[ja].mano.sacar()
            self.jugadores[js].mano.meter(carta)
            if self.jugadores[ja].mano.ncartas() == 0:
                self.ganador = self.jugadores[ja]
                break

            self.jugadores[js].mano.elimina_duplicados()
            if self.jugadores[js].mano.ncartas() == 0:
                self.ganador = self.jugadores[js]
                break
            ja += 1
            self.generar_supuestos_graficos(self.jugadores)
            pygame.display.flip()
            pygame.time.wait(200)

        self.generar_supuestos_graficos(self.jugadores)
        pygame.display.flip()
        self.turno += 1
        pygame.time.wait(1000)


def iniciar_partida(imagen, pantalla):
    jg1 = Jugador("Paula")
    jg2 = Jugador("Lucia")
    jg3 = Jugador("Andres")
    jg4 = Jugador("Guillermo")
    jg5 = Jugador("Jaime")
    jg6 = Jugador("Diego")
    jg7 = Jugador("Mariela")
    jg8 = Jugador("Shayma")

    partida = PartidaConGraficos(pantalla, imagen)

    partida.incorpora_jugador(jg1)
    partida.incorpora_jugador(jg2)
    partida.incorpora_jugador(jg3)
    partida.incorpora_jugador(jg4)
    partida.incorpora_jugador(jg5)
    partida.incorpora_jugador(jg6)
    partida.incorpora_jugador(jg7)
    partida.incorpora_jugador(jg8)


    return partida


if __name__ == "__main__":

    pygame.init()
    size = (1200, 800)
    screen = pygame.display.set_mode(size)
    img = pygame.image.load("img/palos.png")

    partida_actual = iniciar_partida(img, screen)
    partida_actual.repartir_cartas()

    automatico = False
    hay_ganador = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

        if hay_ganador and keyboard.is_pressed("c"):
            hay_ganador = False
            partida_actual = iniciar_partida(img, screen)
            partida_actual.repartir_cartas()
            automatico = False

        if hay_ganador:
            screen.fill((0, 0, 0))
            text_font = pygame.font.Font('fonts/roboto.ttf', 32)
            text = text_font.render("Ganador: " + partida_actual.obtener_ganador().nombre(), False, (255, 255, 255))
            screen.blit(text, (400, 400))

        if keyboard.is_pressed("n"):
            if partida_actual.obtener_ganador() is None:
                screen.fill((0, 0, 0))
                partida_actual.jugar()
                automatico = False
            else:
                hay_ganador = True

        if keyboard.is_pressed("v"):
            automatico = True

        if automatico:
            if partida_actual.obtener_ganador() is None:
                screen.fill((0, 0, 0))
                partida_actual.jugar()
            else:
                hay_ganador = True
        pygame.display.flip()
