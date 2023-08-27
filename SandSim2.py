import pygame
from pygame.locals import *
from Particle import *
from Hotbar import Hotbar
from Particle_Dictionary import PD
from SimulationLogic import SimulateParticles
from Constants import *

# Initialize pygame
pygame.init()

screen = pygame.display.set_mode((GRID_WIDTH * SCALING, GRID_HEIGHT * SCALING + HOTBAR_SIZE))

pygame.display.set_caption('Sand Simulation')

def DrawParticle(particle):
    pygame.draw.rect(screen, particle.color, ((particle.x - 1) * SCALING, (GRID_HEIGHT - particle.y) * SCALING, SCALING, SCALING))

def CursorLocation(actual_x, actual_y):
    # Inside game grid
    if 0 <= actual_x < GRID_WIDTH * SCALING and 0 <= actual_y < GRID_HEIGHT * SCALING:
        x = actual_x // SCALING + 1
        y = (GRID_HEIGHT * SCALING - actual_y) // SCALING + 1
        return x, y
    return -1, -1

def DrawBrushOutline(screen, hotbar, scaling, grid_height):
    actual_mouse_x, actual_mouse_y = pygame.mouse.get_pos()
    mouse_x, mouse_y = CursorLocation(actual_mouse_x, actual_mouse_y)

    # Don't draw outline if position is outside game grid
    if mouse_x < 0 or mouse_y < 0:
        return

    brush_size = hotbar.brush_size
    brush_rect = pygame.Rect((mouse_x - brush_size) * scaling, 
                                (grid_height - mouse_y - brush_size + 1) * scaling, 
                                (2 * brush_size - 1) * scaling, 
                                (2 * brush_size - 1) * scaling)
    pygame.draw.rect(screen, (255, 255, 255), brush_rect, 1)

def BrushStroke(x, y, particle_name, size, erasing):
    # Outside game grid
    if x < 0 or y < 0:
        return
    
    for dx in range(x + 1 - size, x + size): 
        for dy in range(y + 1 - size, y + size):
            if erasing:
                RemoveParticle(dx, dy)
            else:
                AddParticle(Particle.spawn(dx, dy, particle_name))

# Bresenham's Line Algorithm to draw a line between two points
def BresenhamLine(x0, y0, x1, y1):
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
    simulation_running = True  # This variable will toggle with the SPACE key
    drawing = False
    erasing = False
    prev_coord = None
    
    block_types = list(PD.keys())  
    hotbar = Hotbar(block_types)
    clock = pygame.time.Clock()

    while running:
        screen.fill((0, 0, 0))
        
        # Simulate all particles
        SimulateParticles(particles)

        # Draw all particles
        for particle in particles.values():
            DrawParticle(particle)

        # Handle user input
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
                gridX, gridY = CursorLocation(mouseX, mouseY)
                prev_coord = (gridX, gridY)

                if event.button == 1:  # Left mouse button
                    drawing = True
                    BrushStroke(gridX, gridY, hotbar.selected_particle_name, hotbar.brush_size, 0)

                elif event.button == 3:  # Right mouse button
                    erasing = True
                    BrushStroke(gridX, gridY, hotbar.selected_particle_name, hotbar.brush_size, 1)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                elif event.button == 3:
                    erasing = False
                prev_coord = None
            elif event.type == MOUSEMOTION and prev_coord:
                mouseX, mouseY = event.pos
                gridX, gridY = CursorLocation(mouseX, mouseY)

                # Check if either the new cursor position or the previous position is invalid
                if (gridX, gridY) == (-1, -1) or prev_coord == (-1, -1):
                    continue

                if drawing:
                    for coord in BresenhamLine(prev_coord[0], prev_coord[1], gridX, gridY):
                        BrushStroke(coord[0], coord[1], hotbar.selected_particle_name, hotbar.brush_size, 0)

                if erasing:
                    for coord in BresenhamLine(prev_coord[0], prev_coord[1], gridX, gridY):
                        BrushStroke(coord[0], coord[1], hotbar.selected_particle_name, hotbar.brush_size, 1)

                prev_coord = (gridX, gridY)

        DrawBrushOutline(screen, hotbar, SCALING, GRID_HEIGHT)
        hotbar.draw(screen, GRID_WIDTH, GRID_HEIGHT, SCALING)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()