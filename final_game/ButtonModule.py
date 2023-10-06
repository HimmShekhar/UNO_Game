import pygame


class Button:
    def __init__(self, x, y, label_text, image_path, image_pressed_path, font_name, font_size, font_bold, font_italic, font_color):
        self.x = x
        self.y = y
        self.label_text = label_text
        self.unpressed = pygame.image.load(image_path)
        self.pressed = pygame.image.load(image_pressed_path)
        self.size = self.unpressed.get_size()

        self.font = pygame.font.SysFont(font_name, font_size, font_bold, font_italic)
        self.font_colour = pygame.Color(font_color)

    def draw(self, screen):
        is_pressed = pygame.mouse.get_pressed()[0] \
                     and self.coord_inside_button(pygame.mouse.get_pos())
        screen.blit(self.pressed if is_pressed else self.unpressed, (self.x, self.y))

        img = self.font.render(self.label_text, True, self.font_colour)

        label_width, label_height = img.get_size()

        label_x = self.x + (self.size[0] / 2 - label_width / 2)
        label_y = self.y + (self.size[1] / 2 - label_height / 2)

        screen.blit(img, (label_x, label_y))


    def coord_inside_button(self, coord):
        return self.x <= coord[0] <= self.x + self.size[0] \
                and self.y <= coord[1] <= self.y + self.size[1]
