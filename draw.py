from turtle import RawTurtle, Screen

def rotate_right(dx, dy):
    return dy, -dx

def rotate_left(dx, dy):
    return -dy, dx

def draw_maze(maze, scale, *, screen = None, tracer = False, delay = 0, speed = 0, updates = False, start_x = 0, start_y = 0):
    if screen is None:
        screen = Screen()

    width = scale * maze.width
    height = scale * maze.height

    original_tracer = screen.tracer()
    original_delay = screen.delay()

    screen.tracer(tracer)
    screen.delay(delay)

    turtle = RawTurtle(screen, visible=False)
    turtle.speed(speed)
    turtle.setpos(start_x, start_y)
    turtle.setheading(0)
    turtle.showturtle()

    x, y, dx, dy = 0, 0, 1, 0

    while True:
        sx, sy = rotate_right(dx, dy)

        print(x, y, maze[x, y])

        if maze[x, y][sx, sy]:
            if maze[x, y][rotate_left(sx, sy)]:
                print('a')
                turtle.forward(scale - 1)
                turtle.left(90)
                dx, dy = rotate_left(dx, dy)
            else:
                print('b')
                turtle.forward(scale)
                x, y = x + dx, y + dy
        else:
            print('c')
            turtle.right(90)
            turtle.forward(1)
            dx, dy = rotate_right(dx, dy)
            x, y = x + dx, y + dy

        if (x, y, dx, dy) == (0, 0, 1, 0):
            break

    screen.tracer(original_tracer)
    screen.delay(original_delay)
    screen.update()

    return screen
