import pygame
import random
from neural import Neural
import numpy as np
from defs import *
import scipy.special




class Bird():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.time_lived = 0
        self.fitness = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)
        self.neural = Neural(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

    def reset(self):
        self.state = BIRD_ALIVE
        self.speed = 0
        self.fitness = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)

    def move(self, dt):

        distance = 0
        new_speed = 0

        distance = (self.speed * dt) + (0.5 * GRAVITY * dt * dt)
        new_speed = self.speed + (GRAVITY * dt)

        self.rect.centery += distance
        self.speed = new_speed

        if self.rect.top < 0:
            self.rect.top = 0
            self.speed = 0

    def jump(self, pipes):
        inputs = self.get_inputs(pipes)
        output = self.neural.get_max_value(inputs)
        if output > 0.5:
            self.speed = BIRD_START_SPEED
        #self.speed = BIRD_START_SPEED

    def draw(self):
        self.gameDisplay.blit(self.img, self.rect)

    def check_status(self, pipes, pipes_down):
        if self.rect.bottom > WIN_HEIGHT or self.rect.top <= 0:
            self.fitness = -WIN_HEIGHT
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipes, pipes_down)

    def check_hits(self, pipes, pipes_down):
        gap_y = 0;
        for p in pipes:
            if p.colliderect(self.rect):
                self.state = BIRD_DEAD
                gap_y = p.top - PIPE_GAP / 2
                self.fitness = -(abs(self.rect.centery - gap_y))
                break
        for p in pipes_down:
            if p.colliderect(self.rect):
                self.state = BIRD_DEAD
                gap_y = p.bottom + PIPE_GAP / 2
                self.fitness = -(abs(self.rect.centery - gap_y))
                break

    def update(self, dt, pipes, pipes_down):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes)
            self.draw()
            self.check_status(pipes, pipes_down)

    def get_inputs(self, pipes):
        closest = WIN_WIDTH + 10
        height = 0
        for p in pipes:
            if closest > p.right > self.rect.left:
                closest = p.right
                height = p.top

        distance = closest-self.rect.right
        vertical_distance = height - self.rect.centery
        normalized_distance = distance/WIN_WIDTH
        normalized_vertical_distance = vertical_distance/WIN_HEIGHT

        inputs = [normalized_distance, normalized_vertical_distance]
        return inputs

    def create_offspring(b1, b2, gameDisplay):
        offspring = Bird(gameDisplay)
        offspring.neural.reproduce_neural(b1.neural, b2.neural)
        return offspring




class BirdCollection():

    def __init__(self, window):
        self.window = window
        self.birds = []
        self.create_new_generation()

    def create_new_generation(self):
        self.birds = []
        for i in range(0, GENERATION_SIZE):
            self.birds.append(Bird(self.window))

    def update(self, dt, pipes, pipes_down):
        num_alive = 0
        for b in self.birds:
            b.update(dt, pipes, pipes_down)
            if b.state == BIRD_ALIVE:
                num_alive += 1

        return num_alive

    def get_avg(self):
        total = 0
        for b in self.birds:
            total += b.fitness
        ret = total/GENERATION_SIZE
        return ret


    def evolve(self):
        for b in self.birds:
            #b.fitness += b.time_lived*(TIMER_MS/1000)
            b.fitness += b.time_lived
            #print(b.fitness)
        self.birds.sort(key=lambda x: x.fitness, reverse=True)
        x = (int(len(self.birds)*KEEP_BEST_PERC))
        print('best', self.birds[0].fitness)
        print('avg', self.get_avg())
        print('worst', self.birds[len(self.birds)-1].fitness)
        good_birds = self.birds[0:x]
        bad_birds = self.birds[x:]
        for b in bad_birds:
            b.neural.random_mutation()
        new_birds = []
        new_birds = random.sample(bad_birds, int(len(bad_birds)*KEEP_BAD_PERC))
        new_birds.extend(good_birds)
        remaining_children = len(self.birds)-len(new_birds)
        while len(new_birds) < len(self.birds):
            parents = random.sample(good_birds, 2)
            new_bird = Bird.create_offspring(parents[0], parents[1], self.window)
            if random.random() < MUTATION_CHANCE:
                new_bird.neural.random_mutation()
            new_birds.append(new_bird)

        for b in new_birds:
            b.reset()
        self.birds = new_birds

    def get_best(self):
        self.birds.sort(key=lambda x: x.fitness, reverse=True)
        return self.birds[0].fitness

    def get_worst(self):
        self.birds.sort(key=lambda x: x.fitness, reverse=True)
        return self.birds[len(self.birds)-1].fitness
