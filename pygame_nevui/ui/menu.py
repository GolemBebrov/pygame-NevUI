import pygame
import copy
from .style import *
from .utils import *
from .window import Window
class Menu:
    def __init__(self,window:Window,size,style:Style): 
        self.window = window
        self.window_surface = None
        self.size = size
        self.coordinatesMW = [0,0]
        self.coordinates = [0,0]
        self.style = style
        self.surface = pygame.Surface(self.size)
        
        if not self.window:
            self.window_surface = self.window
            self.window = None
            return
        
        self.isrelativeplaced = False
        self.relx = None
        self.rely = None
        
        self.first_window_size = self.window.size
        self.first_size = size
        self.first_coordinates = [0,0]
        self.window.add_event(Event(Event.RESIZE,self.resize))
        self._resize_ratio = [1,1]
        
        self.layout = None

    def resize(self,size):
        self._resize_ratio = [size[0]/self.first_window_size[0],size[1]/self.first_window_size[1]]
        self.coordinatesMW = [self.coordinates[0]*self._resize_ratio[0]+self.window._offset[0],self.coordinates[1]*self._resize_ratio[1]+self.window._offset[1]]
        
        self.surface = pygame.Surface([self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]])
        
        if self.layout:
            self.layout.resize(self._resize_ratio)
        
        print(self._resize_ratio)
    @property
    def style(self):
        return self._style
    @style.setter
    def style(self,style:Style):
        self._style = copy.copy(style)
    
    def apply_style_to_all(self,style:Style):
        self.style = style
        if self.layout:
            self.layout.apply_style_to_all(style)
    
    def set_layout(self,layout):
        if layout._can_be_main_layout:
            layout.coordinates = (self.size[0]/2-layout.size[0]/2,self.size[1]/2-layout.size[1]/2)
            layout.connect_to_menu(self)
            self.layout = layout
        else:
            raise Exception("this Layout can't be main")
    def _set_layout_coordinates(self,layout):
        layout.coordinates = [self.size[0]/2-layout.size[0]/2,self.size[1]/2-layout.size[1]/2]
    def set_coordinates(self,x,y):
        self.coordinates = [x,y]
        self.coordinatesMW = [self.coordinates[0]*self._resize_ratio[0]+self.window._offset[0],self.coordinates[1]*self._resize_ratio[1]+self.window._offset[1]]
        
        self.isrelativeplaced = False
        self.relx = None
        self.rely = None
        
        self.first_coordinates = self.coordinates
    def set_coordinates_relative(self,relx,rely):
        self.coordinates = [self.window.size[0]/100*relx-self.size[0]/2,self.window.size[1]/100*rely-self.size[1]/2]
        self.coordinatesMW = [self.coordinates[0]*self._resize_ratio[0]+self.window._offset[0],self.coordinates[1]*self._resize_ratio[1]+self.window._offset[1]]
        
        self.isrelativeplaced = True
        self.relx = relx
        self.rely = rely

        self.first_coordinates = self.coordinates
    def draw(self):
        rect_val = [self.coordinatesMW,self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]]
        self.surface.fill(self._style.bgcolor)
        self.layout.draw()
        if self._style.borderwidth > 0:
            pygame.draw.rect(self.surface,self._style.bordercolor,[0,0,rect_val[1],rect_val[2]],int(self._style.borderwidth*(self._resize_ratio[0]+self._resize_ratio[1])/2) if int(self._style.borderwidth*(self._resize_ratio[0]+self._resize_ratio[1])/2)>0 else 1,border_radius=int(self._style.borderradius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        if self._style.borderradius > 0:
            self.surface = RoundedSurface.create(self.surface,int(self._style.borderradius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        self.window.surface.blit(self.surface,rect_val[0])
    def update(self):
        if self.layout:
            self.layout.update()
    
class Group():
    def __init__(self,items=[]):
        self.items = items
        self.enabled = True
    def update(self):
        if not self.enabled:
            return
        for item in self.items:
            item.update()
    def draw(self):
        if not self.enabled:
            return
        for item in self.items:
            item.draw()
    def step(self):
        if not self.enabled:
            return
        for item in self.items:
            item.update()
            item.draw()
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False
    def switch(self):
        self.enabled = not self.enabled