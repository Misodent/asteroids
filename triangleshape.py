import pygame, random
from circleshape import CircleShape
from constants import *

# Base class for game objects
class TriangleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.rotation = 0
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius < distance:
            return False

        return True

    def explode(self):
        for i in range(EXPLOSION_PARTICLES):
            angle = random.uniform(0, 360)
            new_velocity = self.velocity.rotate(angle)
            explosion_particle = CircleShape(
                self.position.x, 
                self.position.y, 
                EXPLOSION_PARTICLE_SIZE
                )
            explosion_particle.velocity = new_velocity * 5