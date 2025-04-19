import pygame
from config import *
import math
import random

class Spritesheet:
     def __init__(self, file):
          self.sheet = pygame.image.load(file).convert_alpha()
     
     def get_sprite(self, x, y, width, height):
          sprite = pygame.Surface([width, height], pygame.SRCALPHA)
          sprite.blit(self.sheet, (0,0), (x, y, width, height))
          return sprite

class Player(pygame.sprite.Sprite):
     def __init__(self, game, x, y):
     
          self.game = game
          self._layer = PLAYER_LAYER
          self.groups = self.game.all_sprites
          pygame.sprite.Sprite.__init__(self, self.groups)

          self.x = x * TILESIZE
          self.y = y * TILESIZE
          self.width = TILESIZE
          self.height = TILESIZE

          self.x_change = 0
          self.y_change = 0

          self.facing = "down"

          self.image = self.game.character_spritesheet.get_sprite(0, 0, 16, 32)
          self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE * 2))

          self.rect = self.image.get_rect()
          self.rect.x = self.x
          self.rect.y = self.y - (self.rect.height - TILESIZE)

     def update(self):
          self.movement()

          self.rect.x += self.x_change
          self.rect.y += self.y_change

          self.x_change = 0
          self.y_change = 0

     def movement(self):
          keys = pygame.key.get_pressed()
          if keys[pygame.K_LEFT]:
               self.x_change -= PLAYER_SPEED
               self.facing = "left"
          if keys[pygame.K_RIGHT]:
               self.x_change += PLAYER_SPEED
               self.facing = "right"
          if keys[pygame.K_DOWN]:
               self.y_change += PLAYER_SPEED
               self.facing = "down"
          if keys[pygame.K_UP]:
               self.y_change -= PLAYER_SPEED
               self.facing = "up"