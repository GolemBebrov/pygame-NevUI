import pygame
import numpy as np
import copy
import math
from PIL import Image
from .style import *
from .utils import *
from .color import *

default_style = Theme.DEFAULT

class Widget:
    def __init__(self,size,style:Style):
        self.size = np.array(size,dtype=np.int32)
        
        self.style = style
        self.surface = pygame.Surface(size,flags=pygame.SRCALPHA)
        self.coordinates = np.array([0,0],dtype=np.float32)
        self.__is_render = True
        self.__is_active = True
        
        self._text_baked = None
        self._text_surface = None
        self._text_rect = None
        
        self._resize_ratio = [1,1]
        
        self._events = []
        
        self.x = 0
        self.y = 0
    def add_event(self,event:Event):
        self._events.append(event)
        
    #______RENDER______________________________
    def enable_render(self):
        self.__is_render = True
    def disable_render(self):
        self.__is_render = False
    @property
    def render(self):
        return self.__is_render
    @render.getter
    def render(self):
        return self.__is_render
    @render.setter
    def render(self,value:bool):
        self.__is_render = value
    #______ACTIVE______________________________
    def activate(self):
        self.__is_active = True
    def disactivate(self):
        self.__is_active = False
    @property
    def active(self):
        return self.__is_active
    @active.getter
    def active(self):
        return self.__is_active
    @active.setter
    def active(self,value:bool):
        self.__is_active = value
    #__________________________________________
    def _event_cycle(self,type:int,*args, **kwargs):
            for event in self._events:
                if event.type == type:
                    event(*args, **kwargs)
    def resize(self,_resize_ratio):
        self._resize_ratio = _resize_ratio
        self.surface = pygame.Surface([int(self.size[0]*self._resize_ratio[0]),int(self.size[1]*self._resize_ratio[1])],flags=pygame.SRCALPHA)
        self._event_cycle(Event.RESIZE)
    @property
    def style(self):
        return self._style
    @style.setter
    def style(self,style:Style):
        self._style = copy.copy(style)
        
    def draw(self):
        if not self.render:
            return
        self._event_cycle(Event.DRAW)
        Color_Type().check_bg(self._style.bgcolor,if_transparent=lambda:self.surface.fill((0,0,0,0)),if_gradient=lambda:self._style.bgcolor(self.surface),if_value=lambda:self.surface.fill(self._style.bgcolor),bool=False)
        if self._style.borderwidth > 0:
            if not self._style.bordercolor == Color_Type.TRANSPARENT:
                pygame.draw.rect(self.surface,self._style.bordercolor,[0,0,int(self.size[0]*self._resize_ratio[0]),int(self.size[1]*self._resize_ratio[1])],self._style.borderwidth,border_radius=int(self._style.borderradius))
        if self._style.borderradius > 0:
                self.surface = RoundedSurface.create(self.surface,int(self._style.borderradius))
    def update(self,*args):
        self._event_cycle(Event.UPDATE)
    def bake_text(self,text):
        print("Bake_text called for widget:", type(self)) # Добавлено: Печать типа виджета
        print("Current fontcolor:", self._style.fontcolor) # Добавлено: Печать текущего цвета шрифта
        if self._style.fontname == "Arial":
            renderFont = pygame.font.SysFont(self._style.fontname,int(self._style.fontsize*self._resize_ratio[1]))
        else:
            renderFont = pygame.font.Font(self._style.fontname,int(self._style.fontsize*self._resize_ratio[1]))
        is_popped  =False
        line_height = renderFont.size("a")[1]
        words = list(text.strip())
        lines = []
        current_line = ""
        ifnn = False
        for word in words:
            if word == '\n':
                ifnn = True
            if ifnn:
                lines.append(current_line)
                current_line = ""
                test_line = ""
                text_size = 0
                ifnn = False
                continue
            test_line = current_line + word + ""
            text_size = renderFont.size(test_line)
            if text_size[0] > self.size[0]*self._resize_ratio[0]:
                lines.append(current_line)
                current_line = word + ""
            else:
                current_line = test_line
        lines.append(current_line)
        while len(lines)*line_height > self.size[1]*self._resize_ratio[1]:
            lines.pop(-1)
            is_popped = True
        self._text_baked = "\n".join(lines)
        if is_popped:
            self._text_baked = self._text_baked[0:-3]+"..."
        self._text_surface = renderFont.render(self._text_baked, True, self._style.fontcolor)
        print("Fontcolor after render:", self._style.fontcolor) # Добавлено: Печать цвета шрифта после рендера
        self._text_rect = self._text_surface.get_rect(center=self.surface.get_rect().center)
class Empty_Widget(Widget):
    def __init__(self, size):
        super().__init__(size, default_style)
    def draw(self):
        pass
    
class Label(Widget):
    def __init__(self,size,text,style:Style):
        super().__init__(size,style)
        self._text = ""
        self.text = text
    @property
    def text(self):
        return self.text
    @text.setter
    def text(self,text:str):
        self._text = text
        self.bake_text(text)
    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        self.bake_text(self._text)
    @property
    def style(self):
        return self._style
    @style.setter
    def style(self,style:Style):
        self._style = copy.copy(style)
        if hasattr(self,'_text'):
            self.bake_text(self._text)
    def draw(self):
        super().draw()
        if not self.render:
            return
        self.surface.blit(self._text_surface, self._text_rect)
        self._event_cycle(Event.RENDER)

class Button(Label):
    def __init__(self,fuction,text:str,size,style:Style=default_style,active:bool = True):
        super().__init__(size,text,style)
        ### Basic variables
        self.fuction = fuction
        self.active = active
    
    def update(self,*args):
        super().update(*args)
        if not self.active:
            return
        if mouse.left_fdown:
            #print(self.master_coordinates)
            self._check_for_collide_and_after()
    def _check_for_collide_and_after(self):
        if pygame.Rect([self.master_coordinates[0],self.master_coordinates[1]],self.surface.get_size()).collidepoint(mouse.pos):
            if self.fuction:
                self.fuction()
class CheckBox(Button):
    def __init__(self,on_change_fuction,state,size,style:Style,active:bool = True):
        super().__init__(lambda:on_change_fuction(state) if on_change_fuction else None,"",size,style)
        self._id = None
        self._check_box_group = None
        self.is_active = False
        self.state = state
        self.active = active
    def draw(self):
        super().draw()
        if not self.render:
            return
        if self.is_active:
            pygame.draw.rect(self.surface,(200,50,50),[0,0,self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]],border_radius=int(self._style.borderradius*(self._resize_ratio[0]+self._resize_ratio[1])/2))
        self._event_cycle(Event.RENDER)
    def _check_for_collide_and_after(self):
        if not self.active:
            return
        if pygame.Rect([self.master_coordinates[0],self.master_coordinates[1]],self.surface.get_size()).collidepoint(mouse.pos):
            if self.fuction:
                self.fuction()
                self.call_dot_group()
    def connect_to_dot_group(self,dot_group,id):
        self._id = id
        self._check_box_group = dot_group
    def call_dot_group(self):
        self._check_box_group.active = self._id

class ImageWidget(Widget):
    def __init__(self,size,image,style:Style):
        super().__init__(size,style)
        self.image_orig = image
        self.image = self.image_orig
        self.resize([1,1])
    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        self.image = pygame.transform.scale(self.image_orig,(self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]))
        
    def draw(self):
        if not self.render:
            return
        self._event_cycle(Event.DRAW)
        self.surface.blit(self.image,[0,0])
        if self._style.borderradius > 0:
            self.surface = RoundedSurface.create(self.surface,int(self._style.borderradius))
        self._event_cycle(Event.RENDER)
class GifWidget(Widget):
    def __init__(self,size,gif_path=None,style:Style=default_style,frame_duration=100):
        """
        Инициализирует виджет для отображения GIF-анимации.

        Args:
            coordinates (list): Координаты виджета [x, y].
            surf (pygame.Surface): Поверхность, на которой будет отображаться виджет.
            size (list, optional): Размеры виджета [ширина, высота]. Defaults to [100, 100].
            borderradius (int, optional): Радиус скругления углов. Defaults to 0.
            gif_path (str, optional): Путь к GIF-файлу. Defaults to None.
            frame_duration (int, optional): Длительность одного кадра в миллисекундах. Defaults to 100.
        """
        super().__init__(size,style)
        self.gif_path = gif_path
        self.frames = []
        self.frame_index = 0
        self.frame_duration = frame_duration
        self.last_frame_time = 0
        self.original_size = size
        self._load_gif()
        #self.scale([1,1]) # сразу подгоняем кадры
        self.current_time = 0
        self.scaled_frames = None
        self.resize(self._resize_ratio)
    def _load_gif(self):
        """Загружает GIF-анимацию из файла."""
        if self.gif_path:
            try:
                gif = Image.open(self.gif_path)
                for i in range(gif.n_frames):
                    gif.seek(i)
                    frame_rgb = gif.convert('RGB')
                    frame_surface = pygame.image.frombuffer(frame_rgb.tobytes(), frame_rgb.size, 'RGB')
                    self.frames.append(frame_surface)
                
            except FileNotFoundError:
                print(f"Error: GIF file not found at {self.gif_path}")
            except Exception as e:
                print(f"Error loading GIF: {e}")

    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        """Изменяет размер GIF-анимации.
        Args:
            _resize_ratio (list, optional): Коэффициент масштабирования [scale_x, scale_y]. Defaults to [1, 1].
        """
        if self.frames:
            self.scaled_frames = [pygame.transform.scale(frame,[self.size[0]*self._resize_ratio[0],self.size[1]*self._resize_ratio[1]]) for frame in self.frames]


    def draw(self):
        """Отрисовывает текущий кадр GIF-анимации."""
        super().draw()
        if not self.render:
            return
        if not self.frames:
            return
        self.current_time += 1*time.delta_time*100
        if self.current_time > self.frame_duration:
             self.frame_index = (self.frame_index + 1) % len(self.frames)
             self.current_time = 0
        if self.scaled_frames:
            frame_to_draw = self.scaled_frames[self.frame_index] if hasattr(self,"scaled_frames") else self.frames[self.frame_index]
            frame_rect = frame_to_draw.get_rect(center=self.coordinates)
            self.surface.blit(frame_to_draw,(0,0))
        self._event_cycle(Event.RENDER)
        
class Input(Widget):
    def __init__(self, size, style,default:str="",placeholder:str="",blacklist=None,whitelist=None):
        super().__init__(size, style)
        self._entered_text = default
        self.selected = False
        self.bake_text(self._entered_text)
        self.blacklist = blacklist
        self.whitelist = whitelist
        self.placeholder = placeholder
    @property
    def style(self):
        return self._style
    @style.setter
    def style(self, style:Style):
        self._style = copy.copy(style)
        if hasattr(self,'_entered_text'):
            self.bake_text(self._entered_text)
        
    def bake_text(self, text):
        if self._style.fontname == "Arial":
            renderFont = pygame.font.SysFont(self._style.fontname,int(self._style.fontsize*self._resize_ratio[1]))
        else:
            renderFont = pygame.font.Font(self._style.fontname,int(self._style.fontsize*self._resize_ratio[1]))
        self.font_size = renderFont.size(text)
        self._text_surface = renderFont.render(self._entered_text, True, self.style.fontcolor)
        if not self.font_size[0]+10*self._resize_ratio[0] >= self.size[0]*self._resize_ratio[0]:
            self._text_rect = self._text_surface.get_rect(left=10*self._resize_ratio[0],centery=self.surface.get_height()/2)
        else:
            self._text_rect = self._text_surface.get_rect(right=self.surface.get_width()-10*self._resize_ratio[0],centery=self.surface.get_height()/2)
    def update(self,events:list[pygame.event.Event]):
        super().update()
        if not self.active:
            return
        self.check_selected()
        
        if self.selected:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_BACKSPACE:
                        self._entered_text = self._entered_text[:-1]
                        print([len(self._entered_text)])
                        if len(self._entered_text) == 0: 
                            self.bake_text(self.placeholder)
                        else:
                            self.bake_text(self._entered_text)
                    elif event.unicode:
                        unicode = event.unicode
                        if self.blacklist:
                            for i in range(len(self.blacklist)):
                                item = self.blacklist[i]
                                if item in unicode:
                                    unicode = unicode.replace(item,"")
                        if self.whitelist:
                            new_unicode = ""
                            for i in range(len(unicode)):
                                item = unicode[i]
                                if item in self.whitelist:
                                    new_unicode += item
                            unicode = new_unicode
                        self._entered_text += unicode
                        self.bake_text(self._entered_text)
    def check_selected(self):
        #print(pygame.Rect([self.master_coordinates[0],self.master_coordinates[1]],self.surface.get_size()),mouse.pos)
        if pygame.Rect([self.master_coordinates[0],self.master_coordinates[1]],self.surface.get_size()).collidepoint(mouse.pos) and mouse.left_fdown:
            self.selected = True
        if not pygame.Rect([self.master_coordinates[0],self.master_coordinates[1]],self.surface.get_size()).collidepoint(mouse.pos) and mouse.left_fdown:
            self.selected = False
    @property
    def text(self):
        if self._entered_text=="":
            return self.placeholder
        return self._entered_text
    @text.setter
    def text(self,text:str):
        self._entered_text = text
        self.bake_text(self._entered_text)
    
    def draw(self):
        self._event_cycle(Event.DRAW)
        super().draw()
        if not self.render:
            return
        
        self.surface.blit(self._text_surface, self._text_rect)
        self._event_cycle(Event.RENDER)
class MusicPlayer(Widget):
    def __init__(self, size, music_path, style: Style = default_style):
        super().__init__(size, style)
        pygame.mixer.init()
        self.music_path = music_path
        self.sound = pygame.mixer.Sound(music_path) 
        self.music_length = self.sound.get_length() * 1000 
        self.channel = None 
        self.start_time = 0 
        self.progress = 0
        self.side_button_size = self.size[1] / 4
        self.progress_bar_height = self.size[1] / 4
        self.cross_image = self.draw_cross()
        self.circle_image = self.draw_circle()
        self.button_image = self.circle_image
        self.button_rect = self.button_image.get_rect(center=(self.side_button_size / 2, self.side_button_size / 2))
        self.time_label = Label((size[0] - self.side_button_size * 2, 20),
                              f"{self.format_time(self.progress)}/{self.format_time(self.music_length)}",
                              style(fontsize=12, bordercolor=Color_Type.TRANSPARENT, bgcolor=Color_Type.TRANSPARENT))
        self.is_playing = False
        self.sinus_margin = 0

    def resize(self, _resize_ratio):
        super().resize(_resize_ratio)
        self.time_label.resize(_resize_ratio)
    def draw_sinusoid(self,size,frequency,margin):
        self.sinus_surf = pygame.Surface(size,pygame.SRCALPHA)
        self.sinus_surf.fill((0,0,0,0))
        for i in range(int(size[0])):
            y = abs(int(size[1] * math.sin(frequency * i+margin))) 
            y = size[1]-y
            print(y)
            pygame.draw.line(self.sinus_surf,(50,50,200),(i,size[1]),(i,y))
            
    def update(self, *args):
        super().update()
        if self.is_playing:
            self.sinus_margin+=1*time.delta_time
        if self.sinus_margin >= 100:
            self.sinus_margin = 0
        self.time_label.coordinates = [(self.size[0] / 2 - self.time_label.size[0] / 2) * self._resize_ratio[0],(self.size[1] - self.time_label.size[1]) * self._resize_ratio[1]]
        if mouse.left_fdown:
            if pygame.Rect([self.master_coordinates[0], self.master_coordinates[1]],[self.side_button_size, self.side_button_size]).collidepoint(mouse.pos):
                self.toggle_play()

        if self.is_playing:
            self.progress = pygame.time.get_ticks() - self.start_time
            if self.progress >= self.music_length:
                self.stop()
            self.time_label.text = f"{self.format_time(self.progress)}/{self.format_time(self.music_length)}"
            self.button_image = self.cross_image 
        else:
            self.button_image = self.circle_image
            if self.progress >= self.music_length:
                self.progress = 0

            self.time_label.text = f"{self.format_time(self.progress)}/{self.format_time(self.music_length)}"
    def format_time(self, milliseconds):
        total_seconds = milliseconds // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes:02}:{seconds:02}"
    def toggle_play(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()
    def play(self):
            self.channel = self.sound.play(0)
            if self.channel is not None:
                self.start_time = self.progress 
                self.is_playing = True
            else:
                print("Error: Could not obtain a channel to play the sound. Jopa also")
    def pause(self):
        if self.is_playing:
            if self.channel:
                self.channel.pause()
            self.is_playing = False
    def stop(self):
        if self.channel:
            self.channel.stop()
        self.is_playing = False
        self.progress = 0
    def draw_cross(self):
        cross_surface = pygame.Surface((self.side_button_size, self.side_button_size), pygame.SRCALPHA)
        pygame.draw.line(cross_surface, (255, 255, 255), (5, 5), (self.side_button_size - 5, self.side_button_size - 5), 3)
        pygame.draw.line(cross_surface, (255, 255, 255), (self.side_button_size - 5, 5), (5, self.side_button_size - 5), 3)
        return cross_surface

    def draw_circle(self):
        circle_surface = pygame.Surface((self.side_button_size, self.side_button_size), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, (255, 255, 255), (self.side_button_size // 2, self.side_button_size // 2),self.side_button_size // 2 - 5)
        return circle_surface

    def draw(self):
        super().draw()
        self.surface.blit(self.button_image, self.button_rect)
        progress_width = (self.size[0] / 1.2 * (self.progress / self.music_length)) * self._resize_ratio[0] if self.music_length > 0 else 0
        pygame.draw.rect(self.surface, (10, 10, 10),
                         ((self.size[0] - self.size[0] / 1.2) / 2 * self._resize_ratio[0],
                          (self.size[1] / 2 - self.progress_bar_height / 2) * self._resize_ratio[1],
                          self.size[0] / 1.2 * self._resize_ratio[0],
                          self.progress_bar_height * self._resize_ratio[1]), 0, self._style.borderradius)
        self.draw_sinusoid([progress_width,self.size[1]/17*self._resize_ratio[1]],0.15,self.sinus_margin)
        self.surface.blit(self.sinus_surf,((self.size[0] - self.size[0] / 1.2) / 2 * self._resize_ratio[0],(self.size[1] / 2 - self.sinus_surf.get_height()-self.progress_bar_height / 2) * self._resize_ratio[1]))
        pygame.draw.rect(self.surface, (50, 50, 200),
                         ((self.size[0] - self.size[0] / 1.2) / 2 * self._resize_ratio[0],
                          (self.size[1] / 2 - self.progress_bar_height / 2) * self._resize_ratio[1], progress_width,
                          self.progress_bar_height * self._resize_ratio[1]), 0, -1,0,0,self._style.borderradius,self._style.borderradius)

        self.time_label.draw()
        self.surface.blit(self.time_label.surface, self.time_label.coordinates)
        self._event_cycle(Event.RENDER)