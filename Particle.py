import random

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
        initial_color = PD[name].color
        initial_lifetime = PD[name].lifetime
        burning = PD[name].burning
        state = PD[name].state

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

# Particle Dictionary
PD = {
    "Sand":                 Particle(None, None, "Sand", None, (200, 200, 0), -1, False, "Solid"),
    "Rock":                 Particle(None, None, "Rock", None, (100, 100, 100), -1, False, "Solid"),
    "Water":                Particle(None, None, "Water", None, (100, 100, 255), -1, False, "Liquid"),
    "Wood":                 Particle(None, None, "Wood", None, (100, 50, 0), -1, False, "Solid"),
    "Water Source":         Particle(None, None, "Water Source", None, (28, 21, 189), -1, False, "Solid"),
    "Sand Source":          Particle(None, None, "Sand Source", None, (212, 136, 15), -1, False, "Solid"),
    "Fire":                 Particle(None, None, "Fire", None, (232, 55, 23), 200, True, "Solid"),
    "Smoke":                Particle(None, None, "Smoke", None, (150, 150, 150), 100, False, "Gas"),
    "TNT":                  Particle(None, None, "TNT", None, (255, 0, 0), -1, False, "Solid"),
    "Explosion Particle":   Particle(None, None, "Explosion Particle", None, (255, 150, 20), 10, False, "Gas"),
    "Fuse":                 Particle(None, None, "Fuse", None, (0, 54, 11), -1, False, "Solid"),
    "Lit Fuse":             Particle(None, None, "Lit Fuse", None, (232, 55, 23), 50, True, "Solid")
}