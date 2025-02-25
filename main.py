import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, ASTEROID_MIN_RADIUS, ASTEROID_KINDS, ASTEROID_SPAWN_RATE, ASTEROID_MAX_RADIUS, COLOR_BLACK, GAME_TITLE
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from shot import Shot

class Game:
    def __init__(self):
        self.running = True
        self.initialize_display()
        self.initialize_game_objects()
        self.initialize_game_clock()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type ==pygame.QUIT:
                    return
            self.paint_background()
            for updatable in self.updatables:
                updatable.update(self.dt) 
            for asteroid in self.asteroids:
                self.check_player_collision(asteroid)
                for shot in self.shots:
                    self.check_shot_collision(asteroid, shot)
            for drawable in self.drawables:
                drawable.draw(self.screen)
            self.refresh_screen()
            self.dt = self.clock.tick(FPS) / 1000

    def initialize_display(self):
       self.resolution = (SCREEN_WIDTH, SCREEN_HEIGHT)
       self.screen = pygame.display.set_mode(self.resolution)
       pygame.display.set_caption(GAME_TITLE) 

    def initialize_game_objects(self):
        self.make_groups()
        self.fill_groups()
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()
        
    def make_groups(self):
        self.updatables = pygame.sprite.Group()
        self.drawables =  pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()

    def fill_groups(self):
        Player.containers = (self.updatables, self.drawables)
        Shot.containers = (self.updatables, self.drawables, self.shots)
        Asteroid.containers = (self.updatables, self.drawables, self.asteroids)
        AsteroidField.containers = (self.updatables,)
        
    def initialize_game_clock(self):
        self.clock = pygame.time.Clock()
        self.dt = 0

    def paint_background(self):
        self.screen.fill(COLOR_BLACK)

    def refresh_screen(self):
        pygame.display.flip()

    def check_player_collision(self, asteroid):
        if self.player.collision_detection(asteroid) == True:
            print("Game over!")
            exit()
        else:
            pass

    def check_shot_collision(self, asteroid, shot):
        if shot.collision_detection(asteroid) == True:
            asteroid.split()
            shot.kill()
            asteroid.kill()

# Initiates pygame, creates and starts the game object. 
def main():
    pygame.init()
    print("Starting asteroids!")
    game = Game()
    game.run()

if __name__ == "__main__":
    main()