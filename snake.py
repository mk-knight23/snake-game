import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
DARK_GRAY = (40, 40, 40)

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')

class Snake:
    def __init__(self):
        # Start with a bigger snake (length 5)
        self.positions = [(GRID_WIDTH // 2 - i, GRID_HEIGHT // 2) for i in range(5)]
        self.direction = (1, 0)
        self.length = 5
        self.colors = [GREEN, BLUE, CYAN, PURPLE, YELLOW]  # Rainbow effect for snake

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + x) % GRID_WIDTH, (cur[1] + y) % GRID_HEIGHT)
        if new in self.positions[3:]:
            return False
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.positions = [(GRID_WIDTH // 2 - i, GRID_HEIGHT // 2) for i in range(5)]
        self.direction = (1, 0)
        self.length = 5

    def render(self, surface):
        for i, p in enumerate(self.positions):
            color = self.colors[i % len(self.colors)]  # Cycle through colors
            pygame.draw.rect(surface, color,
                           (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH-1),
                        random.randint(0, GRID_HEIGHT-1))
        # Random food color
        self.color = random.choice([RED, BLUE, PURPLE, YELLOW, CYAN])

    def render(self, surface):
        pygame.draw.rect(surface, self.color,
                        (self.position[0] * GRID_SIZE,
                         self.position[1] * GRID_SIZE,
                         GRID_SIZE, GRID_SIZE))

def draw_glowing_text(surface, text, size, color, position, glow_color=(255, 255, 255), glow_radius=2):
    font = pygame.font.Font(None, size)
    # Draw glow effect
    for offset in range(glow_radius, 0, -1):
        glow_surface = font.render(text, True, glow_color)
        for dx, dy in [(0, offset), (0, -offset), (offset, 0), (-offset, 0)]:
            x = position[0] + dx
            y = position[1] + dy
            surface.blit(glow_surface, (x, y))
    # Draw main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, position)

def draw_welcome_box(surface):
    # Calculate box dimensions and position
    box_width = 400
    box_height = 200
    x = (WINDOW_WIDTH - box_width) // 2
    y = (WINDOW_HEIGHT - box_height) // 2
    
    # Draw glowing border
    glow_color = ORANGE
    for i in range(10, 0, -1):
        alpha = int(255 * (i / 10))
        glow_surface = pygame.Surface((box_width + i*2, box_height + i*2), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (*glow_color, alpha), 
                        (0, 0, box_width + i*2, box_height + i*2), 
                        border_radius=20)
        surface.blit(glow_surface, (x-i, y-i))
    
    # Draw main box
    pygame.draw.rect(surface, DARK_GRAY, (x, y, box_width, box_height), 
                    border_radius=15)
    pygame.draw.rect(surface, ORANGE, (x, y, box_width, box_height), 
                    width=2, border_radius=15)
    
    # Draw welcome text
    draw_glowing_text(surface, "Welcome to Snake Game!", 48, WHITE, 
                     (x + 40, y + 40), ORANGE)
    draw_glowing_text(surface, "Press SPACE to Start", 36, WHITE, 
                     (x + 80, y + 120), ORANGE)

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    high_score = 99
    font = pygame.font.Font(None, 36)
    game_started = False

    # Create a gradient background
    background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    for y in range(WINDOW_HEIGHT):
        color_value = int((y / WINDOW_HEIGHT) * 50)
        pygame.draw.line(background, (color_value, color_value, color_value),
                        (0, y), (WINDOW_WIDTH, y))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not game_started and event.key == pygame.K_SPACE:
                    game_started = True
                if game_started:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)

        # Draw gradient background
        screen.blit(background, (0, 0))
        
        # Draw grid lines
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

        # Draw "Made BY KAZI" text
        draw_glowing_text(screen, "Made BY KAZI", 72, YELLOW, 
                         (WINDOW_WIDTH//2 - 200, WINDOW_HEIGHT - 100), 
                         glow_color=ORANGE)

        if not game_started:
            draw_welcome_box(screen)
        else:
            if not snake.update():
                snake.reset()
                food.randomize_position()
                score = 0

            if snake.get_head_position() == food.position:
                snake.length += 1
                score += 1
                food.randomize_position()

            snake.render(screen)
            food.render(screen)
            
            # Display score and high score
            score_text = font.render(f'Score: {score}', True, WHITE)
            high_score_text = font.render(f'High Score: {high_score}', True, YELLOW)
            screen.blit(score_text, (10, 10))
            screen.blit(high_score_text, (10, 50))

        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    main() 