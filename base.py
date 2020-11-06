import pygame as pg
import os
import gamerule

base_image = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "base.png")).convert_alpha())

class Base:
	WIDTH = base_image.get_width()
	def __init__(self, y):
		self.y = y
		self.x1 = 0
		self.x2 = self.WIDTH

	def move(self):
		self.x1 -= gamerule.vx
		self.x2 -= gamerule.vx
		if self.x1 < -self.WIDTH:
			self.x1 = self.x2 + self.WIDTH
		if self.x2 < -self.WIDTH:
			self.x2 = self.x1 + self.WIDTH

	def draw(self, screen):
		screen.blit(base_image, (self.x1, self.y))
		screen.blit(base_image, (self.x2, self.y))
