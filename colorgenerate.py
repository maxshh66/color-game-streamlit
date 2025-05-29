import random

# Generate a base color
def generate_color():
    r = random.randint(50, 200)
    g = random.randint(50, 200)
    b = random.randint(50, 200)
    return f"#{r:02x}{g:02x}{b:02x}", (r, g, b)

# Adjust brightness of a color
def adjust_brightness(rgb, factor=1.2):
    r, g, b = rgb
    r = min(max(int(r * factor), 0), 255)
    g = min(max(int(g * factor), 0), 255)
    b = min(max(int(b * factor), 0), 255)
    return f"#{r:02x}{g:02x}{b:02x}"