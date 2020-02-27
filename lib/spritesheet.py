import pygame


class Spritesheet:
    def __init__(self, sheet):
        self.sheet = sheet

    def get_images(self, start, size, columns, rows=1):
        """
        Recorta la imagen dada.
        :param start: donde empieza. Requiere una tupla. (0,0)
        :param size: tamaño de la subimagen en píxeles. Requiere una tupla. (0,0)
        :param columns: número de columnas de la imagen.
        :param rows: número de filas de la imagen.
        :return: lista con las imágenes.
        """
        frames = []
        for j in range(rows):
            for i in range(columns):
                location = (start[0] + size[0] * i, start[1] + size[1] * j)
                frames.append(self.sheet.subsurface(pygame.Rect(location, size)))

        return frames
