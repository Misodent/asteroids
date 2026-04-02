import pygame, random
from constants import *
from circleshape import CircleShape
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.explode()
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        new_velocity_0 = self.velocity.rotate(angle)
        new_velocity_1 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        new_asteroid_0 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
        new_asteroid_0.velocity = new_velocity_0 * 1.2
        new_asteroid_1.velocity = new_velocity_1 * 1.2