import pygame
import time as tt
import numpy as np
class RoundedSurface():
    @staticmethod
    def create(surface:pygame.SurfaceType, radius:int):
        """
        Создает копию surface с закругленными углами.

        Args:
            surface: Исходный Surface.
            radius: Радиус закругления углов.

        Returns:
            Surface с закругленными углами.
        """
        rect = surface.get_rect()
        a_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        a_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(a_surf, (255, 255, 255, 255), rect, border_radius=radius)
        new = surface.copy()
        new.blit(a_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return new
class Mouse:
    STILL= 0
    FDOWN= 1
    DOWN = 2
    UP= 3
    def __init__(self):
        self._pos = (0,0)
        
        self._left = 0
        self._right = 0
        self._center = 0
        
        self._left_up = False
        self._right_up = False
        self._center_up = False
        
        self._left_fdown = False
        self._right_fdown = False
        self._center_fdown = False
        
        self._left_down = False
        self._right_down = False
        self._center_down = False
        
        self._left_still = False
        self._right_still = False
        self._center_still = False
    
    @property
    def pos(self):
        return self._pos
    @pos.setter
    def pos(self,value):
        self._pos = value
    
    @property
    def left(self):
        return self._left
    @left.setter
    def left(self,value):
        self._left = value
    
    @property
    def right(self):
        return self._right
    @right.setter
    def right(self,value):
        self._right = value
    
    @property
    def center(self):
        return self._center
    @center.setter
    def center(self,value):
        self._center = value
    
    @property
    def left_up(self):
        return self._left_up
    @left_up.setter
    def left_up(self,value):
        self._left_up = value
    
    @property
    def left_fdown(self):
        return self._left_fdown
    @left_fdown.setter
    def left_fdown(self,value):
        self._left_fdown = value
    
    @property
    def left_down(self):
        return self._left_down
    @left_down.setter
    def left_down(self,value):
        self._left_down = value
    
    @property
    def left_still(self):
        return self._left_still
    @left_still.setter
    def left_still(self,value):
        self._left_still = value
    
    @property
    def right_up(self):
        return self._right_up
    @right_up.setter
    def right_up(self,value):
        self._right_up = value
    
    @property
    def right_fdown(self):
        return self._right_fdown
    @right_fdown.setter
    def right_fdown(self,value):
        self._right_fdown = value
    
    @property
    def right_down(self):
        return self._right_down
    @right_down.setter
    def right_down(self,value):
        self._right_down = value
    
    @property
    def right_still(self):
        return self._right_still
    @right_still.setter
    def right_still(self,value):
        self._right_still = value
    
    @property
    def center_up(self):
        return self._center_up
    @center_up.setter
    def center_up(self,value):
        self._center_up = value
    
    @property
    def center_fdown(self):
        return self._center_fdown
    @center_fdown.setter
    def center_fdown(self,value):
        self._center_fdown = value
    
    @property
    def center_down(self):
        return self._center_down
    @center_down.setter
    def center_down(self,value):
        self._center_down = value
    
    @property
    def center_still(self):
        return self._center_still
    @center_still.setter
    def center_still(self,value):
        self._center_still = value
    
    @property
    def any_down(self):
        return self.left_down or self.right_down or self.center_down
    @property
    def any_fdown(self):
        return self.left_fdown or self.right_fdown or self.center_fdown
    @property
    def any_up(self):
        return self.left_up or self.right_up or self.center_up
    
    def updateKeys(self,is_clicked,key):
        State = key
        if is_clicked:
            if State == self.FDOWN:
                State = self.DOWN
            if State != self.DOWN:
                State = self.FDOWN
        else:
            if State == self.DOWN:
                State = self.UP
            else:
                State = self.STILL
        return State
    def set_states(self,state):
        up = False
        fd = False
        dw = False
        st = False
        if state == self.STILL:
            st = True
        elif state == self.FDOWN:
            fd = True
        elif state == self.DOWN:
            dw = True
        elif state == self.UP:
            up = True
        return up,fd,dw,st
    def update(self):
        self.pos = pygame.mouse.get_pos()
        keys = pygame.mouse.get_pressed()
        self.left = self.updateKeys(keys[0],self.left)
        self.left_up,self.left_fdown,self.left_down,self.left_still = self.set_states(self.left)
        self.right = self.updateKeys(keys[2],self.right)
        self.right_up,self.right_fdown,self.right_down,self.right_still = self.set_states(self.right)
        self.center = self.updateKeys(keys[1],self.center)
        self.center_up,self.center_fdown,self.center_down,self.center_still = self.set_states(self.center)

class Time():
    def __init__(self):
        """
        Initializes the Time object with default delta time, frames per second (fps),
        and timestamps for time calculations.

        Attributes:
            delta_time/dt (float): The time difference between the current and last frame.
            fps (int): Frames per second, calculated based on delta time.
            now (float): The current timestamp.
            after (float): The timestamp of the previous frame.
        """

        self._delta_time = np.float16(1.0)
        self._fps = np.int16()
        self._now = tt.time()
        self._after = tt.time()
    @property
    def delta_time(self):
        return float(self._delta_time)
    @property
    def dt(self):
        return float(self._delta_time)
    @property
    def fps(self):
        return int(self._fps)
    def _calculate_delta_time(self):
        self._now = tt.time()
        self._delta_time = np.float16((self._now - self._after))
        self._after = self._now
    def _calculate_fps(self):
        try:
            self._fps = np.int16(int(1 / (self.delta_time)))
        except:
            self._fps = 0
    def update(self):
        self._calculate_delta_time()
        self._calculate_fps()

class Keyboard:
    def __init__(self,keys=[]):
        self.keys = keys
        #TODO: add KAKASHKE SIGMA BALLS
        raise NotImplementedError("Keyboard not implemented yet")

time = Time()
mouse = Mouse()

class Event:
    DRAW = 0
    UPDATE = 1
    RESIZE = 2
    RENDER = 3
    def __init__(self,type,function,*args, **kwargs):
        """
        Initializes an Event object with a type, function, and optional arguments.

        Parameters:
        type (int): The type of event, indicating the kind of operation.
        function (callable): The function to be executed when the event is triggered.
        *args: Variable length argument list to be passed to the function.
        **kwargs: Arbitrary keyword arguments to be passed to the function.
        """
        self.type = type
        
        self._function = function
        self._args = args
        self._kwargs = kwargs
    def __call__(self,*args, **kwargs):
        if args: self._args = args
        if kwargs: self._kwargs = kwargs
        self._function(*self._args, **self._kwargs)

class Input_Type():
    NUMBERS = "0123456789"
    LETTERS_ENG = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    LETTERS_RUS = "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
    BASIC_SYMBOLS = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"

    LETTERS_UKR = "ієїґа-яІЄЇҐА-Я"
    LETTERS_BEL = "абвгдеёжзійклмнопрстуўфхцчшыьэюяАБВГДЕЁЖЗІЙКЛМНОПРСТУЎФХЦЧШЫЬЭЮЯ"
    LETTERS_GER = "äöüÄÖÜßa-zA-Z"
    LETTERS_FR = "àâçéèêëîïôûüÿÀÂÇÉÈÊËÎÏÔÛÜŸæœÆŒa-zA-Z"
    LETTERS_ES = "áéíóúüñÁÉÍÓÚÜÑa-zA-Z"
    LETTERS_IT = "àèéìòóùÀÈÉÌÒÓÙa-zA-Z"
    LETTERS_PL = "ąćęłńóśźżĄĆĘŁŃÓŚŹŻa-zA-Z"
    LETTERS_PT = "àáâãçéêíóôõúüÀÁÂÃÇÉÊÍÓÔÕÚÜa-zA-Z"

    WHITESPACE = " \t\n\r\f\v"
    SEPARATORS_COMMON = ",.;:?!"
    SEPARATORS_BRACKETS = "()[]{}"
    SEPARATORS_QUOTES = "\"'`«»"

    MATH_SYMBOLS_BASIC = "+-*/="
    MATH_SYMBOLS_ADVANCED = "><≤≥≠≈±√∑∫"
    MATH_SYMBOLS_CURRENCY = "€£¥₽$"

    URL_SYMBOLS = "-._~:/?#[]@!$&'()*+,;=%abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    EMAIL_SYMBOLS = "-._%+-@abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

    HEX_DIGITS = "0123456789abcdefABCDEF"

    PUNCTUATION_MARKS = ",.;:?!—…"
    DASHES = "-—‒–"
    APOSTROPHE = "'"

    CONTROL_CHARS = "".join(chr(i) for i in range(32))

    MARKDOWN_SYMBOLS = "*_-`~>#+![]()="
    COMBINATIONS = ":-) :-( :D :P <3"
    SPECIAL_SYMBOLS = "©®™°№§"

    ALL_LETTERS = LETTERS_ENG + LETTERS_RUS + LETTERS_UKR + LETTERS_BEL + LETTERS_GER + LETTERS_FR + LETTERS_ES + LETTERS_IT + LETTERS_PL + LETTERS_PT
    ALL_SYMBOLS = BASIC_SYMBOLS + SEPARATORS_COMMON + SEPARATORS_BRACKETS + SEPARATORS_QUOTES + MATH_SYMBOLS_BASIC + MATH_SYMBOLS_ADVANCED + MATH_SYMBOLS_CURRENCY + PUNCTUATION_MARKS + DASHES + APOSTROPHE + MARKDOWN_SYMBOLS + SPECIAL_SYMBOLS