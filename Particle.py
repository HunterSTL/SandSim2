import random
from Particle_Dictionary import PD

id = 0

particles = {}

def AddParticle(particle):
    global particles
    key = (particle.x, particle.y)
    particles[key] = particle

def GetParticle(x, y):
    global particles
    key = (x, y)
    return particles.get(key, None)

def RemoveParticle(x, y):
    global particles
    key = (x, y)
    if key in particles:
        del particles[key]

class Particle:
    def __init__(self, x, y, name, id, color, lifetime, burning, state):
        self.x = x
        self.y = y
        self.name = name
        self.id = id
        self.color = color
        self.lifetime = lifetime
        self.burning = burning
        self.state = state

    @classmethod
    def spawn(cls, x, y, name):
        global id
        id += 1
        particle_data = PD[name]
        initial_color = particle_data["color"]
        initial_lifetime = particle_data["lifetime"]
        burning = particle_data["burning"]
        state = particle_data["state"]

        if initial_lifetime != -1:
            # between 80% and 100% 
            lifetime_modifyer = random.random() * 0.2 + 0.8
            initial_lifetime = int(initial_lifetime * lifetime_modifyer)
            r = int(initial_color[0] * lifetime_modifyer)
            g = int(initial_color[1] * lifetime_modifyer)
            b = int(initial_color[2] * lifetime_modifyer)
            initial_color = (r, g, b)
        
        # add newly spawned particle to the particles dictionary
        particle = cls(x, y, name, id, initial_color, initial_lifetime, burning, state)
        return particle