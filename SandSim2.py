import pygame
from pygame.locals import *
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 50
SCALING = 10

screen = pygame.display.set_mode((SCREEN_WIDTH * SCALING, SCREEN_HEIGHT * SCALING + SCALING * 2))

pygame.display.set_caption('Sand Simulation')

def draw_particle(particle):
    pygame.draw.rect(screen, particle.color, (particle.x * SCALING, particle.y * SCALING, SCALING, SCALING))

id = 0
particles = {}

def add_particle(particle):
    global particles
    key = (particle.x, particle.y)
    particles[key] = particle

def get_particle(x, y):
    global particles
    key = (x, y)
    return particles.get(key, None)

def remove_particle(x, y):
    global particles
    key = (x, y)
    if key in particles:
        del particles[key]

def CursorLocation(actual_x, actual_y):
    return actual_x // SCALING, actual_y // SCALING

def BrushStroke(x, y, particle_name):
    if particle_name == "Air":
        remove_particle(x, y)
    else:
        Particle.spawn(x, y, particle_name)

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
        add_particle(particle)
        return particle

class Hotbar:
    def __init__(self, particle_types):
        self.particle_types = particle_types
        self.selected_particle = 0
        self.selected_particle_name = self.particle_types[self.selected_particle]  # Directly get name from the list
        self.brush_size = 1

    def change_brush_size(self, increment):
        if 0 < self.brush_size + increment < 10:
            self.brush_size += increment

    def select_next_block(self):
        self.selected_particle = (self.selected_particle + 1) % (len(self.particle_types))
        self.selected_particle_name = self.particle_types[self.selected_particle]

    def select_previous_block(self):
        self.selected_particle = (self.selected_particle - 1) % (len(self.particle_types))
        self.selected_particle_name = self.particle_types[self.selected_particle]

    def draw(self, screen):
        y_offset = SCREEN_HEIGHT * SCALING  # This will place it right below the game screen
        hotbar_rect = pygame.Rect(0, y_offset, SCREEN_WIDTH * SCALING, 2 * SCALING)
        pygame.draw.rect(screen, (50, 50, 50), hotbar_rect)

        for i, name in enumerate(self.particle_types):
            block_rect = pygame.Rect(i * SCALING * 2, y_offset, SCALING * 2, SCALING * 2)
            pygame.draw.rect(screen, PD[name].color, block_rect)

            if i == self.selected_particle:
                selected_block_rect_outer = pygame.Rect(i * SCALING * 2, y_offset, SCALING * 2, SCALING * 2)
                pygame.draw.rect(screen, (255, 0, 0), selected_block_rect_outer, 2)



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

# Bresenham's Line Algorithm to draw a line between two points
def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    return points

def main():
    running = True
    simulation_running = False  # This variable will toggle with the SPACE key
    drawing = False
    erasing = False
    prev_coord = None
    
    block_types = list(PD.keys())  
    hotbar = Hotbar(block_types)

    while running:
        screen.fill((0, 0, 0))
        particle_type = hotbar.selected_particle_name
        
        # Draw all particles
        for particle in particles.values():
            draw_particle(particle)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_running = not simulation_running
                elif event.key == pygame.K_RIGHT:
                    hotbar.select_next_block()
                elif event.key == pygame.K_LEFT:
                    hotbar.select_previous_block()
                elif event.key == pygame.K_UP:
                    hotbar.change_brush_size(1)
                elif event.key == pygame.K_DOWN:
                    hotbar.change_brush_size(-1)
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    hotbar.select_next_block()
                elif event.y == -1:
                    hotbar.select_previous_block()
            elif event.type == MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                gridX, gridY = mouseX // SCALING, mouseY // SCALING
                prev_coord = (gridX, gridY)

                if event.button == 1:  # Left mouse button
                    drawing = True
                    Particle.spawn(gridX, gridY, particle_type)

                elif event.button == 3:  # Right mouse button
                    erasing = True
                    remove_particle(gridX, gridY)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                elif event.button == 3:
                    erasing = False
                prev_coord = None
            elif event.type == MOUSEMOTION and prev_coord:
                mouseX, mouseY = event.pos
                gridX, gridY = mouseX // SCALING, mouseY // SCALING

                if drawing:
                    for coord in bresenham_line(prev_coord[0], prev_coord[1], gridX, gridY):
                        Particle.spawn(coord[0], coord[1], particle_type)

                if erasing:
                    for coord in bresenham_line(prev_coord[0], prev_coord[1], gridX, gridY):
                        remove_particle(coord[0], coord[1])

                prev_coord = (gridX, gridY)

        hotbar.draw(screen)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()