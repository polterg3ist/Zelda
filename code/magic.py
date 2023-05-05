import pygame
from settings import *
from random import randint


class MagicPlayer:
    def __init__(self, animation_player, volume_master):
        self.animation_player = animation_player
        self.sounds = {
            'heal': volume_master.game_sounds['heal'],
            'flame': volume_master.game_sounds['flame'],
        }

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost:
            self.sounds['heal'].play()
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats['health']:
                player.health = player.stats['health']
            self.animation_player.create_particles('aura', player.rect.center, groups)
            heal_offset = pygame.math.Vector2(0, 60)
            self.animation_player.create_particles('heal', player.rect.center - heal_offset, groups)

    def flame(self, player, cost, groups):
        print('this')
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost

            if player.status.split('_')[0] == 'right': direction = pygame.math.Vector2(1, 0)
            elif player.status.split('_')[0] == 'left': direction = pygame.math.Vector2(-1, 0)
            elif player.status.split('_')[0] == 'up': direction = pygame.math.Vector2(0, -1)
            else: direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                if direction.x: # horizontal
                    offset_x = (direction.x * i) * TILESIZE
                    x = player.rect.centerx + offset_x + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)
                else: # vertical
                    offset_y = (direction.y * i) * TILESIZE
                    x = player.rect.centerx + randint(-TILESIZE // 3, TILESIZE // 3)
                    y = player.rect.centery + offset_y + randint(-TILESIZE // 3, TILESIZE // 3)
                    self.animation_player.create_particles('flame', (x, y), groups)

    def flame_my_version(self, player, cost, groups):
        """My variation of method called flame"""
        if player.energy >= cost:
            self.sounds['flame'].play()
            player.energy -= cost
            direction = player.status.split('_')[0]
            offset = pygame.math.Vector2(0, 0)

            if direction == 'down':
                for x in range(5):
                    offset += pygame.math.Vector2(randint(-32, 32), 64)
                    self.animation_player.create_particles('flame', player.rect.center + offset, groups)
            elif direction == 'up':
                for x in range(5):
                    offset += pygame.math.Vector2(randint(-32, 32), -64)
                    self.animation_player.create_particles('flame', player.rect.center + offset, groups)
            elif direction == 'left':
                for x in range(5):
                    offset += pygame.math.Vector2(-64, randint(-32, 32))
                    self.animation_player.create_particles('flame', player.rect.center + offset, groups)
            elif direction == 'right':
                for x in range(5):
                    offset += pygame.math.Vector2(+64, randint(-32, 32))
                    self.animation_player.create_particles('flame', player.rect.center + offset, groups)