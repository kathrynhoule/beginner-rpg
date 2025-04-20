import pygame
from pytmx.util_pygame import load_pygame
from config import *
from sprites import Block

class TiledMap:
     def __init__(self, game, map_file):
          self.game = game
          self.tmx_data = load_pygame(map_file)

          self.width = self.tmx_data.width * TILESIZE
          self.height = self.tmx_data.height * TILESIZE

          self.load_map()

     def load_map(self):
          for obj in self.tmx_data.get_layer_by_name("Collisions").tiles():
               x, y, tile = obj
               Block(self.game, x, y)

     def draw_map(self, screen, camera):
          # draws background layers
          for layer in self.tmx_data.visible_layers:
               if layer.name in ["Walls_Flooring", "Objects_Ground", "Objects_Front"]:
                    self.draw_layer(screen, camera, layer)

          # draws front layers after sprites
          self.front_layers = [layer for layer in self.tmx_data.visible_layers if layer.name == "Objects_Behind"]

     def draw_layer(self, screen, camera, layer):
          for x, y, tile in layer.tiles():
               if tile:
                    tile = pygame.transform.scale(tile, (TILESIZE, TILESIZE))
                    tile_rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    screen.blit(tile, camera.apply_rect(tile_rect))