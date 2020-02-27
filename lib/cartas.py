from random import shuffle


class Carta:
    def __init__(self, palo, valor):
        self.palo = palo
        self.valor = valor

    def __str__(self):
        return f"{Mazo.VALORES[self.valor]} de {self.palo}"

    def __eq__(self, otra):
        return self.valor == otra.valor


class Mazo:
    PALOS = ["Copas", "Oros", "Bastos", "Espadas"]
    #VALORES = [None, "As", "2", "3", "4", "5", "6", "7", "Sota", "Caballo", "Rey"]
    VALORES = [None, "1", "2", "3", "4", "5", "6", "7", "Sota", "Caballo", "Rey"]

    def __init__(self, cartas=None):
        if cartas is None:
            self.cartas = []
        else:
            self.cartas = cartas

    def __str__(self):
        resultado = ""
        for carta in self.cartas:
            resultado += str(carta)+"\n"
        return resultado

    def sacar(self, n=1):
        lista_cartas = []
        for i in range(n):
            if len(self.cartas)>0:
                carta_sacada = self.cartas.pop()
                lista_cartas.append(carta_sacada)
            else:
                break
        resultado = Mazo(lista_cartas)
        return resultado

    def meter(self, otro_mazo):
        lista_cartas = otro_mazo.cartas
        self.cartas.extend(lista_cartas)

    def crear_baraja(self):
        for palo in Mazo.PALOS:
            for i in range(1, len(Mazo.VALORES)):
                nueva_carta = Carta(palo, i)
                self.cartas.append(nueva_carta)

    def barajar(self):
        shuffle(self.cartas)

    def ncartas(self):
        return len(self.cartas)

    def hay_duplicados(self):
        for i in range(len(self.cartas)-1):
            if self.cartas[i] in self.cartas[i+1:]:
                return True
        return False

    def elimina_duplicados(self):
        while self.hay_duplicados():
            for i in range(len(self.cartas)-1):
                try:
                    pos = self.cartas[i+1:].index(self.cartas[i])
                    del self.cartas[i+1+pos]
                    del self.cartas[i]
                    break
                except ValueError:
                    continue


class Jugador:
    def __init__(self, nombre, puntos=0):
        self.nombre = nombre
        self.puntos = puntos

    def __str__(self):
        return f"{self.nombre} ({self.puntos})"


class JugadorPartida:
    def __init__(self, jugador, orden, puntuacion, mano):
        self.jugador = jugador
        self.orden = orden
        self.puntuacion = puntuacion
        self.mano = mano

    def __str__(self):
        return f"{str(self.jugador)}\nOrden: {self.orden}\nPuntuacion: {self.puntuacion}\nCartas en la mano:\n{str(self.mano)}"

    def recibir(self, mazo):
        self.mano.meter(mazo)

    def nombre(self):
        return self.jugador.nombre

    def obtener_cartas(self):
        return self.mano.cartas


class Partida:
    def __init__(self, jugadores=None):
        if jugadores is None:
            self.jugadores = []
        else:
            self.jugadores = jugadores
        self.mazo = Mazo()
        self.mazo.crear_baraja()
        self.mazo.barajar()

    def __str__(self):
        resultado = "Jugadores:\n"
        for jugador in self.jugadores:
            resultado += str(jugador) + "\n"
        resultado += "Cartas en el mazo:\n" + str(self.mazo)
        return resultado

    def incorpora_jugador(self, jugador):
        orden = len(self.jugadores)+1
        mano = Mazo()
        nuevo_jugador = JugadorPartida(jugador,orden,0,mano)
        self.jugadores.append(nuevo_jugador)
    # Gestiona la partida

    def jugar(self):
        if len(self.jugadores)<2 or len(self.jugadores)>10:
            print("No se puede jugar con ese número de jugadores")
            return
        # Repartir las cartas
        nc = self.mazo.ncartas() // len(self.jugadores)
        for jugador in self.jugadores:
            jugador.recibir(self.mazo.sacar(nc))
        for jugador in self.jugadores:
            if self.mazo.ncartas() == 0:
                break
            jugador.recibir(self.mazo.sacar())
        # Juego preparado
        # # Mostramos las cartas repartidas
        # for jugador in self.jugadores:
        #     print(jugador)
        # Quitamos las cartas duplicadas de las manos de los jugadores
        # y comprobamos que no se quedan sin cartas...
        ganador = None
        seguir = True
        for jugador in self.jugadores:
            jugador.mano.elimina_duplicados()
            if jugador.mano.ncartas() == 0:
                ganador = jugador
                seguir = False
                break
        turno = 1
        # Bucle de turnos
        # TODO: Refactorizar para evitar acoplamiento provocado
        # por el acceso abusivo a los atributos de jugador_partida 
        while seguir:
            # Turno
            print(f"Turno: {turno}")
            for jugador in self.jugadores:
                print(f"{jugador.jugador.nombre}: {jugador.mano.ncartas()}")
            ja = 0
            while ja < len(self.jugadores):
                js = ja+1
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
        
        # Imprimr el resultado
        print("Juego finalizado!!!!")
        print(f"Ganador:\n{ganador}")


# Ejemplo de herencia, no es funcional
class PartidaBrisca(Partida):
    def __init__(self):
        Partida.__init__(self)
        self.triunfo = self.mazo.sacar()


if __name__ == "__main__":
    j1 = Jugador("Paula")
    j2 = Jugador("Lucia")
    j3 = Jugador("Andres")
    j4 = Jugador("Guillermo")
    j5 = Jugador("Jaime")
    j6 = Jugador("Diego")
    mi_partida = Partida()
    mi_partida.incorpora_jugador(j1)
    mi_partida.incorpora_jugador(j2)
    mi_partida.incorpora_jugador(j3)
    mi_partida.jugar()