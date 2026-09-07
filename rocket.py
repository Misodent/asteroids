import pygame, random
from triangleshape import TriangleShape
from circleshape import CircleShape
from constants import *

class Rocket(TriangleShape):
    def __init__(self, x, y):
        super().__init__(x, y, ROCKET_RADIUS)

    def update(self, dt):
        super().update(dt)
        self.emit_fuel()

    def emit_fuel(self):
        angle = random.uniform(160, 200)
        new_velocity = self.velocity.rotate(angle)
        explosion_particle = CircleShape(
            self.position.x, 
            self.position.y, 
            EXPLOSION_PARTICLE_SIZE
            )
        explosion_particle.velocity = new_velocity * 1.2