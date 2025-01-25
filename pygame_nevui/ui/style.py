import pygame
import copy

from .color import Color_Type, Color

class Style:
    def __init__(self,**kwargs):
        """
        __init__(self,**kwargs)

        Initializing a new Style object

        Supported properties:

        - bgcolor: color of the widget's background. Should be a tuple of 3 integers or a gradient object.
        - fontcolor: color of the widget's text. Should be a tuple of 3 integers.
        - bordercolor: color of the widget's border. Should be a tuple of 3 integers or a gradient object.
        - borderwidth: width of the widget's border. Should be an integer.
        - borderradius: radius of the widget's corners. Should be an integer.
        - fontname: name of the font. Should be a string.
        - fontsize: size of the font. Should be an integer.

        Raises ValueError if the property value is incorrect.

        :param kwargs: keyword arguments containing style properties
        :return: None
        """
        self.type = type
        
        self.bgcolor = (120,120,120)
        self.borderwidth = 1
        self.bordercolor = (0,0,0)
        self.borderradius = 0
        self._kwargs_for_copy = kwargs
        self._kwargs_getter(**kwargs)
        self.fontname = "Arial"
        self.fontsize = 20
        self.fontcolor=(50,50,50)
    def copy(self):
        return copy.copy(self._kwargs_for_copy)
    def _kwargs_getter(self,**kwargs):
        for name,value in kwargs.items():
            if name=="bgcolor":
                if Color_Type().check_bg(value,bool=True) == [False,False,True]:
                    if hasattr(value, '__getitem__') and hasattr(value, '__len__'):
                        if len(value) == 3:
                            if isinstance(value[0],int) and isinstance(value[1],int) and isinstance(value[2],int):
                                self.bgcolor = value
                            else:
                                raise ValueError("Color items needed to be NUMBERS.")
                        else:
                            raise ValueError("Incorrect bgcolor input.")
                    else:
                        raise ValueError("bgcolor needed to be massive.")
                elif value == Color_Type.TRANSPARENT:
                    self.bgcolor = value
            if name=="fontcolor":
                if hasattr(value, '__getitem__') and hasattr(value, '__len__'):
                    if len(value) == 3:
                        if isinstance(value[0],int) and isinstance(value[1],int) and isinstance(value[2],int):
                            self.fontcolor = value
                        else:
                            raise ValueError("Color items needed to be NUMBERS.")
                    else:
                        raise ValueError("Incorrect fontcolor input.")
                else:
                    raise ValueError("fontcolor needed to be massive.")
            if name=="bordercolor":
                if Color_Type().check_bg(value,bool=True) == [False,False,True]:
                    if hasattr(value, '__getitem__') and hasattr(value, '__len__'):
                        if len(value) == 3:
                            if isinstance(value[0],int) and isinstance(value[1],int) and isinstance(value[2],int):
                                self.bordercolor = value
                            else:
                                raise ValueError("Color items needed to be NUMBERS.")
                        else:
                            raise ValueError("Incorrect bordercolor input.")
                    else:
                        raise ValueError("bordercolor needed to be massive.")
                elif value == Color_Type.TRANSPARENT:
                    self.bordercolor = value
            if name=="borderwidth":
                if isinstance(value,int):
                    self.borderwidth = value
                else:
                    raise ValueError("borderwidth needed to be NUMBER.")
            if name=="borderradius":
                if isinstance(value,int):
                    self.borderradius = value
                else:
                    raise ValueError("borderradius needed to be NUMBER.")
            if name =="fontname":
                if isinstance(value,str):
                    self.fontname = value
                else:
                    raise ValueError("fontname needed to be STRING.")
            if name == "fontsize":
                if isinstance(value,int):
                    self.fontsize = value
                else:
                    raise ValueError("fontsize needed to be NUMBER.")
    def __call__(self,**kwargs):
        style = copy.copy(self)
        style._kwargs_getter(**kwargs)
        return style

class Align():
    CENTER = 101010
    LEFT = 111111
    RIGHT = 121212
    
class Theme:
    DEFAULT = Style()

    DARK = Style(bgcolor=Color.DARKGRAY, fontcolor=Color.LIGHTGRAY, bordercolor=Color.LIGHTGRAY)
    LIGHT = Style(bgcolor=Color.LIGHTGRAY, fontcolor=Color.DARKGRAY, bordercolor=Color.DARKGRAY)
    CUSTOM = Style(bgcolor=Color.BEIGE, fontcolor=Color.MAROON, bordercolor=Color.MAROON)
    PASTEL = Style(bgcolor=Color.LAVENDERBLUSH, fontcolor=Color.PURPLE, bordercolor=Color.PINK)
    VIBRANT = Style(bgcolor=Color.CYAN, fontcolor=Color.MAGENTA, bordercolor=Color.YELLOW)
    NATURE = Style(bgcolor=Color.PALEGREEN, fontcolor=Color.BROWN, bordercolor=Color.OLIVE)
    RETRO = Style(bgcolor=Color.LIGHTYELLOW, fontcolor=Color.BLUE, bordercolor=Color.RED)
    MINIMALIST = Style(bgcolor=Color.WHITE, fontcolor=Color.BLACK, bordercolor=Color.SILVER, borderradius=50)
    FUTURISTIC = Style(bgcolor=Color.NAVY, fontcolor=Color.AQUA, bordercolor=Color.LIME)
    WARM = Style(bgcolor=Color.PEACHPUFF, fontcolor=Color.CHOCOLATE, bordercolor=Color.ORANGE)
    COOL = Style(bgcolor=Color.LAVENDER, fontcolor=Color.TEAL, bordercolor=Color.SILVERGRAY)
    MONOCHROME = Style(bgcolor=Color.LIGHTBLACK, fontcolor=Color.SILVER, bordercolor=Color.GRAY)
    GOLD = Style(bgcolor=Color.LIGHTYELLOW, fontcolor=Color.MAROON, bordercolor=Color.GOLD)
    DEEPBLUE = Style(bgcolor=Color.NAVY, fontcolor=Color.LIGHTGRAY, bordercolor=Color.BLUE)
    FORESTGREEN = Style(bgcolor=Color.OLIVE, fontcolor=Color.LIGHTYELLOW, bordercolor=Color.GREEN)
    SUNSETORANGE = Style(bgcolor=Color.ORANGERED, fontcolor=Color.LIGHTYELLOW, bordercolor=Color.ORANGE)
