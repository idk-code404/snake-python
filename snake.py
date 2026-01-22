import random
import curses

def main(stdscr):
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Refresh every 100ms
    
    # Initialize colors (with fallback)
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)   # Snake
        curses.init_pair(2, curses.COLOR_RED, -1)     # Food
        curses.init_pair(3, curses.COLOR_YELLOW, -1)  # Border/Text
        curses.init_pair(4, curses.COLOR_WHITE, -1)   # Score
        colors_available = True
    except:
        colors_available = False
    
    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    
    # Check minimum size
    if sh < 10 or sw < 20:
        stdscr.clear()
        stdscr.addstr(sh//2, (sw-25)//2, "Terminal too small!")
        stdscr.refresh()
        stdscr.getch()
        return
    
    # Leave margin for border and score
    game_h, game_w = sh - 2, sw - 2
    
    # Create game window with border
    win = curses.newwin(game_h, game_w, 1, 1)
    win.keypad(1)
    
    # Initial snake position (center)
    snake = [
        [game_h//2, game_w//2],
        [game_h//2, game_w//2-1],
        [game_h//2, game_w//2-2]
    ]
    
    # Initial food position
    food = [game_h//4, game_w//2]
    
    # Initial direction (moving right)
    key = curses.KEY_RIGHT
    prev_key = key
    
    # Draw static border once
    win.border(0)
    
    # Initial draw of food
    food_attr = curses.color_pair(2) | curses.A_BOLD if colors_available else curses.A_BOLD
    win.addch(food[0], food[1], '*', food_attr)
    
    # Game loop
    while True:
        # Clear previous score area
        win.addstr(0, 2, " " * (game_w - 4))
        
        # Display score at top
        score_text = f" Score: {len(snake) - 3} "
        score_attr = curses.color_pair(4) | curses.A_BOLD if colors_available else curses.A_BOLD
        win.addstr(0, (game_w - len(score_text)) // 2, score_text, score_attr)
        
        # Get user input
        next_key = win.getch()
        key = key if next_key == -1 else next_key
        
        # Prevent reversing into self
        if (key == curses.KEY_DOWN and prev_key != curses.KEY_UP) or \
           (key == curses.KEY_UP and prev_key != curses.KEY_DOWN) or \
           (key == curses.KEY_RIGHT and prev_key != curses.KEY_LEFT) or \
           (key == curses.KEY_LEFT and prev_key != curses.KEY_RIGHT):
            prev_key = key
        
        # Calculate new head position
        head = snake[0].copy()
        
        if prev_key == curses.KEY_DOWN:
            head[0] += 1
        elif prev_key == curses.KEY_UP:
            head[0] -= 1
        elif prev_key == curses.KEY_RIGHT:
            head[1] += 1
        elif prev_key == curses.KEY_LEFT:
            head[1] -= 1
        
        # Insert new head
        snake.insert(0, head)
        
        # Check for collision with food
        if head == food:
            # Generate new food position
            while True:
                food = [random.randint(1, game_h-2), random.randint(1, game_w-2)]
                if food not in snake:
                    break
            # Draw new food
            win.addch(food[0], food[1], '*', food_attr)
        else:
            # Remove tail if no food eaten
            tail = snake.pop()
            # Clear old tail position
            win.addch(tail[0], tail[1], ' ')
        
        # Game over conditions
        if (head[0] in [0, game_h-1] or 
            head[1] in [0, game_w-1] or 
            head in snake[1:]):
            break
        
        # Draw snake head only (body already drawn)
        head_attr = curses.color_pair(1) | curses.A_BOLD if colors_available else curses.A_BOLD
        if prev_key == curses.KEY_DOWN:
            win.addch(head[0], head[1], 'v', head_attr)
        elif prev_key == curses.KEY_UP:
            win.addch(head[0], head[1], '^', head_attr)
        elif prev_key == curses.KEY_RIGHT:
            win.addch(head[0], head[1], '>', head_attr)
        else:
            win.addch(head[0], head[1], '<', head_attr)
        
        # Draw snake body segments (only needed for segments beyond the first)
        body_attr = curses.color_pair(1) if colors_available else curses.A_NORMAL
        for segment in snake[1:-1]:  # Skip head and tail
            win.addch(segment[0], segment[1], 'o', body_attr)
        
        # Refresh window (only once per frame)
        win.refresh()
    
    # Game over screen
    stdscr.clear()
    stdscr.nodelay(0)  # Wait for input
    
    game_over_text = " GAME OVER! "
    score_text = f"Final Score: {len(snake) - 3} "
    instruction_text = "Press any key to exit... "
    
    go_attr = curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE if colors_available else curses.A_BOLD | curses.A_REVERSE
    stdscr.addstr(sh//2 - 1, (sw - len(game_over_text)) // 2, game_over_text, go_attr)
    
    score_attr = curses.color_pair(4) | curses.A_BOLD if colors_available else curses.A_BOLD
    stdscr.addstr(sh//2, (sw - len(score_text)) // 2, score_text, score_attr)
    
    instr_attr = curses.color_pair(3) if colors_available else curses.A_NORMAL
    stdscr.addstr(sh//2 + 2, (sw - len(instruction_text)) // 2, instruction_text, instr_attr)
    
    stdscr.refresh()
    stdscr.getch()

# Run the game
curses.wrapper(main)
