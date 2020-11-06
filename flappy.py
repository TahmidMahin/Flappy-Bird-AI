import pygame as pg
import os
import gamerule
import neat

pg.init()
screen = pg.display.set_mode((gamerule.ScreenWidth, gamerule.ScreenHeight))

from bird import Bird
from pipe import Pipe
from base import Base

pg.display.set_caption("Flappy Bird")
clock = pg.time.Clock()
STAT_FONT = pg.font.SysFont("Liberation Serif", 50)
END_FONT = pg.font.SysFont("comicsans", 70)
bg_img = pg.transform.scale(pg.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

def show_screen(screen, bird, pipes, base, score):
	screen.blit(bg_img, (0, 0))
	for pipe in pipes:
		pipe.draw(screen)
	base.draw(screen)
	bird.draw(screen)
	text = STAT_FONT.render("Score: " + str(score), False, (255, 255, 255))
	screen.blit(text, (10, 10))
	pg.display.update()

def run():
	score = 0
	bird = Bird(210, 350)
	base = Base(gamerule.FLOOR)
	pipes = [Pipe(gamerule.ScreenWidth + 150 + gamerule.PIPE_GAP*x) for x in range(3)]
	running = True
	while running:
		clock.tick(gamerule.FPS)
		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_SPACE:
					bird.jump()
		for pipe in pipes:
			if pipe.collide(bird):
				running =  False
			if not pipe.passed and bird.x > pipe.x + pipe.PIPE_TOP.get_width():
				pipe.passed = True
				score += 1
			pipe.move()
		if pipes[0].x + pipes[0].PIPE_TOP.get_width() < 0:
			pipes.pop(0)
			pipes.append(Pipe(pipes[-1].x + gamerule.PIPE_GAP))
		if bird.y + bird.img.get_height() > gamerule.FLOOR or bird.y < gamerule.CEILING:
			running = False
		bird.move()
		base.move()
		show_screen(screen, bird, pipes, base, score)
	pg.quit()
	quit()


if __name__ == "__main__":
	run()