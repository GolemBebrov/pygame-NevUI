import pygame
class Color_Type:
    TRANSPARENT = 101
    class Gradient:
        """
        Класс для создания градиентной поверхности.

        Атрибуты:
            START_COLOR (tuple): Константа, представляющая начальный цвет.
            END_COLOR (tuple): Константа, представляющая конечный цвет.
            HORIZONTAL (str): Константа, представляющая горизонтальное направление градиента.
            VERTICAL (str): Константа, представляющая вертикальное направление градиента.
            start_color (tuple): Начальный цвет градиента.
            end_color (tuple): Конечный цвет градиента.
            direction (str): Направление градиента (HORIZONTAL или VERTICAL).
        """
        START_COLOR = (0, 0, 0)
        END_COLOR = (255, 255, 255)
        HORIZONTAL = "horizontal"
        VERTICAL = "vertical"

        def __init__(self, start_color: tuple = START_COLOR, end_color: tuple = END_COLOR, direction: str = HORIZONTAL):
            """
            Инициализирует объект Gradient.

            Args:
                start_color (tuple, optional): Начальный цвет градиента. Defaults to START_COLOR.
                end_color (tuple, optional): Конечный цвет градиента. Defaults to END_COLOR.
                direction (str, optional): Направление градиента (HORIZONTAL или VERTICAL). Defaults to HORIZONTAL.

            Raises:
                ValueError: Если направление градиента не является HORIZONTAL или VERTICAL.
            """
            self.start_color = start_color
            self.end_color = end_color
            if direction not in (self.HORIZONTAL, self.VERTICAL):
                raise ValueError("Invalid direction. Use 'horizontal' or 'vertical'.")
            self.direction = direction
        
        def __call__(self, surface) -> pygame.Surface:
            """
            Создает поверхность с градиентным заполнением.

            Args:
                size (tuple): Размеры поверхности (ширина, высота).

            Returns:
                pygame.Surface: Поверхность с градиентным заполнением.
            """
            print("alah")
            size = surface.get_size()
            width, height = size
            
            if self.direction == self.HORIZONTAL:
                for x in range(width):
                    ratio = x / width
                    r = int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * ratio)
                    g = int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * ratio)
                    b = int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * ratio)
                    pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
            elif self.direction == self.VERTICAL:
                for y in range(height):
                    ratio = y / height
                    r = int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * ratio)
                    g = int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * ratio)
                    b = int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * ratio)
                    pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

    def check_bg(self, bg, if_transparent=None, if_gradient=None, if_value=None, bool=True):
        t = False
        g = False
        v = False
        if bg == self.TRANSPARENT:
            t = True
        if isinstance(bg, self.Gradient):
            g = True
        if not (isinstance(bg, self.Gradient) or bg == self.TRANSPARENT):
            v = True
        if bool:
            return [t, g, v]
        else:
            if t:
                if if_transparent:
                    if_transparent()
            elif g:
                if if_gradient:
                    if_gradient()
            elif v:
                if if_value:
                    if_value()

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    MAGENTA = (255, 0, 255)
    LIME = (0, 255, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    GRAY = (128, 128, 128)
    PINK = (255, 192, 203)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    BROWN = (165, 42, 42)
    SILVER = (192, 192, 192)
    GOLD = (255, 215, 0)
    PALEGREEN = (152, 251, 152)
    NAVY = (0, 0, 128)
    MAROON = (128, 0, 0)
    OLIVE = (128, 128, 0)
    TEAL = (0, 128, 128)
    AQUA = (0, 255, 255)
    LAVENDER = (230, 230, 250)
    BEIGE = (245, 245, 220)
    IVORY = (255, 255, 240)
    UKRAINE = "POOP"
    LEMONCHIFFON = (255, 250, 205)
    LIGHTYELLOW = (255, 255, 224)
    LAVENDERBLUSH = (255, 240, 245)
    MISTYROSE = (255, 228, 225)
    ANTIQUEWHITE = (250, 235, 215)
    PAPAYAWHIP = (255, 239, 213)
    BLANCHEDALMOND = (255, 235, 205)
    BISQUE = (255, 228, 196)
    PEACHPUFF = (255, 218, 185)
    NAVAJOWHITE = (255, 222, 173)
    MOCCASIN = (255, 228, 181)
    CORAL = (255, 127, 80)
    TOMATO = (255, 99, 71)
    ORANGERED = (255, 69, 0)
    DARKORANGE = (255, 140, 0)
    CHOCOLATE = (210, 105, 30)
    SADDLEBROWN = (139, 69, 19)
    LIGHTGRAY = (211, 211, 211)
    SILVERGRAY = (192, 192, 192)
    DARKGRAY = (169, 169, 169)
    LIGHTBLACK = (105, 105, 105)