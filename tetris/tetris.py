import pygame
import random
import os

# --- Add these at the top, after your imports and before your config ---
def get_screen_size(fullscreen):
    if fullscreen:
        info = pygame.display.Info()
        return info.current_w, info.current_h
    else:
        return CELL_SIZE * COLS, CELL_SIZE * ROWS  # <-- Remove +50 here!

def recalc_sizes(screen_width, screen_height):
    # Leave 50px for buttons at the bottom
    grid_height = screen_height - 50
    cell_size = min(screen_width // COLS, grid_height // ROWS)
    width = cell_size * COLS
    height = cell_size * ROWS
    return cell_size, width, height

# Game config
CELL_SIZE = 30
COLS = 10
ROWS = 20
WIDTH = CELL_SIZE * COLS
HEIGHT = CELL_SIZE * ROWS
FPS = 60

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
]
COLORS = [
    (0, 255, 255), (255, 255, 0), (128, 0, 128),
    (0, 0, 255), (255, 165, 0), (0, 255, 0), (255, 0, 0)
]

def rotate(shape):
    return [ [ shape[y][x] for y in range(len(shape)) ][::-1] for x in range(len(shape[0])) ]

class Tetromino:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color

    def image(self):
        return self.shape

    def rotate(self):
        self.shape = rotate(self.shape)

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= COLS or y + off_y >= ROWS:
                    return True
                if y + off_y >= 0 and board[y + off_y][x + off_x]:
                    return True
    return False

def remove_row(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0 for _ in range(COLS)])
    return new_board, lines_cleared

def join_matrix(board, shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell and 0 <= y + off_y < ROWS and 0 <= x + off_x < COLS:
                board[y + off_y][x + off_x] = color

def new_tetromino():
    idx = random.randint(0, len(SHAPES) - 1)
    shape = SHAPES[idx]
    color = COLORS[idx]
    return Tetromino(COLS // 2 - len(shape[0]) // 2, 0, shape, color)

def draw_buttons(screen, width, height, cell_size, replay=False, pause=False):
    button_h = 50
    button_y = height - button_h
    button_count = 4 + int(replay) + int(pause)
    button_w = min(width // button_count, 120)  # Limit max width for better text fit
    total_buttons_width = button_w * button_count
    start_x = (width - total_buttons_width) // 2

    colors = [(200,200,200)]*button_count
    labels = ["LEFT", "ROTATE", "RIGHT", "DOWN"]
    if pause:
        labels.append("PAUSE")
    if replay:
        labels.append("REPLAY")
    font_size = min(24, button_w // 4)
    font = pygame.font.SysFont('Arial', font_size, bold=True)
    rects = []
    for i in range(len(labels)):
        rect = pygame.Rect(start_x + i*button_w, button_y, button_w, button_h)
        pygame.draw.rect(screen, colors[i], rect)
        pygame.draw.rect(screen, (100,100,100), rect, 2)
        # Shrink text if needed
        label = labels[i]
        label_surface = font.render(label, True, (0,0,0))
        while label_surface.get_width() > button_w - 10 and font_size > 10:
            font_size -= 1
            font = pygame.font.SysFont('Arial', font_size, bold=True)
            label_surface = font.render(label, True, (0,0,0))
        label_rect = label_surface.get_rect(center=rect.center)
        screen.blit(label_surface, label_rect)
        rects.append(rect)
    return rects

def save_score(name, score):
    try:
        with open("tetris_scores.txt", "a") as f:
            f.write(f"{name.upper()} {score}\n")
    except Exception as e:
        print(f"Could not save score: {e}")

def get_high_score():
    if not os.path.exists("tetris_scores.txt"):
        return 0
    try:
        with open("tetris_scores.txt", "r") as f:
            scores = [int(line.strip()) for line in f if line.strip().isdigit()]
        return max(scores) if scores else 0
    except Exception as e:
        print(f"Could not read scores: {e}")
        return 0

def get_high_scores(top_n=3):
    if not os.path.exists("tetris_scores.txt"):
        return []
    try:
        with open("tetris_scores.txt", "r") as f:
            entries = []
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2 and parts[1].isdigit():
                    entries.append((parts[0], int(parts[1])))
            entries.sort(key=lambda x: x[1], reverse=True)
            return entries[:top_n]
    except Exception as e:
        print(f"Could not read scores: {e}")
        return []

def get_username(screen, width, height):
    font = pygame.font.SysFont('Arial', 36)
    name = ""
    active = True
    while active:
        screen.fill((0,0,0))
        prompt = font.render("Enter your 3-letter name:", True, (255,255,255))
        name_disp = font.render(name, True, (255,255,0))
        # Center both prompt and name on the whole screen
        prompt_y = screen.get_height() // 2 - prompt.get_height() - 10
        name_y = screen.get_height() // 2 + 10
        screen.blit(prompt, (screen.get_width() // 2 - prompt.get_width() // 2, prompt_y))
        screen.blit(name_disp, (screen.get_width() // 2 - name_disp.get_width() // 2, name_y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) == 3:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 3 and event.unicode.isalpha():
                    name += event.unicode.upper()
        pygame.time.wait(50)
    return name

def game_loop(screen, clock, cell_size, width, height):
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    current = new_tetromino()
    fall_time = 0
    fall_speed = 0.5
    score = 0

    running = True
    mouse_held = False
    held_button_idx = None
    move_delay = 100  # ms between moves when holding
    last_move_time = pygame.time.get_ticks()
    paused = False

    while running:
        screen.fill((0, 0, 0))
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

        # Draw touch buttons (with pause, but NOT replay)
        button_rects = draw_buttons(screen, screen.get_width(), screen.get_height(), cell_size, pause=True, replay=False)

        # Pause logic
        if paused:
            font = pygame.font.SysFont('Arial', 48)
            pause_text = font.render("Paused", True, (255, 255, 0))
            # Center on the whole screen, not just the grid
            screen.blit(
                pause_text,
                (
                    screen.get_width() // 2 - pause_text.get_width() // 2,
                    screen.get_height() // 2 - pause_text.get_height() // 2
                )
            )
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return score, False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if button_rects[-1].collidepoint(mx, my):
                        paused = False
            pygame.time.wait(100)
            continue

        # Move down
        if fall_time / 1000 > fall_speed:
            current.y += 1
            if check_collision(board, current.image(), (current.x, current.y)):
                current.y -= 1
                join_matrix(board, current.image(), (current.x, current.y), current.color)
                board, lines = remove_row(board)
                score += lines * 100
                current = new_tetromino()
                if check_collision(board, current.image(), (current.x, current.y)):
                    running = False  # Game over
            fall_time = 0

        offset_x = (screen.get_width() - width) // 2
        offset_y = (screen.get_height() - 50 - height) // 2

        # Draw board
        for y in range(ROWS):
            for x in range(COLS):
                color = board[y][x]
                if color:
                    pygame.draw.rect(
                        screen, color,
                        (offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size)
                    )
        # Draw current tetromino
        for y, row in enumerate(current.image()):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        current.color,
                        (offset_x + (current.x + x) * cell_size, offset_y + (current.y + y) * cell_size, cell_size, cell_size)
                    )
        # Draw grid
        for x in range(COLS):
            pygame.draw.line(screen, (40, 40, 40),
                             (offset_x + x * cell_size, offset_y),
                             (offset_x + x * cell_size, offset_y + height))
        for y in range(ROWS):
            pygame.draw.line(screen, (40, 40, 40),
                             (offset_x, offset_y + y * cell_size),
                             (offset_x + width, offset_y + y * cell_size))

        # Draw score
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        score_rect = score_text.get_rect(center=(screen.get_width() // 2, 20))
        screen.blit(score_text, score_rect)

        pygame.display.flip()

        # --- Continuous KEYBOARD movement ---
        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if keys[pygame.K_LEFT] and now - last_move_time > move_delay:
            current.x -= 1
            if check_collision(board, current.image(), (current.x, current.y)):
                current.x += 1
            last_move_time = now
        elif keys[pygame.K_RIGHT] and now - last_move_time > move_delay:
            current.x += 1
            if check_collision(board, current.image(), (current.x, current.y)):
                current.x -= 1
            last_move_time = now
        elif keys[pygame.K_DOWN] and now - last_move_time > move_delay:
            current.y += 1
            if check_collision(board, current.image(), (current.x, current.y)):
                current.y -= 1
            last_move_time = now

        # --- Continuous MOUSE movement for touch buttons ---
        if mouse_held and held_button_idx is not None and now - last_move_time > move_delay:
            if held_button_idx == 0:  # LEFT
                current.x -= 1
                if check_collision(board, current.image(), (current.x, current.y)):
                    current.x += 1
            elif held_button_idx == 1:  # ROTATE
                old_shape = current.shape
                current.rotate()
                if check_collision(board, current.image(), (current.x, current.y)):
                    current.shape = old_shape
            elif held_button_idx == 2:  # RIGHT
                current.x += 1
                if check_collision(board, current.image(), (current.x, current.y)):
                    current.x -= 1
            elif held_button_idx == 3:  # DOWN
                current.y += 1
                if check_collision(board, current.image(), (current.x, current.y)):
                    current.y -= 1
            elif held_button_idx == 4:  # PAUSE
                paused = True
            last_move_time = now

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, False
            elif event.type == pygame.ACTIVEEVENT:
                if event.state & 2:  # 2 = focus state
                    if event.gain == 0:
                        paused = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    old_shape = current.shape
                    current.rotate()
                    if check_collision(board, current.image(), (current.x, current.y)):
                        current.shape = old_shape
                    last_move_time = pygame.time.get_ticks()
                elif event.key == pygame.K_p:
                    paused = True
                elif event.key == pygame.K_f:
                    # Toggle fullscreen
                    is_fullscreen = screen.get_flags() & pygame.FULLSCREEN
                    if is_fullscreen:
                        # Windowed mode
                        screen_width, screen_height = get_screen_size(False)
                        cell_size, width, height = recalc_sizes(screen_width, screen_height)
                        screen = pygame.display.set_mode((width, height + 50))
                    else:
                        # Fullscreen mode
                        screen_width, screen_height = get_screen_size(True)
                        cell_size, width, height = recalc_sizes(screen_width, screen_height)
                        screen = pygame.display.set_mode((width, height + 50), pygame.FULLSCREEN)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mx, my):
                        held_button_idx = i
                        mouse_held = True
                        last_move_time = pygame.time.get_ticks() - move_delay  # move instantly
                        if i == 4:  # PAUSE
                            paused = True
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
                held_button_idx = None

    return score, True

def main():
    pygame.init()
    fullscreen = False
    screen_width, screen_height = get_screen_size(fullscreen)
    cell_size, width, height = recalc_sizes(screen_width, screen_height)
    screen = pygame.display.set_mode((width, height + 50))  # Default windowed
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    while True:
        score, game_over = game_loop(screen, clock, cell_size, width, height)
        if not game_over:
            break  # User closed window

        # Prompt for username
        name = get_username(screen, width, height)
        save_score(name, score)

        high_scores = get_high_scores(3)

        # Game Over screen
        font = pygame.font.SysFont('Arial', 48)
        over_text = font.render("Game Over!", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.fill((0,0,0))
        screen.blit(over_text, (screen.get_width()//2 - over_text.get_width()//2, screen.get_height()//2 - 110))
        screen.blit(score_text, (screen.get_width()//2 - score_text.get_width()//2, screen.get_height()//2 - 50))

        # Draw top 3 high scores with names
        small_font = pygame.font.SysFont('Arial', 32)
        for i, (uname, hs) in enumerate(high_scores):
            hs_text = small_font.render(f"{i+1}. {uname}: {hs}", True, (255,255,0))
            screen.blit(hs_text, (screen.get_width()//2 - hs_text.get_width()//2, screen.get_height()//2 + 10 + i*40))
        button_rects = draw_buttons(screen, width, height + 50, cell_size, replay=True)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        fullscreen = not fullscreen
                        screen_width, screen_height = get_screen_size(fullscreen)
                        cell_size, width, height = recalc_sizes(screen_width, screen_height)
                        if fullscreen:
                            screen = pygame.display.set_mode((width, height + 50), pygame.FULLSCREEN)
                        else:
                            screen = pygame.display.set_mode((width, height + 50))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if len(button_rects) == 5 and button_rects[4].collidepoint(mx, my):
                        waiting = False  # Replay
            pygame.time.wait(50)

    pygame.quit()
    print("Game Over! Your score:", score)

if __name__ == "__main__":
    main()