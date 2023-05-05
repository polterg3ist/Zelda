import pygame
from settings import *


class VolumeMaster:
    def __init__(self, visible_sprites):
        # general setup
        self.sprites = [sprite for sprite in visible_sprites.sprites() if sprite.sprite_type == 'enemy']
        # sounds volume
        self.main_theme_volume = 0.2
        self.game_volume = 0.2

        # sounds
        self.main_theme = pygame.mixer.Sound('../audio/main.ogg')
        self.game_sounds = {
            "hit": pygame.mixer.Sound('../audio/hit.wav'),
            "sword": pygame.mixer.Sound('../audio/sword.wav'),
            "death": pygame.mixer.Sound('../audio/death.wav'),
            "flame": pygame.mixer.Sound('../audio/flame.wav'),
            "heal": pygame.mixer.Sound('../audio/heal.wav'),
            "claw": pygame.mixer.Sound('../audio/attack/claw.wav'),
            "thunder": pygame.mixer.Sound('../audio/attack/fireball.wav'),
            "slash": pygame.mixer.Sound('../audio/attack/slash.wav'),
            "leaf_attack": pygame.mixer.Sound('../audio/attack/slash.wav')
        }

        self.change_volume()

    def change_volume(self):
        self.main_theme.set_volume(self.main_theme_volume)
        for sound in self.game_sounds:
            self.game_sounds[sound].set_volume(self.game_volume)

    def trigger(self, operation_type, index):
        volume = self.main_theme_volume if index == 0 else self.game_volume
        if operation_type == 'increase':
            if volume < 1:
                volume += 0.1
                if volume > 1:
                    volume = 1
        else:
            if volume > 0:
                volume -= 0.1
                if volume < 0:
                    volume = 0

        if index == 0:
            self.main_theme_volume = volume
        else:
            self.game_volume = volume


class VolumeMenu:
    def __init__(self, volume_master):
        # general setup
        self.volume_master = volume_master
        self.is_active = False
        self.display_surface = pygame.display.get_surface()

        # calculating coordinates
        self.width = WIDTH * 0.3
        self.height = HEIGHT // 5
        self.main_theme_btn_y = (HEIGHT // 2) - (self.height * 1.25)
        self.game_volume_btn_y = self.main_theme_btn_y + (self.height * 1.5)
        self.buttons_x = WIDTH // 2 - self.width // 2

        # item creation
        self.main_theme_btn = Button(self.buttons_x, self.main_theme_btn_y,
                                     self.width, self.height, 0, "Main Theme Volume")

        self.game_volume_btn = Button(self.buttons_x, self.game_volume_btn_y,
                                      self.width, self.height, 1, "Game Volume")

        self.buttons = (self.main_theme_btn, self.game_volume_btn)

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_DOWN] and self.selection_index < 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_LEFT]:
                self.volume_master.trigger('decrease', self.selection_index)
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.volume_master.change_volume()
            elif keys[pygame.K_RIGHT]:
                self.volume_master.trigger('increase', self.selection_index)
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
                self.volume_master.change_volume()

            #print(self.volume_master.main_theme_volume, self.volume_master.game_volume)

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def display(self):
        self.input()
        self.selection_cooldown()

        # display buttons
        for index, button in enumerate(self.buttons):
            if index == 0:
                value = self.volume_master.main_theme_volume
            else:
                value = self.volume_master.game_volume
            print(value)
            button.display(self.selection_index, value)


class Button:
    def __init__(self, l, t, w, h, index, text):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.text = text
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.surface = pygame.display.get_surface()

    def display_names(self, surface, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render(self.text, False, color)
        title_rect = title_surf.get_rect(midtop=self.rect.midtop + pygame.math.Vector2(0, 25))

        # draw
        surface.blit(title_surf, title_rect)

    def display_bar(self, surface, value, selected):

        # drawing setup
        left = self.rect.midleft + pygame.math.Vector2(60, 0)
        right = self.rect.midright - pygame.math.Vector2(60, 0)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        # bar setup
        full_width = right[0] - left[0]
        relative_number = (value / 1) * full_width
        value_rect = pygame.Rect(left[0] + relative_number, left[1] - 15, 10, 30)

        # draw elements
        pygame.draw.line(surface, color, left, right, 5)
        pygame.draw.rect(surface, color, value_rect)

    def display(self, selection_num, value):
        if self.index == selection_num:
            pygame.draw.rect(self.surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(self.surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(self.surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(self.surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(self.surface, self.index == selection_num)
        self.display_bar(self.surface, value, self.index == selection_num)
