import pygame


class WinWindow:
    def __init__(self, size, font, who_won='Zander', won=False):
        self.graphics = pygame.Surface(size, flags=pygame.SRCALPHA)

        self.message = []

        if won:
            self.message.append('You won the game!')
            self.message.append('Congratulations!')
        else:
            self.message.append(who_won + ' won the game.')
            self.message.append('Better luck next time.')

    def get_graphics(self):
        return self.graphics
