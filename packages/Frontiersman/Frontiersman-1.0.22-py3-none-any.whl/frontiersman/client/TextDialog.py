import pygame_gui as pg_g


class TextDialog(pg_g.elements.UITextBox):
    def __init__(self, rect, manager, anchors=None, max_lines=100):
        super().__init__('', rect, manager, anchors=anchors)
        self.max_lines = max_lines
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)
        if len(self.lines) == self.max_lines:
            self.lines = self.lines[1:]
        self.html_text = '<br>'.join(reversed(self.lines))
        self.rebuild()
