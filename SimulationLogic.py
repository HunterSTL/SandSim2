from Particle import *
import random
from Constants import *

def IsWithinGrid(x, y):
    return 1 <= x <= GRID_WIDTH and 1 <= y <= GRID_HEIGHT

def Move(particle, dx, dy):
    RemoveParticle(particle.x, particle.y)  # Remove particle from current position
    AddParticle(Particle(particle.x + dx, particle.y + dy,  #Spawn new particle at new position
                         particle.name, particle.id,
                         particle.color, particle.lifetime,
                         particle.burning, particle.state))

def SwapPositions(particle1, particle2):
    # Swapping positions of two particles
    particle1.x, particle2.x = particle2.x, particle1.x
    particle1.y, particle2.y = particle2.y, particle1.y
    # Update the particles dictionary to reflect these changes
    RemoveParticle(particle1.x, particle1.y)
    RemoveParticle(particle2.x, particle2.y)
    AddParticle(particle1)
    AddParticle(particle2)

def SimulateParticles(particles):
    particles_to_update = list(particles.values())
    random.shuffle(particles_to_update)

    for particle in particles_to_update:
        if particle.name == "Sand":
            # Defining the potential move directions (dx, dy) for below, bottom-left, bottom-right
            directions = [(0, -1), (-1, -1), (1, -1)]

            for dx, dy in directions:
                new_x, new_y = particle.x + dx, particle.y + dy
                neighbor = GetParticle(new_x, new_y)

                # If the neighboring cell is within the grid and either empty or contains a Liquid/Gas
                if IsWithinGrid(new_x, new_y):
                    if neighbor is None:
                        Move(particle, dx, dy)
                        break
                    elif neighbor.state in ["Liquid", "Gas"]:
                        SwapPositions(particle, neighbor)
                        break
        elif particle.name == "Water":
            # Defining the potential move directions (dx, dy) for below, bottom-left, bottom-right
            directions = [(0, -1), (-1, -1), (1, -1), (-1, 0), (1, 0)]

            for dx, dy in directions:
                new_x, new_y = particle.x + dx, particle.y + dy
                neighbor = GetParticle(new_x, new_y)

                # If the neighboring cell is within the grid and either empty or contains a Liquid/Gas
                if IsWithinGrid(new_x, new_y):
                    if neighbor is None:
                        Move(particle, dx, dy)
                        break