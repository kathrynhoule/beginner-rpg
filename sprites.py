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
          self.animation_loop = 1

          sprite = self.game.character_spritesheet.get_sprite(0, 10, 16, 22)
          scale_factor = TILESIZE / 16
          new_width = int(16 * scale_factor)
          new_height = int(22 * scale_factor)
          self.image = pygame.transform.scale(sprite, (new_width, new_height))

          self.rect = self.image.get_rect()
          self.rect.topleft = (self.x, self.y)

          self.hitbox = pygame.Rect(self.rect.x, self.rect.y + TILESIZE, TILESIZE, (TILESIZE + 10) // 2)
     
     def scale_sprite(self, sprite, width=16, height=22):
          scale_factor = TILESIZE / width
          new_width = int(width * scale_factor)
          new_height = int(height * scale_factor)
          return pygame.transform.scale(sprite, (new_width, new_height))

     def animate(self):
          down_animations = [self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 10, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(16, 10, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(32, 10, 16, 22))]
          
          up_animations = [self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 106, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(16, 106, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(32, 106, 16, 22))]
          
          left_animations = [self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 75, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(16, 75, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(32, 75, 16, 22))]
          
          right_animations = [self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 43, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(16, 43, 16, 22)),
                             self.scale_sprite(self.game.character_spritesheet.get_sprite(32, 43, 16, 22))]
          
          if self.facing == "down":
               if self.y_change == 0:
                    self.image = self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 10, 16, 22))
               else:
                    self.image = down_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                         self.animation_loop = 1

          if self.facing == "up":
               if self.y_change == 0:
                    self.image = self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 106, 16, 22))
               else:
                    self.image = up_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                         self.animation_loop = 1

          if self.facing == "left":
               if self.x_change == 0:
                    self.image = self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 75, 16, 22))
               else:
                    self.image = left_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                         self.animation_loop = 1

          if self.facing == "right":
               if self.x_change == 0:
                    self.image = self.scale_sprite(self.game.character_spritesheet.get_sprite(0, 43, 16, 22))
               else:
                    self.image = right_animations[math.floor(self.animation_loop)]
                    self.animation_loop += 0.1
                    if self.animation_loop >= 3:
                         self.animation_loop = 1
          
     def update(self):
          self.movement()
          self.animate()

          self.hitbox.x += self.x_change
          self.collision('x')
          self.hitbox.y += self.y_change
          self.collision('y')

          self.x_change = 0
          self.y_change = 0

          self.rect.center = self.hitbox.center

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

     def collision(self, direction):
          for block in self.game.blocks:
               if self.hitbox.colliderect(block.rect):
                    if direction == 'x':
                         if self.x_change > 0:
                              self.hitbox.right = block.rect.left
                         if self.x_change < 0:
                              self.hitbox.left = block.rect.right
                    if direction == 'y':
                         if self.y_change > 0:
                              self.hitbox.bottom = block.rect.top
                         if self.y_change < 0:
                              self.hitbox.top = block.rect.bottom

class Block(pygame.sprite.Sprite):
     def __init__(self, game, x, y):
          self.game = game
          self._layer = BLOCK_LAYER
          self.groups = self.game.all_sprites, self.game.blocks
          pygame.sprite.Sprite.__init__(self, self.groups)

          self.x = x * TILESIZE
          self.y = y * TILESIZE
          self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
          self.image.fill((0, 0, 0, 0))
          self.rect = self.image.get_rect()
          self.rect.x = self.x
          self.rect.y = self.y

class Interactions(pygame.sprite.Sprite):
     def __init__(self, game, x, y, w, h, text):
          self.game = game
          self._layer = OBJECT_LAYER
          self.groups = self.game.all_sprites, self.game.interactions
          pygame.sprite.Sprite.__init__(self, self.groups)

          self.x = x
          self.y = y
          self.width = w
          self.height = h

          self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
          self.rect = self.image.get_rect(topleft=(self.x, self.y))

          self.text = text

          # for debugging
          print(f"Interaction at ({x}, {y}) with size ({w}, {h}) and text: {text}")