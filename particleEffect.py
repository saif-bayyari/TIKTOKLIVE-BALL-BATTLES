import arcade
import random 
from particle import Particle
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600



def singleParticleLeak():

    pass



class ParticleEffect():
    def __init__(self):
        self.particles = [Particle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2) for _ in range(100)]
        for p in self.particles:
            p.draw()
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.center_x += self.velocity_x
        self.center_y += self.velocity_y
        
        
