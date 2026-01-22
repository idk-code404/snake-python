import random
import curses

def main(stdscr):
    # Initialize curses settings
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Refresh every 100ms
    
    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    
    # Game window
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    
    # Initial snake position (center)
    snake = [
        [sh//2, sw//2],
        [sh//2, sw//2-1],
        [sh//2, sw//2-2]
    ]
    
    # Initial food position
    food = [sh//4, sw//2]
    
    # Initial direction (moving right)
    key = curses.KEY_RIGHT
    
    # Game loop
    while True:
        # Display score and instructions
        win.addstr(0, 2, f'Score: {len(snake) - 3}')
        win.addstr(0, sw//2 - 10, 'Use arrow keys to move')
        
        # Draw food
        win.addch(food[0], food[1], '#')
        
        # Get user input
        next_key = win.getch()
        key = key if next_key == -1 else next_key
        
        # Calculate new head position
        head = snake[0].copy()
        
        if key == curses.KEY_DOWN:
            head[0] += 1
        elif key == curses.KEY_UP:
            head[0] -= 1
        elif key == curses.KEY_RIGHT:
            head[1] += 1
        elif key == curses.KEY_LEFT:
            head[1] -= 1
        
        # Insert new head
        snake.insert(0, head)
        
        # Check for collision with food
        if head == food:
            # Generate new food position
            while True:
                food = [random.randint(1, sh-2), random.randint(1, sw-2)]
                if food not in snake:
                    break
        else:
            # Remove tail if no food eaten
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')
        
        # Game over conditions
        if (head[0] in [0, sh-1] or 
            head[1] in [0, sw-1] or 
            head in snake[1:]):
            break
        
        # Draw snake
        win.addch(head[0], head[1], '*')
    
    # Game over screen
    win.clear()
    win.addstr(sh//2, sw//2 - 5, f'GAME OVER! Score: {len(snake) - 3}')
    win.addstr(sh//2 + 1, sw//2 - 10, 'Press any key to exit...')
    win.refresh()
    win.timeout(-1)  # Wait for input
    win.getch()

# Run the game
curses.wrapper(main)