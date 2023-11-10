import pygame


class ChipDisplay:
    def __init__(self, chip_images, spacing=10):
        # Initializing the ChipDisplay attributes
        self.chip_images = chip_images  # Images of different chips
        self.spacing = spacing  # Spacing between chips
        self.chips = []  # Collection of chips
        self.display_chips = True  # Indicates whether chips are displayed

    def draw_chips(self, surface):
        # Draws the chips on the given surface
        if self.display_chips:
            x = self.spacing
            chip_height = self.chip_images[0].get_height()
            for chip_image in self.chip_images:
                y = surface.get_height() - chip_height
                surface.blit(chip_image, (x, y))
                x += chip_image.get_width() + self.spacing

    def hide(self):
        # Hides the chips
        self.display_chips = False

    def show(self):
        # Displays the chips
        self.display_chips = True

    def get_chip_value(self, surface, x, y, chip_values):
        # Retrieves the value of the chip at the given coordinates
        x_position = self.spacing
        chip_height = self.chip_images[0].get_height()
        for i, chip_image in enumerate(self.chip_images):
            y_position = surface.get_height() - chip_height
            chip_rect = pygame.Rect(x_position, y_position, chip_image.get_width(), chip_image.get_height())
            if chip_rect.collidepoint(x, y):
                return chip_values[i]
            x_position += chip_image.get_width() + self.spacing
        return None

    def is_mouse_over_chip(self, surface, x, y):
        # Checks if the mouse is over a chip
        chip_height = self.chip_images[0].get_height()
        for i, chip_image in enumerate(self.chip_images):
            x_position = i * (chip_image.get_width() + self.spacing)
            y_position = surface.get_height() - chip_height
            if (x_position <= x < x_position + chip_image.get_width() and y_position <= y < y_position + chip_image.get_height()):
                return True, i
        return False, None
