import pygame, sys
from circleshape import CircleShape
from triangleshape import TriangleShape
from constants import *
from shot import Shot
from rocket import Rocket

class Player(TriangleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.rocket_cooldown_timer = 0
        self.points = 0
        self.lives = PLAYER_LIVES
        self.__last_moved = pygame.time.get_ticks()
        self.speed = PLAYER_DEFAULT_SPEED

    # in the Player class

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.shot_cooldown_timer > 0:
            self.shot_cooldown_timer -= dt
        if self.rocket_cooldown_timer > 0:
            self.rocket_cooldown_timer -= dt

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_r]:
            self.rocket()

    def move(self, dt):
        movement_speed = self.speed

        if (pygame.time.get_ticks() - self.__last_moved) < 100:
            movement_speed = min(self.speed + 1, PLAYER_MAX_SPEED)
        else:
            movement_speed = PLAYER_DEFAULT_SPEED

        self.speed = movement_speed
        self.__last_moved = pygame.time.get_ticks()

        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * movement_speed * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SHOOT_SPEED
        shot.velocity = rotated_with_speed_vector

    def rocket(self):
        if self.rocket_cooldown_timer > 0:
            return

        self.rocket_cooldown_timer = ROCKET_COOLDOWN
        rocket = Rocket(self.position.x, self.position.y)
        rocket.rotation = self.rotation
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * ROCKET_SPEED
        rocket.velocity = rotated_with_speed_vector

    def game_over(self):
        print("Game over!")
        print(f"Total points: {self.points}")
        sys.exit()

    def respawn(self):
        if self.lives == 1:
            print("1 life remaining!")
        else:
            print(f"{self.lives} lives remaining!")
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rotation = 0