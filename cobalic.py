import sys
import time as py_time
import os
import random
from math import ceil

import pygame
from pygame import *
from pygame import time as pygame_time

image_files = [file for file in os.listdir("./images") if file != '.gitkeep']
images = [image.load('images/' + file) for file in image_files]

width, height = images[0].get_size()

class Tile(sprite.Sprite):
    def __init__(self, images, pos, size):
        sprite.Sprite.__init__(self)

        self.rect = None
        self.image = None

        self.images = images
        self.num_images = len(images)

        self.random_tilesheet()
        self.reconstruct(pos, size)

    def crop(self):
        if not self.rect:
            return

        x, y = self.rect.topleft
        self.image.blit(self.tilesheet, (-x, -y))

    def reconstruct(self, pos, size):
        self.rect = Rect(pos, size)

        self.image = Surface(size)
        self.crop()

    def refresh_tilesheet(self):
        self.tilesheet = self.images[self.index]
        self.crop()

    def next_tilesheet(self):
        self.index = (self.index + 1) % self.num_images
        self.refresh_tilesheet()

    def prev_tilesheet(self):
        self.index = (self.index - 1) % self.num_images
        self.refresh_tilesheet()

    def random_tilesheet(self):
        self.index = random.randint(0, self.num_images - 1)
        self.refresh_tilesheet()



pygame.init()

info = display.Info()
screen_width = info.current_w
screen_height = info.current_h

width_scale_ratio = width / screen_width
height_scale_ratio = height / screen_height

screen = display.set_mode(
    (screen_width, screen_height),
    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
)

composite = Surface((width, height))

timer = pygame_time.Clock()



horizontal_parts = 1
vertical_parts = 1

part_width = width / horizontal_parts
part_height = height / vertical_parts



tiles = sprite.Group()

def draw_tiles():
    tiles.draw(composite)
    transform.scale(composite, (screen_width, screen_height), screen)

def reconstruct_grid():
    tiles.empty()

    part_width = ceil(width / horizontal_parts)
    part_height = ceil(height / vertical_parts)

    tile_list = []
    for x in range(horizontal_parts):
        for y in range(vertical_parts):
            tile_list.append(
                Tile(images,
                     (x * part_width, y * part_height),
                     (part_width, part_height)))

    tiles.add(tile_list)
    draw_tiles()

reconstruct_grid()

# We create a sprite which follows the mouse position so that it can be
# used to collide with a sprite group, which is easier than
# checking each tile
mouse_sprite = sprite.Sprite()
mouse_sprite.image = pygame.Surface((1, 1))
mouse_sprite.image.fill(Color("#000000"))
mouse_sprite.rect = mouse_sprite.image.get_rect()

def check_collision(mouse, sprite):
    return sprite.rect.collidepoint(mouse.rect.topleft)

while True:
    timer.tick()

    for e in pygame.event.get():
        if e.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            x *= width_scale_ratio
            y *= height_scale_ratio

            mouse_sprite.rect.topleft = (x, y)

            selected_tile = sprite.spritecollideany(
                mouse_sprite,
                tiles,
                check_collision
            )

            # Skip if no tile was selected
            if not selected_tile:
                pass

            # Next image
            elif e.button == 1:
                selected_tile.next_tilesheet()
                draw_tiles()

            # Random image
            elif e.button == 2:
                selected_tile.random_tilesheet()
                draw_tiles()

            # Previous image
            elif e.button == 3:
                selected_tile.prev_tilesheet()
                draw_tiles()

        elif e.type == KEYDOWN:

            amount_of_steps = 1
            mods = pygame.key.get_mods()
            if mods & KMOD_LCTRL:
                amount_of_steps = 50

            # Less horizontal parts
            if e.key == K_LEFT:
                if horizontal_parts > 1:
                    horizontal_parts -= amount_of_steps
                    reconstruct_grid()

            # Less vertical parts
            elif e.key == K_UP:
                vertical_parts += amount_of_steps
                reconstruct_grid()

            # More horizontal parts
            elif e.key == K_RIGHT:
                horizontal_parts += amount_of_steps
                reconstruct_grid()

            # More vertical parts
            elif e.key == K_DOWN:
                if vertical_parts > 1:
                    vertical_parts -= amount_of_steps
                    reconstruct_grid()

            # Randomize
            elif e.key == K_r:
                reconstruct_grid()

            # Save image
            elif e.key == K_s:
                image.save(composite, 'cover_{}x{}_{}.png'.format(
                    horizontal_parts,
                    vertical_parts,
                    py_time.time())
                )

            # Quit
            elif e.key == K_ESCAPE:
                sys.exit()

        elif e.type == QUIT:
            sys.exit()

    pygame.display.flip()
