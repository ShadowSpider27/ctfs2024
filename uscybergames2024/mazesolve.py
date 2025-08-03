from collections import deque

def text_to_maze(text_maze):
    return [[1 if char == '█' else 0 for char in line] for line in text_maze.strip().split('\n')]

def print_maze(maze, path=None):
    maze_copy = [row[:] for row in maze]
    if path:
        for (r, c) in path:
            maze_copy[r][c] = '*'
    for row in maze_copy:
        print(' '.join(str(cell) if cell != 1 else '█' for cell in row))
    print()

def find_start_end(maze):
    start = None
    end = None

    # Find start (first empty space in the first row)
    for col, cell in enumerate(maze[0]):
        if cell == 0:
            start = (0, col)
            break

    # Find end (only empty space in the last row)
    for col, cell in enumerate(maze[-1]):
        if cell == 0:
            end = (len(maze) - 1, col)
            break

    return start, end

def solve_maze_debug(maze, start, end):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    rows, cols = len(maze), len(maze[0])
    queue = deque([(start[0], start[1], [])])  # (row, col, path)
    visited = set()

    while queue:
        r, c, path = queue.popleft()
        
        if (r, c) == end:
            return path + [(r, c)]
        
        if (r, c) in visited:
            continue
        
        visited.add((r, c))
        
        # Debug: Print the current position and path
        #print(f"Visiting: ({r}, {c}), Path length: {len(path) + 1}")
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                queue.append((nr, nc, path + [(r, c)]))
    
    return "No path found."

def print_solution(solution, maze):
    if solution != "No path found.":
        # Flip coordinates before printing
        flipped_solution = [(col, row) for row, col in solution]
        print("Solution Path:")
        print(','.join([f"({r},{c})" for r, c in flipped_solution]))
        print()
        #print_maze(maze, solution)
    else:
        print(solution)


# Text-based maze input
def maze(text_maze):

    # Convert the text maze to a 2D list
    maze = text_to_maze(text_maze)

    # Find the start and end points based on the criteria
    start, end = find_start_end(maze)

    print("Maze:")
    #print_maze(maze)
    print(f"Start: {start}, End: {end}")

    solution = solve_maze_debug(maze, start, end)

    print_solution(solution, maze)

if __name__ == "__main__":
    text_maze = """
████████ ████████████████████████████████████████
█ █             █     █         █   █           █
█ ███████████ █ ███ █ █ █ █████ █ █ █ █ ███████ █
█         █   █     █ █ █ █     █ █   █     █   █
█████████ █ █████████ ███ █ █████ █████████ █ ███
█   █   █ █     █   █ █   █ █   █ █       █ █   █
█ █ █ █ █ █████ ███ █ █ ███ █ ███ ███ ███ █ ███ █
█ █ █ █   █   █ █   █   █   █   █ █   █ █ █ █   █
█ ███ █████ █ █ █ ███████ ███ █ █ █ ███ █ █ █ ███
█   █ █     █ █ █       █   █ █   █   █   █ █   █
███ █ █ █ ███ █ ███ ███████ █ █████ █ █ ███ █████
█   █ █ █   █   █   █       █     █ █ █   █ █   █
█ ███ █████ █████ █ █ ███████████ █ █ █████ █ █ █
█     █     █     █ █   █   █     █ █ █     █ █ █
█ █████ ███████ ███ ███ █ ███ ███████ █ █████ █ █
█   █   █       █     █ █   █         █       █ █
███ ███ █ █ ███ ███████ █ █ ███████ ███████ ███ █
█ █ █   █ █ █   █   █   █ █     █   █     █ █   █
█ █ █ ███ █ █████ █ █ █████████ █ ███ ███ █ █ ███
█ █   █   █       █ █ █   █   █   █   █ █ █ █   █
█ █████ ███████████ █ █ █ █ █ █████ ███ █ █ ███ █
█   █   █     █   █ █ █ █ █ █       █ █   █ █   █
█ ███ █████ █ █ █ █ █ █ █ █ █████████ █ ███ █ ███
█     █     █   █ █ █   █   █ █   █   █ █   █   █
█ █████ ███████ ███ █████████ █ █ █ █ █ ███████ █
█   █         █ █       █     █ █   █ █   █   █ █
███ █████████ █ █ ███████ ███ █ █████ ███ █ █ █ █
█             █ █           █       █       █   █
█████████████████████████ ███████████████████████
    """
    maze(text_maze)