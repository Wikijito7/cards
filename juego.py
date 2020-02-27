from lib.cartas import *
from lib.spritesheet import Spritesheet as ss
import pygame


class PartidaConGraficos(Partida):

    def __init__(self, screen, imagen):
        super().__init__()
        self.screen = screen
        self.imagen = imagen

    def obtener_imagen(self, carta, x, y):
        white = (255, 255, 255)
        black = (0, 0, 0)
        palo = ss(self.imagen).get_images((0, 0), (32, 32), 4)
        img = palo[Mazo.PALOS.index(carta.palo)]
        font = pygame.font.Font('fonts/roboto.ttf', 12)
        text = font.render(str(carta.valor), False, black)

        pygame.draw.rect(screen, white, (x, y, 40, 64))
        screen.blit(img, (x + 4, y + 16))
        screen.blit(text, (x + 2, y + 2))

    def jugar(self):
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

        ganador = None
        seguir = True
        for jugador in self.jugadores:
            jugador.mano.elimina_duplicados()
            if jugador.mano.ncartas() == 0:
                ganador = jugador
                seguir = False
                break
        turno = 1
        negro = (0, 0, 0)

        while seguir:
            screen.fill(negro)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

            y = 0
            print(f"Turno: {turno}")

            font = pygame.font.Font('fonts/roboto.ttf', 36)
            turno_texto = font.render("Turno: " + str(turno), False, (255, 255, 255))
            screen.blit(turno_texto, (0, 20))
            for jugador in self.jugadores:
                text = font.render(jugador.nombre(), False, (255, 255, 255))
                if self.jugadores.index(jugador) % 2 != 0:
                    x = 20
                else:
                    x = 400
                screen.blit(text, (x, 70 + 70 * y))
                print(f"{jugador.jugador.nombre}: {jugador.mano.ncartas()}")
                for carta in jugador.mano.cartas:
                    self.obtener_imagen(carta, x, 130 + 70 * y)
                    x += 50

                y += 1

            ja = 0
            while ja < len(self.jugadores):
                js = ja + 1
                if js >= len(self.jugadores):
                    js = 0
                self.jugadores[ja].mano.barajar()
                carta = self.jugadores[ja].mano.sacar()
                if self.jugadores[ja].mano.ncartas() == 0:
                    ganador = self.jugadores[ja]
                    seguir = False
                    break
                self.jugadores[js].mano.meter(carta)
                self.jugadores[js].mano.elimina_duplicados()
                if self.jugadores[js].mano.ncartas() == 0:
                    ganador = self.jugadores[js]
                    seguir = False
                    break
                ja += 1
            turno += 1
            pygame.display.flip()
            pygame.time.wait(1000)

        print("Juego finalizado!!!!")
        print(f"Ganador:\n{ganador}")

        while True:
            screen.fill(negro)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
            font = pygame.font.Font('fonts/roboto.ttf', 36)
            text = font.render("Ganador: " + str(ganador.nombre()), False, (255, 255, 255))

            screen.blit(text, (200, 300))
            pygame.display.flip()


if __name__ == "__main__":

    pygame.init()
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    img = pygame.image.load("img/palos.png")

    j1 = Jugador("Paula")
    j2 = Jugador("Lucia")
    j3 = Jugador("Andres")
    j4 = Jugador("Guillermo")
    j5 = Jugador("Jaime")
    j6 = Jugador("Diego")

    partida = PartidaConGraficos(screen, img)

    partida.incorpora_jugador(j1)
    partida.incorpora_jugador(j2)
    partida.incorpora_jugador(j3)
    partida.incorpora_jugador(j4)
    partida.incorpora_jugador(j5)
    partida.incorpora_jugador(j6)

    partida.jugar()

