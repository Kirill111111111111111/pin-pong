import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-понг")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 60
clock = pygame.time.Clock()


class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 7

    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

class Ball:
    def __init__(self, size):
        self.size = size
        self.rect = pygame.Rect(WIDTH // 2 - size // 2,
                               HEIGHT // 2 - size // 2, size, size)
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx = random.choice([-3, 3])
        self.dy = random.choice([-3, 3])

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect)

class Game:
    def __init__(self):
        self.paddle_left = Paddle(20, HEIGHT // 2 - 25, 10, 50)
        self.paddle_right = Paddle(WIDTH - 30, HEIGHT // 2 - 25, 10, 50)
        self.ball = Ball(15)
        self.score_left = 0
        self.score_right = 0
        self.font = pygame.font.Font(None, 36)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.paddle_left.move_up()
        if keys[pygame.K_s]:
            self.paddle_left.move_down()
        if keys[pygame.K_UP]:
            self.paddle_right.move_up()
        if keys[pygame.K_DOWN]:
            self.paddle_right.move_down()

    def update(self):
        self.ball.move()
        if self.ball.rect.colliderect(self.paddle_left.rect) or \
           self.ball.rect.colliderect(self.paddle_right.rect):
            self.ball.dx *= -1

        if self.ball.rect.left <= 0:
            self.score_right += 1
            self.ball.reset()
        elif self.ball.rect.right >= WIDTH:
            self.score_left += 1
            self.ball.reset()

    def draw(self, screen):
        screen.fill(WHITE)
        self.paddle_left.draw(screen)
        self.paddle_right.draw(screen)
        self.ball.draw(screen)
        score_text = self.font.render(f"{self.score_left} - {self.score_right}", True, BLACK)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.handle_input()
            self.update()
            self.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()




