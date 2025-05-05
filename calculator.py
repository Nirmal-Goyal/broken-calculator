import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings (BIGGER SIZE + RESIZABLE)
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Broken Calculator")

# Now safe to init clipboard
pygame.scrap.init()

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
ORANGE = (255, 165, 0)
RED = (255, 99, 71)
GREEN = (144, 238, 144)
PURPLE = (186, 85, 211)

# Fonts (Bigger for input, smaller for buttons)
font = pygame.font.SysFont(None, 60)  # Bigger font for current input
button_font = pygame.font.SysFont(None, 40)  # Smaller font for button text
small_font = pygame.font.SysFont(None, 35)

# Calculator state
current_input = ""
history = []

# Buttons (label, position)
buttons = [
    ('7', (0, 1)), ('8', (1, 1)), ('9', (2, 1)), ('/', (3, 1)),
    ('4', (0, 2)), ('5', (1, 2)), ('6', (2, 2)), ('*', (3, 2)),
    ('1', (0, 3)), ('2', (1, 3)), ('3', (2, 3)), ('-', (3, 3)),
    ('0', (0, 4)), ('.', (1, 4)), ('=', (2, 4)), ('+', (3, 4)),
    ('C', (0, 5)), ('AC', (1, 5)), ('Undo', (2, 5)), ('Copy', (3, 5))
]

# Function to draw the calculator interface
def draw():
    screen.fill(WHITE)
    width, height = screen.get_size()  # Get window size

    # Dynamically resize input and buttons based on window size
    button_width = width // 5  # Adjust width for smaller buttons
    button_height = height // 8  # Divide screen into 8 rows for buttons to fit better

    # Draw history
    y_offset = 20
    for item in history[-3:]:
        history_text = small_font.render(item, True, DARK_GRAY)
        screen.blit(history_text, (10, y_offset))
        y_offset += 30

    # Draw current input
    input_rect = pygame.Rect(10, 90, width - 20, 40)
    pygame.draw.rect(screen, LIGHT_GRAY, input_rect, border_radius=8)
    input_text = font.render(current_input, True, BLACK)
    screen.blit(input_text, (15, 90))

    # Draw buttons
    for (text, pos) in buttons:
        button_rect = pygame.Rect(pos[0] * button_width, pos[1] * button_height + 150, button_width - 10, button_height - 10)  # Adjust button size

        # Color buttons differently
        if text in ['+', '-', '*', '/']:
            color = ORANGE
        elif text in ['=', 'C', 'AC', 'Undo', 'Copy']:
            if text == '=':
                color = GREEN
            elif text == 'Undo':
                color = BLUE
            elif text == 'Copy':
                color = PURPLE  # Purple for Copy button
            else:
                color = RED
        else:
            color = GRAY

        pygame.draw.rect(screen, color, button_rect, border_radius=12)

        # Use the smaller font for button text
        label = button_font.render(text, True, BLACK)
        label_rect = label.get_rect(center=button_rect.center)
        screen.blit(label, label_rect)

    pygame.display.update()

# Function to copy text to clipboard
def copy_to_clipboard(text):
    pygame.scrap.put(pygame.SCRAP_TEXT, text.encode('utf-8'))

# Function to handle button clicks
def handle_click(pos):
    global current_input, history

    for (text, button_pos) in buttons:
        button_rect = pygame.Rect(button_pos[0] * (WIDTH // 5), button_pos[1] * (HEIGHT // 8) + 150, WIDTH // 5 - 10, HEIGHT // 8 - 10)
        if button_rect.collidepoint(pos):
            if text == 'C':
                current_input = current_input[:-1]  # Clear last character
            elif text == 'AC':
                current_input = ""
                history = []
            elif text == 'Undo':
                if history:
                    last_entry = history.pop()
                    if '=' in last_entry:
                        restored_expr = last_entry.split('=')[0].strip()
                        current_input = restored_expr
            elif text == 'Copy':
                if current_input:
                    copy_to_clipboard(current_input)
            elif text == '=':
                try:
                    result = str(eval(current_input))
                    history.append(f"{current_input} = {result}")
                    current_input = result
                except ZeroDivisionError:
                    current_input = "Cannot divide by zero"
                except SyntaxError:
                    current_input = "Syntax Error"
                except Exception:
                    current_input = "Error"
            elif text == '.':
                if '.' not in current_input.split(' ')[-1]:
                    current_input += text
            else:
                current_input += text

# Function to handle keyboard input
def handle_keyboard_input(event):
    global current_input

    key = event.key
    if key == pygame.K_0:
        current_input += '0'
    elif key == pygame.K_1:
        current_input += '1'
    elif key == pygame.K_2:
        current_input += '2'
    elif key == pygame.K_3:
        current_input += '3'
    elif key == pygame.K_4:
        current_input += '4'
    elif key == pygame.K_5:
        current_input += '5'
    elif key == pygame.K_6:
        current_input += '6'
    elif key == pygame.K_7:
        current_input += '7'
    elif key == pygame.K_8:
        current_input += '8'
    elif key == pygame.K_9:
        current_input += '9'
    elif key == pygame.K_PLUS or key == pygame.K_EQUALS:
        current_input += '+'
    elif key == pygame.K_MINUS:
        current_input += '-'
    elif key == pygame.K_ASTERISK:
        current_input += '*'
    elif key == pygame.K_SLASH:
        current_input += '/'
    elif key == pygame.K_PERIOD:
        if '.' not in current_input.split(' ')[-1]:
            current_input += '.'
    elif key == pygame.K_RETURN:
        handle_click((250, 450))  # Simulate "=" button click
    elif key == pygame.K_BACKSPACE:
        current_input = current_input[:-1]

# Main loop
running = True
while running:
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_click(event.pos)
        elif event.type == pygame.KEYDOWN:
            handle_keyboard_input(event)

pygame.quit()
sys.exit()
