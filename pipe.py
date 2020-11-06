import pygame as pg
import gamerule
import os
import random

pipe_image = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())

class Pipe():
	GAP = 200
	PIPE_HEIGHT = pipe_image.get_height()
	def __init__(self, x):
		self.x = x
		self.height = random.randrange(50, 450)
		self.PIPE_TOP = pg.transform.flip(pipe_image, False, True)
		self.PIPE_BOTTOM = pipe_image
		self.top = self.height - self.PIPE_HEIGHT
		self.bottom = self.height + self.GAP
		self.passed = False
		self.vy = random.randrange(gamerule.PIPE_V_MIN, gamerule.PIPE_V_MAX)
		
	def move(self):
		self.x -= gamerule.vx
		if self.height < 50 or self.height > 450:
			self.vy *= -1
		self.height += self.vy
		self.top = self.height - self.PIPE_HEIGHT
		self.bottom = self.height + self.GAP 

	def draw(self, screen):
		screen.blit(self.PIPE_TOP, (self.x, self.top))
		screen.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

	def collide(self, bird):
		bird_mask = bird.get_mask()
		top_mask = pg.mask.from_surface(self.PIPE_TOP)
		bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)
		top_offset = (self.x - bird.x, self.top - round(bird.y))
		bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

		top_point = bird_mask.overlap(top_mask, top_offset)
		bottom_point = bird_mask.overlap(bottom_mask, bottom_offset)

		if top_point or bottom_point:
			return True
		return False
