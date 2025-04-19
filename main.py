import pygame
from pytmx.util_pygame import load_pygame
from sprites import *
from config import *
import sys

class Game:
     def __init__(self):
          pygame.init()

          self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

          self.clock = pygame.time.Clock()
          self.running = True

     def new(self):
          # a new game starts
          self.playing = True

          # loads map
          self.tmx_data = load_pygame("map/ghost_home_interior_map.tmx")

          self.all_sprites = pygame.sprite.LayeredUpdates()
          self.blocks = pygame.sprite.LayeredUpdates()
          self.enemies = pygame.sprite.LayeredUpdates()
          self.attacks = pygame.sprite.LayeredUpdates()

          self.player = Player(self, 1, 2)

     def events(self):
          # game loop events
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False

     def update(self):
          # game loop updates
          self.all_sprites.update()

     def draw(self):
          self.screen.fill(BLACK)

          for layer in self.tmx_data.visible_layers:
               if hasattr(layer, 'data'):
                    for x, y, tile in layer.tiles():
                         if tile:
                              tile = pygame.transform.scale(tile, (TILESIZE, TILESIZE))
                              self.screen.blit(tile, (x * TILESIZE, y * TILESIZE))

          self.all_sprites.draw(self.screen)

          self.clock.tick(FPS)
          pygame.display.update()

     def main(self):
          # game loop
          while self.playing:
               self.events()
               self.update()
               self.draw()
          self.running = False

     def game_over(self):
          pass

     def intro_screen(self):
          pass

g = Game()
g.intro_screen()
g.new()
while g.running:
     g.main()
     g.game_over()

pygame.quit()
sys.exit()