import pygame, sys
from constants import *
from logger import log_state, log_event
from circleshape import CircleShape
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print(f"{PLAYER_LIVES} lives remaining!")
 
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # Groups
    updatable = pygame.sprite.Group()
    drawables = pygame.sprite.Group()
    wrappables = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Objects
    CircleShape.containers = (updatable, drawables)
    Player.containers = (updatable, drawables, wrappables)
    Asteroid.containers = (updatable, drawables, asteroids, wrappables)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawables, shots)

    # Instantiate player at center of screen
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)
    asteroid_field = AsteroidField()

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")

        # Update and draw
        updatable.update(dt)
        for drawable in drawables:
            drawable.draw(screen)

        for wrappable in wrappables:
            if wrappable.position.x < 0:
                wrappable.position.x = SCREEN_WIDTH
            if wrappable.position.y < 0:
                 wrappable.position.y = SCREEN_HEIGHT
            if wrappable.position.x > SCREEN_WIDTH:
                wrappable.position.x = 0
            if wrappable.position.y > SCREEN_HEIGHT:
                wrappable.position.y = 0
        
        # Asteroid crashing
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                player.explode()
                player.lives -= 1
                if player.lives > 0:
                    player.respawn()
                else:
                    player.game_over()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    points_earned = round(max(
                        ASTEROID_MAX_POINTS - ((5/2) * asteroid.radius - 50), 
                        ASTEROID_MIN_POINTS
                        ))
                    player.points += points_earned
                    print(f"+{points_earned} points!")
                    shot.kill()
                    asteroid.split()

        # Fps
        pygame.display.flip()
        tick = clock.tick(60)
        dt = tick / 1000

if __name__ == "__main__":
    main()
