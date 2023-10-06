import pygame

class Label:
    def __init__(self, text, x, y, size, colour, fontname, bold, italic):

        self.text = text
        self.x = x
        self.y = y
        self.dy = -5
        # bold加粗，italic斜体
        self.font = pygame.font.SysFont(fontname, size, bold, italic)
        self.font_colour = pygame.Color(colour)

    def draw(self, screen):

        # 第二个参数抗锯齿
        img = self.font.render(self.text, True, self.font_colour)
        screen.blit(img, (self.x, self.y))

    # def move(self, screen):
    #
    #     width, weight = screen.get_size()
    #
    #     self.y += self.dy
