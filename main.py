import pygame
import random

pygame.init()
WIDTH = 800
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ITECH 210 FLAPP BIRD")
clock = pygame.time.Clock()

#color constants
BLACK = (0,0,0)

#fonts
score_font = pygame.font.SysFont("arial", 30)
go_font = pygame.font.SysFont("arial", 60)

#load music
pygame.mixer.music.load("forest.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.05)

#background
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

#player
player_pos = [100,200]
player_sprite = pygame.image.load("bird.png").convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (64,64))
player_rect = player_sprite.get_rect(center=player_pos)
player_hit = player_rect.inflate(-20,-20)
force =0
gravity = 1

pipes = [
    [200, random.randint(50, 225)], 
    [500, random.randint(50, 225)], 
    [800, random.randint(50, 225)], 
    [1100, random.randint(50, 225)], 
]
pipe_1 = pygame.image.load('pipe.png').convert_alpha()
pipe_ratio = pipe_1.get_width() / pipe_1.get_height()
new_width = 150
new_height = int(new_width * pipe_1.get_height() / pipe_1.get_width())
pipe_1 = pygame.transform.scale(pipe_1, (new_width, new_height))
pipe_2 = pygame.transform.flip(pipe_1, False, True)

gap = 150
speed = 1
score = 0
game_over = False



#main loop
running = True
while running:
    #check for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                force += 10

    if game_over:
        continue

    #update player pos
    force -= gravity
    force = max(-1*gravity, force)
    player_pos[1] -= force
    player_rect = player_sprite.get_rect(center=player_pos)
    player_hit.center = player_rect.center
    


    #update pipe positions
    for pipe in pipes:
        pipe[0] -= speed

        if pipe[0] < -200:
            pipe[0] = 1000

    #check collisions
    for pipe in pipes:
        rect_2 = pipe_2.get_rect(bottomleft=pipe)
        hit_2 = rect_2.inflate(-20,-20)
        hit_2.center = rect_2.center
        
        rect_1 = pipe_1.get_rect(topleft=(pipe[0], pipe[1] + gap))
        hit_1 = rect_1.inflate(-20,-20)
        hit_1.center = rect_1.center
        
        if player_hit.colliderect(hit_2) or player_hit.colliderect(hit_1):
            game_over = True
        

    #update score
    score = pygame.time.get_ticks() // 1000
    
    #update speed
    speed = (score //10) + 1

    #draw to screen
    screen.fill(BLACK)

    #draw background
    screen.blit(bg, (0,0))

    #draw player
    screen.blit(player_sprite, player_rect) 
    

    #draw pipes
    for pipe in pipes:
        
        rect_2 = pipe_2.get_rect(bottomleft=pipe)
        rect_1 = pipe_1.get_rect(topleft=(pipe[0], pipe[1] + gap))
        
        screen.blit(pipe_1, rect_1)
        screen.blit(pipe_2, rect_2)
        
    #draw score
    score_text = score_font.render(f"Score: {score}", True, (255,255,255))
    score_rect = score_text.get_rect(center=(WIDTH//2,25))
    screen.blit(score_text, score_rect)

    if game_over:
        go_text = go_font.render("GAME OVER", True, (255,255,255))
        go_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(go_text, go_rect)


    pygame.display.flip()
    dt = clock.tick(60) / 1000  #60 frames per second

pygame.quit()