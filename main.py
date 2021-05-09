# TODO LIST
# Map working
import pygame
from pygame.locals import *
import time
import random
import math

SIZE = 40
SCALE = 5
BACKGROUND_COLOR = (209, 229, 231)

WIDTH = SCALE * 160  # Make sure is divisible by size 4:3
HEIGHT = SCALE * 120  # Make sure is divisible by size
TAGS = ['b1', 'b2', 'b3', 'b4']


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Receiver:
    def __init__(self, parent_screen, x, y, tag):
        self.tag = tag
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/"+tag+".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.x = x
        self.y = y

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))


class Generator:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/machine.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.x = -10
        self.y = 20
        self.separation = 0

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def to_gen(self):
        if self.separation == 0:
            self.separation += 1
            return True
        else:
            self.separation = (self.separation + 1) % random.randint(5, 8)
            return False


class Track:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/track.jpg").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.positions = [(0, 40)]
        for i in range(1, 50):
            self.positions.append((i * 40, 40))
        for i in range(1, 50):
            self.positions.append((200, i * 40))
        for i in range(1, 50):
            self.positions.append((200 + i * 40, 150))
        for i in range(1, 50):
            self.positions.append((300, 40 + i * 40))

    def draw(self):
        for position in self.positions:
            self.parent_screen.blit(self.image, (position[0], position[1]))


class Switch:
    def __init__(self, parent_screen, x, y):
        self.state = 0
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/A0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image = rot_center(self.image, -90)
        self.x = x
        self.x = x
        self.y = y

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def change(self):
        self.image = rot_center(self.image, 90)
        rot_center(self.image, 90)
        self.state = (self.state + 90) % 360


class Package:
    def __init__(self, parent_screen):
        self.tag = random.choice(TAGS)
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/" + self.tag + ".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.direction = 'down'

        self.x = 40
        self.y = 40

        self.x_vel = 1
        self.y_vel = 0

    def draw(self):
        self.x += self.x_vel * SIZE
        self.y += self.y_vel * SIZE
        self.parent_screen.blit(self.image, (self.x, self.y))


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("REMOTE ACCESS CONTROL: RUDOLF FACTORY 12")

        pygame.mixer.init()
        self.play_background_music()
        self.score = 1

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))

        # Initializing and drawing switches
        self.switches = [Switch(self.surface, 0, 40),
                         Switch(self.surface, 200, 40),
                         Switch(self.surface, 300, 40),
                         Switch(self.surface, 200, 150),
                         Switch(self.surface, 300, 150)]
        for switch in self.switches:
            switch.draw()

        self.packages = []
        for package in self.packages:
            package.draw()

        # Initializing and drawing tracks
        self.tracks = Track(self.surface)
        self.tracks.draw()

        # Initializing and drawing tracks
        self.receivers = [Receiver(self.surface, 700, 40, 'm1'),
                          Receiver(self.surface, 700, 150, 'm2'),
                          Receiver(self.surface, 200, 560, 'm3'),
                          Receiver(self.surface, 300, 560, 'm4')]
        for receiver in self.receivers:
            receiver.draw()

        # Initializing and drawing tracks
        self.generator = Generator(self.surface)
        self.generator.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/background.ogg')
        pygame.mixer.music.play(-1, 0)

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        # TODO
        # self. = Train(self.surface)
        # self.apple = Apple(self.surface)
        pass

    def is_collision(self, x1, y1, x2, y2):
        center1 = [x1+20,y1+20]
        center2 = [x2+20,y2+20]

        # print(math.dist(center1, center2))

        if math.dist(center1, center2) < 40:
            return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.tracks.draw()
        for switch in self.switches:
            switch.draw()
        for package in self.packages:
            package.draw()
        for receiver in self.receivers:
            receiver.draw()
        self.generator.draw()
        self.display_score()
        pygame.display.flip()

        try:
            for i in range(len(self.packages)):
                for receiver in self.receivers:
                    if self.is_collision(receiver.x, receiver.y, self.packages[i].x, self.packages[i].y):
                        if receiver.tag[-1] == package.tag[-1]:
                            self.score += 1
                        self.packages.pop(i)

        except IndexError:
            print('Deletion successfully')

        # Changing package direction after collision with switch
        for package in self.packages:
            for switch in self.switches:
                if self.is_collision(package.x, package.y, switch.x,
                                     switch.y):
                    if switch.state == 0:
                        package.x_vel = 1
                        package.y_vel = 0
                    elif switch.state == 90:
                        package.x_vel = 0
                        package.y_vel = -1
                    elif switch.state == 180:
                        package.x_vel = -1
                        package.y_vel = 0
                    elif switch.state == 270:
                        package.x_vel = 0
                        package.y_vel = 1
                    elif switch.state == 360:
                        package.x_vel = 1
                        package.y_vel = 0
                    package.x = switch.x
                    package.y = switch.y

        if self.generator.to_gen():
            self.packages.append(Package(self.surface))

        on_track = False
        # for package in self.packages:
        #     for track in self.tracks.positions:
        #         if self.is_collision(package.x, package.y, track[0], track[1]):
        #             on_track = True
        #             break
        #     if not on_track:
        #         raise Exception('Run for you life')

        for i in range(len(self.packages)):
            for track in self.tracks.positions:
                if self.is_collision(self.packages[i].x, self.packages[i].y, track[0], track[1]):
                    on_track = True
                    break
            if not on_track:
                try:
                    self.packages.pop(i)
                except IndexError:
                    print('Deletion successfully')
                raise Exception('Run for you life')

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.score}", True, (0, 0, 0))
        self.surface.blit(score, (500, 350))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line = font.render(f"Whoops. The noise was loud and Santa has fired you.", True, (255, 255, 255))
        self.surface.blit(line, (50, 50))
        line = font.render(f"Your score was {self.score}", True, (255, 255, 255))
        self.surface.blit(line, (50, 80))

        line = font.render("* To plead to Santa, and play game please press enter.", True, (255, 255, 255))
        self.surface.blit(line, (100, 200))
        line = font.render("* To start fresh rerun the script", True, (255, 255, 255))
        self.surface.blit(line, (100, 250))
        line = font.render("* To leave the game press Escape!", True, (255, 255, 255))
        self.surface.blit(line, (100, 300))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                elif event.type == QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for switch in self.switches:
                        if self.is_collision(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], switch.x, switch.y):
                            switch.change()
                            print([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], switch.x, switch.y])

            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)

if __name__ == '__main__':
    game = Game()
    game.run()