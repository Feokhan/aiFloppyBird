import pygame
import random


def base_movement(window, base_image, x_val):
    window.blit(base_image, (x_val, 550))
    #second widnwow
    window.blit(base_image, (x_val+900, 550))


def bird_movement(window, bird_image, bird_rect):
    window.blit(bird_image, bird_rect)


def pipe_movement(window, pipes, pipe_image):
    for pipe in pipes:
        pipe.centerx -= 5
    for pipe in pipes:
        window.blit(pipe_image, pipe)

def collision(pipes, bird_rect):
    for pipe in pipes:
        if pipe.colliderect(bird_rect):
            print("collision")
    if bird_rect.top <= -25:
        print("collision with ceiling")
    if bird_rect.bottom >= 575:
        print("collission bottom")


def game_build():
    pygame.init()
    window = pygame.display.set_mode((900, 600))

    running = True
    clock = pygame.time.Clock()
    #bg
    bg_image = pygame.image.load("img/bg.png")
    #base
    base_image = pygame.image.load("img/base.png")
    x_val = 0
    #bird
    bird_image = pygame.image.load("img/bird.png")
    bird_rect = bird_image.get_rect(center=(250, 300))
    g_force = 1.5
    bird_next_pos = 0
    #pipe
    pipe_image = pygame.image.load("img/pipe.png")
    pipes_list = []
    TIMER = pygame.USEREVENT
    pygame.time.set_timer(TIMER, 1300)

    while running:
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    #bird_next_pos = 0
                    bird_next_pos -= 50
            if event.type == TIMER:
                rand_h = [100, 150, 200, 250, 300, 350, 400, 450]
                pipes = pipe_image.get_rect(midtop=(910,random.choice(rand_h)))
                pipes_list.append(pipes)

        #game
        window.blit(bg_image, (0,0))
        #collision detection
        collision(pipes_list, bird_rect)
        # pipe movement
        pipe_movement(window, pipes_list, pipe_image)
        #base movement
        x_val -= 1
        base_movement(window, base_image, x_val)
        if x_val <= -900:
            x_val = 0
        #bird movement
        bird_next_pos += g_force
        bird_rect.centery = bird_next_pos
        bird_movement(window, bird_image, bird_rect)


        #update
        clock.tick(60)
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    game_build()
    print("test")