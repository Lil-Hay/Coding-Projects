import pygame
import random

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

def draw_buttons(screen, width, height, cell_size, replay=False):
    button_h = 50
    button_y = height - button_h
    button_w = width // (5 if replay else 4)
    colors = [(200,200,200)]*(5 if replay else 4)
    labels = ["LEFT", "ROTATE", "RIGHT", "DOWN"]
    if replay:
        labels.append("REPLAY")
    font = pygame.font.SysFont('Arial', 20)
    rects = []
    for i in range(len(labels)):
        rect = pygame.Rect(i*button_w, button_y, button_w, button_h)
        pygame.draw.rect(screen, colors[i], rect)
        pygame.draw.rect(screen, (100,100,100), rect, 2)
        label = font.render(labels[i], True, (0,0,0))
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        rects.append(rect)
    return rects

def game_loop(screen, clock):
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

    while running:
        screen.fill((0, 0, 0))
        fall_time += clock.get_rawtime()
        clock.tick(FPS)

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

        # Draw board
        for y in range(ROWS):
            for x in range(COLS):
                color = board[y][x]
                if color:
                    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Draw current tetromino
        for y, row in enumerate(current.image()):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(
                        screen,
                        current.color,
                        ((current.x + x) * CELL_SIZE, (current.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                    )
        # Draw grid
        for x in range(COLS):
            pygame.draw.line(screen, (40, 40, 40), (x * CELL_SIZE, 0), (x * CELL_SIZE, HEIGHT))
        for y in range(ROWS):
            pygame.draw.line(screen, (40, 40, 40), (0, y * CELL_SIZE), (WIDTH, y * CELL_SIZE))

        # Draw score
        font = pygame.font.SysFont('Arial', 24)
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.blit(score_text, (5, 5))

        # Draw touch buttons
        button_rects = draw_buttons(screen, WIDTH, HEIGHT + 50, CELL_SIZE)

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
            last_move_time = now

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    old_shape = current.shape
                    current.rotate()
                    if check_collision(board, current.image(), (current.x, current.y)):
                        current.shape = old_shape
                    last_move_time = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mx, my):
                        held_button_idx = i
                        mouse_held = True
                        last_move_time = pygame.time.get_ticks() - move_delay  # move instantly
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
                held_button_idx = None

    return score, True

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 50))  # Extra space for buttons
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    while True:
        score, game_over = game_loop(screen, clock)
        if not game_over:
            break  # User closed window

        # Game Over screen
        font = pygame.font.SysFont('Arial', 48)
        over_text = font.render("Game Over!", True, (255, 0, 0))
        score_text = font.render(f"Score: {score}", True, (255,255,255))
        screen.fill((0,0,0))
        screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        button_rects = draw_buttons(screen, WIDTH, HEIGHT + 50, CELL_SIZE, replay=True)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    if len(button_rects) == 5 and button_rects[4].collidepoint(mx, my):
                        waiting = False  # Replay
            pygame.time.wait(50)

    pygame.quit()
    print("Game Over! Your score:", score)

if __name__ == "__main__":
    main()