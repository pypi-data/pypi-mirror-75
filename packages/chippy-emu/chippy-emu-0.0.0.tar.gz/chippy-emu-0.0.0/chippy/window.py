"""Chip8 display and keypad."""

import pygame

def to_number(s):
    """Convert one-hexdigit hexstring or KeyCode to number."""
    try:
        return int(s, 16) & 0xf
    except ValueError:
        pass
    except TypeError:
        pass

def press(chip8, key):
    """Press key on chip-8 keypad."""
    shift_amount = to_number(key)
    if shift_amount is None:
        return
    mask = 1 << shift_amount
    chip8.keypad |= mask

    # Handle op_fx0a
    if chip8.waiting:
        index = chip8.waiting.pop()
        chip8.registers[index] = shift_amount

def release(chip8, key):
    """Release key on chip-8 keypad."""
    shift_amount = to_number(key)
    if shift_amount is None:
        return
    mask = 0xffff
    mask -= (1 << shift_amount)
    chip8.keypad &= mask

def convert_key(key):
    """Convert pygame key constant to hex character."""
    return chr(key)

def draw_pixel(x, y, scale=1):
    """Draw pixel on the display."""
    surface = pygame.display.get_surface()
    rect = pygame.Rect(x * scale, y * scale, scale, scale)
    color = pygame.Color(255, 255, 255)
    pygame.draw.rect(surface, color, rect)

class Window:
    def __init__(self, chip8):
        self.width = 64
        self.height = 32
        self.scale = 12

        self.chip8 = chip8

    @property
    def screen_size(self):
        """Get screen size."""
        return (self.width * self.scale, self.height * self.scale)

    def render(self):
        """Render chip8 sprites."""
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        for y, row in enumerate(self.chip8.display):
            x = 0
            bits = row
            while bits:
                cell = 0x8000000000000000 & bits
                if cell:
                    draw_pixel(x, y, self.scale)
                bits &= 0x7fffffffffffffff
                bits <<= 1
                x += 1
        pygame.display.update()

    def init_screen(self):
        """Initialize screen."""
        pygame.init()
        pygame.display.set_caption("Chippy")
        self.screen = pygame.display.set_mode(self.screen_size)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.chip8.running = False
                return
            if event.type == pygame.KEYDOWN:
                key = convert_key(event.key)
                press(self.chip8, key)
            elif event.type == pygame.KEYUP:
                key = convert_key(event.key)
                release(self.chip8, key)
