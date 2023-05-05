import pygame
from settings import *
from sys import exit as close_game


class Menu:
    def __init__(self, player, volume_menu):
        # general setup
        self.player = player
        self.volume_menu = volume_menu
        self.display_surface = pygame.display.get_surface()
        self.is_active = False
        self.buttons = {
            'resume': {
                'text': 'Resume',
                'func': self.resume},

            'volume': {
                'text': 'Game Volume',
                'func': self.show_volume_menu
            },

            'exit': {
                'text': 'Exit the Game',
                'func': self.exit_game},
        }
        self.buttons_nr = len(self.buttons)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # buttons creation
        self.width = WIDTH * 0.3
        self.height = HEIGHT / (self.buttons_nr + 3)
        self.create_buttons()

        # selection system
        self.selection_index = 0
        self.selection_time = None
        self.can_move = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            if keys[pygame.K_DOWN] and self.selection_index < self.buttons_nr - 1:
                self.selection_index += 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()
            elif keys[pygame.K_UP] and self.selection_index > 0:
                self.selection_index -= 1
                self.can_move = False
                self.selection_time = pygame.time.get_ticks()

            if keys[pygame.K_SPACE]:
                selected_section = self.get_item_by_index(self.selection_index)
                selected_section['func']()

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True

    def create_buttons(self):
        self.item_list = []

        for item, index in enumerate(range(self.buttons_nr)):
            # horizontal position
            left = WIDTH // 2 - self.width // 2
            # vertical position
            increment = HEIGHT // self.buttons_nr
            top = (item * increment) + (increment - self.height) // 2
            # create object
            button_text = self.get_item_by_index(index)['text']
            item = Item(left, top, self.width, self.height, index, self.font, button_text)
            self.item_list.append(item)

    def get_item_by_index(self, index):
        return self.buttons[list(self.buttons)[index]]

    def display(self):
        self.input()
        self.selection_cooldown()

        for item in self.item_list:
            item.display(self.selection_index)

    def resume(self):
        # disable attack to not hit immediately after unpause
        self.player.ability_to_attack = False
        self.player.attack_time = pygame.time.get_ticks() - 300

        self.is_active = False
        self.volume_menu.is_active = False

    def exit_game(self):
        close_game()

    def show_volume_menu(self):
        self.volume_menu.is_active = True
        self.is_active = False


class Item:
    def __init__(self, l, t, w, h, index, font, text):
        self.rect = pygame.Rect(l, t, w, h)
        self.index = index
        self.font = font
        self.text = text
        self.surface = pygame.display.get_surface()

    def display_names(self, surface, selected):
        color = TEXT_COLOR_SELECTED if selected else TEXT_COLOR

        # title
        title_surf = self.font.render(self.text, False, color)
        title_rect = title_surf.get_rect(center=self.rect.center)

        # draw
        surface.blit(title_surf, title_rect)

    def display(self, selection_num):
        if self.index == selection_num:
            pygame.draw.rect(self.surface, UPGRADE_BG_COLOR_SELECTED, self.rect)
            pygame.draw.rect(self.surface, UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(self.surface, UI_BG_COLOR, self.rect)
            pygame.draw.rect(self.surface, UI_BORDER_COLOR, self.rect, 4)
        self.display_names(self.surface, self.index == selection_num)
