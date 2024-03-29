import pygame
import sys
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Colors
BLACK, WHITE = (0, 0, 0), (255, 255, 255)

# Game variables
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 7
BALL_VELOCITY_X, BALL_VELOCITY_Y = 5, 5
PADDLE_VELOCITY = 10
left_paddle = pygame.Rect(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 30 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Sound generation function (same as Breakout)
def generate_square_wave(frequency=440, volume=0.1, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    period = int(sample_rate / frequency)
    amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    waveform = array('h', [int(amplitude if time < period / 2 else -amplitude) for time in range(period)] * int(duration * frequency))
    sound = pygame.mixer.Sound(waveform)
    sound.set_volume(volume)
    return sound

# Predefined sounds
hit_paddle_sound = generate_square_wave(660, 0.1, 0.1)
hit_wall_sound = generate_square_wave(440, 0.1, 0.1)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.move_ip(0, -PADDLE_VELOCITY)
    if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
        left_paddle.move_ip(0, PADDLE_VELOCITY)
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.move_ip(0, -PADDLE_VELOCITY)
    if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.move_ip(0, PADDLE_VELOCITY)

    # Ball movement and collision
    ball.x += BALL_VELOCITY_X
    ball.y += BALL_VELOCITY_Y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        BALL_VELOCITY_Y *= -1
        hit_wall_sound.play()

    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        BALL_VELOCITY_X *= -1
        hit_paddle_sound.play()

    # Drawing
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    pygame.display.flip()
    pygame.time.delay(30)
