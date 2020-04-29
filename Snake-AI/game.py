import pygame
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FONT = pygame.font.SysFont("baskervillettc", 50)

# print(pygame.font.get_fonts())

WIN_WIDTH = 750
BORDER = 800
BORDER_WIDTH = 50

dis = pygame.display.set_mode((BORDER, BORDER), pygame.FULLSCREEN)
pygame.display.set_caption('Snake Game by Edureka')

SNAKE_BLOCK = 20


def run(x1, y1, x1_change, y1_change, width):
    # Setting up the game
    game_over = False
    game_close = False

    clock = pygame.time.Clock()

    # Staring score
    score = 1

    # First food item
    food_x = get_food_coordinates()
    food_y = get_food_coordinates()

    # List of snake coordinates
    snake_list = [(x1, y1)]

    while not game_over:

        # After the game is lost give a screen
        while game_close:
            dis.fill(BLACK)
            message("You Lost! Score: %s" % str(max(0, score - 1)), RED)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    # New game
                    if event.key == pygame.K_SPACE:
                        game_close = False
                        game_over = False
                        x1 = 400
                        y1 = 400
                        x1_change = 10
                        y1_change = 0
                        width = 20
                        score = 0
                        snake_list = [(x1, y1)]

        # Change direction of the snake
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break

            # Note: Snake cannot go the opposite direction it is heading
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -SNAKE_BLOCK / 2
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = SNAKE_BLOCK / 2
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -SNAKE_BLOCK / 2
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = SNAKE_BLOCK / 2
                    x1_change = 0

        # Apply change in direction
        x1 += x1_change
        y1 += y1_change

        # Get current coordinates and update snake_list
        snake_head = (x1, y1)
        snake_list.append(snake_head)
        if len(snake_list) >= score:
            del snake_list[0]

        """
        Losing the game
        Either by the snake touching itself
        Or going out of bounds 
        """
        for x, y in snake_list[:-1]:
            if (x, y) == snake_head:
                game_close = True
        if x1 >= WIN_WIDTH - SNAKE_BLOCK or x1 <= BORDER_WIDTH or y1 >= WIN_WIDTH - SNAKE_BLOCK or y1 <= BORDER_WIDTH:
            game_close = True

        # Eat food and update food coordinates
        if (food_x - 20 <= x1 <= food_x + 20) and (food_y - 20 <= y1 <= food_y + 20):
            food_x = get_food_coordinates()
            food_y = get_food_coordinates()
            score += 1

        # Drawing all the elements
        dis.fill(BLACK)
        draw_border()
        draw_snake(snake_list, SNAKE_BLOCK)
        draw_food(food_x, food_y, width)
        pygame.display.update()

        # Frame rate
        clock.tick(30)

    pygame.quit()
    quit()


# Randomly gets coordinates for the food items
def get_food_coordinates():
    return round(random.randrange(BORDER_WIDTH + SNAKE_BLOCK, WIN_WIDTH - SNAKE_BLOCK) / 10.0) * 10.0


# Draw a border around the game
def draw_border():
    pygame.draw.rect(dis, BLUE, [0, 0, BORDER_WIDTH, BORDER])
    pygame.draw.rect(dis, BLUE, [0, 0, BORDER, BORDER_WIDTH])
    pygame.draw.rect(dis, BLUE, [750, 0, BORDER_WIDTH, BORDER])
    pygame.draw.rect(dis, BLUE, [0, 750, BORDER, BORDER_WIDTH])


# Draw the snake via a list of coordinates
def draw_snake(snake_list, width):
    for x, y in snake_list:
        pygame.draw.rect(dis, WHITE, [x, y, width, width])


# Draw the food item
def draw_food(food_x, food_y, width):
    pygame.draw.rect(dis, RED, [food_x, food_y, width, width])


# Display message to screen
def message(msg, color, width=WIN_WIDTH / 4, length=WIN_WIDTH / 2):
    msg = FONT.render(msg, True, color)
    dis.blit(msg, [width, length])


if __name__ == '__main__':
    x1 = WIN_WIDTH / 2
    y1 = WIN_WIDTH / 2

    x1_change = SNAKE_BLOCK
    y1_change = 0

    run(x1, y1, x1_change, y1_change, SNAKE_BLOCK)
