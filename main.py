import pygame
import random
from bird import Bird
from bird import BirdCollection
import numpy as np
from defs import *



def base_movement(window, base_image, x_val):
    window.blit(base_image, (x_val, 550))
    #second window
    window.blit(base_image, (x_val+WIN_WIDTH, 550))


def update_label(data, title, font, x, y, gameDisplay):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y


def update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_iterations,'Iteration', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_alive,'Alive', font, x_pos, y_pos + gap, gameDisplay)


def pipe_movement(window, pipes, pipe_image):
    for pipe in pipes:
        if pipe.centerx < 0:
            pipes.remove(pipe)
        pipe.centerx -= 5
    for pipe in pipes:
        window.blit(pipe_image, pipe)

def game_build():
    pygame.init()
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    #fonts
    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)
    running = True
    game_over = False
    clock = pygame.time.Clock()
    #bg
    bg_image = pygame.image.load("img/bg.png")
    #base
    base_image = pygame.image.load("img/base.png")
    x_val = 0
    #bird
    bird_image = pygame.image.load("img/bird.png")
    bird_rect = bird_image.get_rect(center=(250, WIN_HEIGHT/2))
    g_force = G_FORCE
    bird_next_pos = WIN_HEIGHT/2-100
    #bird jump
    distance = 0
    new_speed = 0
    speed = 0
    distance = speed*dt + 0.5*G_FORCE*dt*dt
    new_speed = speed + G_FORCE*dt
    #pipe
    pipe_image = pygame.image.load("img/pipe.png")
    pipe_down_image = pygame.image.load("img/pipe_down.png")
    pipes_list = []
    pipes_down_list = []
    TIMER = pygame.USEREVENT
    pygame.time.set_timer(TIMER, TIMER_MS)
    birds = BirdCollection(window)

    num_iterations = 1
    num_iterations = birds.load_generation("data/iteration134.npz")

    while running:
        #time
        dt = clock.tick(FPS)
        game_time += dt

        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                birds.save_generation(num_iterations)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    running = False
            if event.type == TIMER:
                rand_h = [450, 400, 350, 300, 250, 200]
                rand_pipe = random.choice(rand_h)
                pipes = pipe_image.get_rect(midtop=(WIN_WIDTH+10, rand_pipe))
                pipes_down = pipe_down_image.get_rect(midbottom=(WIN_WIDTH+10, rand_pipe-PIPE_GAP))
                pipes_list.append(pipes)
                pipes_down_list.append(pipes_down)

        #game
        window.blit(bg_image, (0,0))
        # pipe movement
        pipe_movement(window, pipes_list, pipe_image)
        pipe_movement(window, pipes_down_list, pipe_down_image)
        #base movement
        x_val -= 1
        base_movement(window, base_image, x_val)
        if x_val <= -WIN_HEIGHT:
            x_val = 0

        # update data labels
        num_alive = birds.update(dt, pipes_list, pipes_down_list)
        update_data_labels(window, dt, game_time, num_iterations, num_alive, label_font)

        if num_alive == 0:
            pipes_list = []
            pipes_down_list = []
            game_time = 0
            birds.evolve()
            num_iterations += 1
        #update
        clock.tick(FPS)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    game_build()
    print("test")