import pygame
import neat
import time
import os
import random
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

STAT_FONT = pygame.font.SysFont("comicsans", 50)
#END_FONT = pygame.font.SysFont("comicsans", 70)
#DRAW_LINES = False

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.FULLSCREEN)


# Bird images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird" + str(x) + ".png")).convert_alpha())
             for x in range(1, 4)]
# Pipe image
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")).convert_alpha())
# Ground base image
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")).convert_alpha())
# Background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")).convert_alpha())


class Bird:
    """
    Class: Bird
    """
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    # starting coordinates of the bird
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    # Jump Method
    def jump(self):
        self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    # Move Method
    def move(self):
        self.tick_count += 1
        # pixels displacement, which is a physics equation
        # e.g for jump - velocity will increase at a decreasing rate based on this formula before coming down
        d = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        # terminal velocity, so that bird doesn't drop down too fast
        d = min(d, 16)

        # fine tuning movement when going up
        if d < 0:
            d -= 2

        # change y based on d
        self.y = self.y + d

        # Tilting

        # check if on upward jump trajectory - height from where the bird jumped + 50
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                # immediately set tile to Max Rotation
                self.tilt = self.MAX_ROTATION
        else:  # downward jump trajectory
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        # Set the wing position based on the animation time
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # set wings to freeze if tilting downwards
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            # when you press jump after the falling animation, it quickly jumps back to level
            self.img_count = self.ANIMATION_TIME * 2

        # rotate the image around the center of bird image
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    """
    Class: Pipe
    """

    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        # Top and bottom of the pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    # Helper function to randomly get pip height
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        # change x position based on the velocity
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # Complex collide function that compares the masks of the bird and pipe object
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # figuring out pixel-perfect collision here
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # Gets the point of collision between bird and bottom pipe, if no collision return None
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        return b_point or t_point


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y

        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))


def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()


def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]

    win = WIN
    win.set_alpha(None)
    clock = pygame.time.Clock()

    # Game score
    score = 0

    run = True
    while run:
        # FPS limit
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # bird.move

        # removed pipes
        rem = []

        # Var to check if we need to add a pipe
        add_pipe = False

        for pipe in pipes:
            if pipe.collide(bird):
                pass
            # pipe is off the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True
            pipe.move()

        # Add a pipe
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        # remove passed pipes from pipe
        for r in rem:
            pipes.remove(r)

        # hit the floor
        if bird.y + bird.img.get_height() >= 730:
            pass

        base.move()
        draw_window(win, bird, pipes, base, score)

    pygame.quit()
    quit()


if __name__ == '__main__':
    pygame.init()
    main()
