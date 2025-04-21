import pygame
from pytmx.util_pygame import load_pygame
from sprites import *
from config import *
from camera import *
from map import TiledMap
import sys

class Game:
     def __init__(self):
          pygame.init()

          self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

          self.clock = pygame.time.Clock()
          self.running = True

          self.character_spritesheet = Spritesheet("sprite/ghost_base_sprites.png")

          self.interact_text = None

     def new(self):
          # a new game starts
          self.playing = True

          self.all_sprites = pygame.sprite.LayeredUpdates()
          self.blocks = pygame.sprite.LayeredUpdates()
          self.enemies = pygame.sprite.LayeredUpdates()
          self.attacks = pygame.sprite.LayeredUpdates()
          self.interactions = pygame.sprite.Group()

          # loads map
          self.map = TiledMap(self, "map/ghost_home_interior_map.tmx")

          self.player = Player(self, 18, 4)

          self.camera = Camera(self.map.width, self.map.height)

     def events(self):
          # game loop events
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False

               # object interactions with h
               elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:
                         self.interact_text = None
                         for interaction in self.interactions:
                              if self.player.hitbox.colliderect(interaction.rect):
                                   self.interact_text = interaction.text

     def update(self):
          # game loop updates
          self.all_sprites.update()
          self.camera.update(self.player)

     def draw(self):
          self.screen.fill(BLACK)

          # draws background
          self.map.draw_map(self.screen, self.camera)

          # draws player and other sprites
          for sprite in self.all_sprites:
               self.screen.blit(sprite.image, self.camera.apply(sprite))

          # draws foreground layers
          for layer in self.map.front_layers:
               self.map.draw_layer(self.screen, self.camera, layer)

          # draws hitboxes for debugging
          pygame.draw.rect(self.screen, (255, 0, 0), self.camera.apply_rect(self.player.hitbox), 2)
          for i in self.interactions:
               pygame.draw.rect(self.screen, (0, 255, 0), self.camera.apply_rect(i.rect), 2)

          # draws textboxes for object interactions
          if self.interact_text:
               font = pygame.font.SysFont("Arial", 18)
               text_surf = font.render(self.interact_text, True, (255, 255, 255))
               
               # background box
               padding = 10
               text_rect = text_surf.get_rect()
               box_width = text_rect.width + padding * 2
               box_height = text_rect.height + padding * 2
               box_x = (WIN_WIDTH - box_width) // 2
               box_y = WIN_HEIGHT - box_height - 30

               # draw box
               pygame.draw.rect(self.screen, (0, 0, 0), (box_x, box_y, box_width, box_height))
               pygame.draw.rect(self.screen, (255, 255, 255), (box_x, box_y, box_width, box_height), 2)

               # draw text
               self.screen.blit(text_surf, (box_x + padding, box_y + padding))

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