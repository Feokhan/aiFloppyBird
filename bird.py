import pygame
import random
from neural import Neural
from defs import *




class Bird():

    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay
        self.state = BIRD_ALIVE
        self.img = pygame.image.load(BIRD_FILENAME)
        self.rect = self.img.get_rect()
        self.speed = 0
        self.time_lived = 0
        self.set_position(BIRD_START_X, BIRD_START_Y)
        self.neural = Neural(NNET_INPUTS, NNET_HIDDEN, NNET_OUTPUTS)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y

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
        if self.rect.bottom > WIN_HEIGHT:
            self.state = BIRD_DEAD
        else:
            self.check_hits(pipes, pipes_down)

    def check_hits(self, pipes, pipes_down):
        for p in pipes:
            if p.colliderect(self.rect):
                self.state = BIRD_DEAD
                break
        for p in pipes_down:
            if p.colliderect(self.rect):
                self.state = BIRD_DEAD
                break

    def update(self, dt, pipes, pipes_down):
        if self.state == BIRD_ALIVE:
            self.time_lived += dt
            self.move(dt)
            self.jump(pipes)
            self.draw()
            self.check_status(pipes, pipes_down)

    def get_inputs(self, pipes):
        print()
        closest = WIN_WIDTH + 10
        heigth = 0
        for p in pipes:
            if closest > p.right > self.rect.left:
                closest = p.right
                heigth = p.top

        distance = closest-self.rect.right
        vertical_distance = heigth - self.rect.centery
        normalized_distance = distance/WIN_WIDTH
        normalized_vertical_distance = vertical_distance/WIN_HEIGHT

        inputs = [normalized_distance, normalized_vertical_distance]
        return inputs




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


