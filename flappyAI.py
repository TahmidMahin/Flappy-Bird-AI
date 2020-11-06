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

STAT_FONT = pg.font.SysFont("Liberation Serif", 50)

bg_img = pg.transform.scale(pg.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (600, 900))

gen = 0

def show_screen(screen, birds, pipes, base, score, gen):
	screen.blit(bg_img, (0, 0))
	for pipe in pipes:
		pipe.draw(screen)
	for bird in birds:
		bird.draw(screen)
	base.draw(screen)
	text = STAT_FONT.render("Score: " + str(score), False, (255, 255, 255))
	screen.blit(text, (10, 10))
	text = STAT_FONT.render("Generation: " + str(gen), False, (255, 255, 255))
	screen.blit(text, (10, 70))
	text = STAT_FONT.render("Alive: " + str(len(birds)), False, (255, 255, 255))
	screen.blit(text, (10, 130))
	pg.display.update()

def eval_genomes(genomes, config):
	global gen
	gen += 1
	nets = []
	birds = []
	ge = []

	for _, genome in genomes:
		genome.fitness = 0
		net = neat.nn.FeedForwardNetwork.create(genome, config)
		nets.append(net)
		birds.append(Bird(gamerule.BIRD_POS,350))
		ge.append(genome)

	score = 0
	base = Base(gamerule.FLOOR)
	pipes = [Pipe(gamerule.ScreenWidth + 150 + gamerule.PIPE_GAP*x) for x in range(3)]
	clock = pg.time.Clock()
	running = True

	while running and len(birds) > 0:
		clock.tick(gamerule.FPS)

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
				pg.quit()
				quit()
				break

		pipe_ind = 0
		for x, pipe in enumerate(pipes):
			if not pipe.passed:
				pipe_ind = x
				break

		for x, bird in enumerate(birds):
			ge[x].fitness += 0.1
			bird.move()
			output = nets[x].activate((bird.y,
									pipes[pipe_ind].height,
									pipes[pipe_ind].bottom,
									pipes[pipe_ind].vy))
			if output[0] > 0.5:
				bird.jump()

		base.move()

		for pipe in pipes:
			for bird in birds:
				if pipe.collide(bird):
					ind = birds.index(bird)
					ge[ind].fitness -= 1
					nets.pop(ind)
					ge.pop(ind)
					birds.pop(ind)
					

			if not pipe.passed and Bird.x > pipe.x + pipe.PIPE_TOP.get_width():
				pipe.passed = True
				for genome in ge:
					genome.fitness += 5
				score += 1
			pipe.move()

		if pipes[0].x + pipes[0].PIPE_TOP.get_width() < 0:
			pipes.pop(0)
			pipes.append(Pipe(pipes[-1].x + gamerule.PIPE_GAP))

		for bird in birds:
			if bird.y + bird.img.get_height() > gamerule.FLOOR or bird.y < gamerule.CEILING:
				ind = birds.index(bird)
				ge[ind].fitness -= 1
				ind = birds.index(bird)
				nets.pop(ind)
				ge.pop(ind)
				birds.pop(ind)

		show_screen(screen, birds, pipes, base, score, gen)

def run(config_file):
	config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
	p = neat.Population(config)
	p.add_reporter(neat.StdOutReporter(True))
	stats = neat.StatisticsReporter()
	p.add_reporter(stats)
	winner = p.run(eval_genomes, 50)
	print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config-feedforward.txt')
	run(config_path)