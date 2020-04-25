import pygame
import neat
import time
import os
import random

pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

GEN = -1

STAT_FONT = pygame.font.SysFont("comicsans", 50)

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.FULLSCREEN, pygame.RESIZABLE)

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


def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render('Score: ' + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render('Gen: ' + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    text = STAT_FONT.render('Alive: ' + str(len(birds)), 1, (255, 255, 255))
    win.blit(text, (10, 40))

    base.draw(win)

    for bird in birds:
        bird.draw(win)

    pygame.display.update()


def main(genomes, config):
    # keep track of the number of generations
    global GEN
    GEN += 1

    nets = []
    ge = []
    birds = []

    # Genome is tuple so we need the _,
    for _, g in genomes:
        """
        Set up Bird, NN for bird, and Genome for bird
        """
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(700)]

    win = WIN
    win.set_alpha(None)
    clock = pygame.time.Clock()

    # Game score
    score = 0

    running = True

    while running:
        # FPS limit
        clock.tick(30)

        for event in pygame.event.get():
            # Quit when window is closed
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            # Quit if exit key is pressed
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()
                quit()

        # checking which pipe (0 or 1) we have to use for our NN
        pipe_ind = 0
        if len(birds) > 0:
            first_pipe = pipes[0]
            if len(pipes) > 1 and birds[0].x > first_pipe.x + first_pipe.PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            break

        for index, bird in enumerate(birds):
            bird.move()
            ge[index].fitness += 0.1

            # Activate the neural network with inputs
            output = nets[index].activate((bird.y,
                                           abs(bird.y - pipes[pipe_ind].height),  # distance from top pipe
                                           abs(bird.y - pipes[pipe_ind].bottom)   # distance from bottom pipe
                                           ))
            """
            Check the value of output from the NN
            output Neuron is a list
            Jump if over 0.5
            """
            if output[0] > 0.5:
                bird.jump()

        # removed pipes
        rem = []

        # Var to check if we need to add a pipe
        add_pipe = False

        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.collide(bird):
                    # prevent birds only hitting the pipes to have high fitness
                    ge[index].fitness -= 1
                    # remove all instances of the bird from the list
                    birds.pop(index)
                    nets.pop(index)
                    ge.pop(index)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            # pipe is off the screen
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            pipe.move()

        # Add a pipe
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))

        # remove passed pipes from pipe
        for r in rem:
            pipes.remove(r)

        for index, bird in enumerate(birds):
            # hits the floor
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(index)
                nets.pop(index)
                ge.pop(index)

        if score > 20:
            break

        # Move the ground along
        base.move()

        draw_window(win, birds, pipes, base, score, GEN)


def run(config_path):
    # Config the fields of the of neat AI
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)
    # Population
    p = neat.Population(config)

    # Display statistics
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # main will be our fitness function
    winner = p.run(main, 50)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')

    run(config_path)
