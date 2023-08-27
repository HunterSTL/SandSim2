import pygame
from pygame.locals import *
from Particle import Particle
from Hotbar import Hotbar

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
        add_particle(Particle.spawn(x, y, particle_name))

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

        hotbar.draw(screen, SCREEN_WIDTH, SCREEN_HEIGHT, SCALING)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()