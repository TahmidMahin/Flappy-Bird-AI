import pygame as pg
import gamerule
import math
import os

bird_images = [pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird" + str(x+1) + ".png"))) for x in range(3)]

class Bird:
	ANIMATION_TIME = 4
	STATES = len(bird_images)
	x = gamerule.BIRD_POS
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.v = 0
		self.y0 = self.y
		self.v0 = self.v
		self.t = 0
		self.tilt = 0
		self.img = bird_images[0]

	def jump(self):
		self.v = -gamerule.JUMP
		self.v0 = self.v
		self.t = 0
		self.y0 = self.y

	def move(self):
		self.t += 1
		k = gamerule.vT/gamerule.a
		self.v = gamerule.vT + (self.v0-gamerule.vT)*math.exp(-self.t/k)
		displacement = gamerule.vT*self.t - k*(self.v0 - gamerule.vT)*math.expm1(-self.t/k)
		self.y = self.y0 + displacement
		self.tilt = math.degrees(-math.atan2(self.v, gamerule.vx))

	def draw(self, screen):
		index = 0 if self.v > gamerule.vT-6 else (self.t//self.ANIMATION_TIME)%self.STATES
		self.img = bird_images[index]
		rotated_image = pg.transform.rotate(self.img, self.tilt)
		new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
		screen.blit(rotated_image, new_rect.topleft)

	def get_mask(self):
		return pg.mask.from_surface(self.img)