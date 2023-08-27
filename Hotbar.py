import pygame

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

    def draw(self, screen, screen_width, screen_height, scaling):
        y_offset = screen_height * scaling  # This will place it right below the game screen
        hotbar_rect = pygame.Rect(0, y_offset, screen_width * scaling, 2 * scaling)
        pygame.draw.rect(screen, (50, 50, 50), hotbar_rect)

        for i, name in enumerate(self.particle_types):
            block_rect = pygame.Rect(i * scaling * 2, y_offset, scaling * 2, scaling * 2)
            pygame.draw.rect(screen, PD[name].color, block_rect)

            if i == self.selected_particle:
                selected_block_rect_outer = pygame.Rect(i * scaling * 2, y_offset, scaling * 2, scaling * 2)
                pygame.draw.rect(screen, (255, 0, 0), selected_block_rect_outer, 2)