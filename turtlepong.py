import turtle
import random


class Ball(turtle.Turtle):
    def __init__(self, color):
        super().__init__()
        self.speed(0)
        self.shape("circle")
        self.color(color)
        self.penup()

    def move(self, speed):
        self.forward(speed)

    def reset(self):
        self.goto(0, 0)
        self.setheading(random.choice([0, 180]))

    def bounce_y(self):
        self.setheading(360 - self.heading())

    def bounce_x(self, x_position):  # bounces from the player or cpu paddle
        self.setheading(180 - self.heading() + random.randint(-30, 30))
        self.setx(x_position)

    def adjust_angle(self):  # prevents vertical-like ball movement
        angle = self.heading()
        if 0 < angle < 20:
            self.setheading(20)
        elif 160 < angle < 180:
            self.setheading(160)
        elif 180 < angle < 200:
            self.setheading(200)
        elif 340 < angle < 360:
            self.setheading(340)


class Paddle(turtle.Turtle):
    def __init__(self, x_position, color):
        super().__init__()
        self.penup()
        self.speed(0)
        self.color(color)
        self.shape("square")
        self.shapesize(stretch_wid=3, stretch_len=0.25)
        self.goto(x_position, 0)

    def move_up(self, amount):
        if self.ycor() < screen_height - 25:
            self.sety(self.ycor() + amount)

    def move_down(self, amount):
        if self.ycor() > -screen_height + 25:
            self.sety(self.ycor() - amount)

    def reset(self, x_position):
        self.goto(x_position, 0)


# ---SETUP---
game_state = "menu"

screen_width = 500
screen_height = 300
ball_speed = 4
speed_increase = 0.75
difficulty = "medium"

window = turtle.Screen()
window.bgcolor("black")
window.tracer(0)  # for smooth movement

turtle.colormode(255)

ball = Ball((57, 255, 0))
ball.reset()

boundry = turtle.Turtle()
boundry.hideturtle()
boundry.speed(0)
boundry.pencolor("orange")

paddle_speed = 15

player = Paddle(-screen_width + 20, "blue")
cpu = Paddle(screen_width - 20, "red")

score = 0
score_board = turtle.Turtle()
score_board.hideturtle()
score_board.penup()
score_board.goto(-screen_width - 50, screen_height + 40)  # goes outside the boundry (top left)
score_board.color("white")
score_board.write(f"Score: {score}", align="center", font=("Courier", 30, "bold"))

menu_text = [
    ["TURTLE PONG", "W / Up to Move Up"],
    ["S / Down Arrow to Move Down", "Click anywhere to Start!"],
    ["Leaderboard only tracks HARD mode scores", ""]
]

y_positions = [120, 40, -40]


def choose_difficulty():
    global ball_speed
    global speed_increase
    global difficulty

    choice = turtle.numinput("Select Difficulty", "Enter a number:\n(1 is easy, 2 is medium, 3 is hard)", 2, 1, 3)

    if choice is None:
        choice = 2  # default sets to medium if not entered

    if choice == 1:
        ball_speed = 4
        speed_increase = 0.4
        difficulty = "easy"
    elif choice == 2:
        ball_speed = 5
        speed_increase = 0.75
        difficulty = "medium"
    elif choice == 3:
        ball_speed = 6
        speed_increase = 1.1
        difficulty = "hard"


def show_instructions():
    score_board.clear()
    score_board.goto(0, 100)
    player.hideturtle()
    cpu.hideturtle()
    ball.hideturtle()

    for row in range(len(menu_text)):
        for col in range(len(menu_text[row])):  # gets index of text and position
            text = menu_text[row][col]

            score_board.goto(0, y_positions[row] - col * 40)
            score_board.write(text, align="center", font=("Courier", 20, "normal"))


def set_boundaries():
    boundry.clear()
    boundry.penup()
    boundry.goto(0, screen_height)
    while boundry.ycor() > -screen_height:  # creates dashed lines for the boundary
        boundry.sety(boundry.ycor() - 10)
        boundry.penup()
        boundry.sety(boundry.ycor() - 10)
        boundry.pendown()

    boundry.penup()
    boundry.goto(-screen_width - 10, screen_height)

    boundry.pendown()
    boundry.goto(screen_width + 10, screen_height)
    boundry.goto(screen_width + 10, -screen_height)
    boundry.goto(-screen_width - 10, -screen_height)
    boundry.goto(-screen_width - 10, screen_height)


def start_game():
    global game_state

    if game_state != "menu":
        return

    choose_difficulty()

    score_board.clear()
    set_boundaries()

    ball.reset()
    ball.showturtle()
    cpu.showturtle()
    player.showturtle()

    game_state = "playing"

    update_score(False)

    move_ball()
    move_computer()


def play_again():
    global score
    global ball_speed
    global game_state

    score = 0
    ball_speed = 4
    game_state = "menu"

    ball.reset()
    player.showturtle()
    cpu.showturtle()
    player.reset(-screen_width + 20)
    cpu.reset(screen_width - 20)

    update_score(False)

    show_instructions()


def update_score(add_score):
    global score

    if add_score:
        score += 1
    score_board.clear()
    score_board.goto(-screen_width - 50, screen_height + 40)
    score_board.write(f"Score: {score} | {difficulty.upper()} MODE", align="center", font=("Courier", 30, "bold"))


def game_over():
    global game_state
    game_state = "gameOver"

    # hides paddles
    player.hideturtle()
    cpu.hideturtle()

    score_board.clear()
    score_board.goto(0, screen_height - 50)

    score_board.write("Game Over!", align="center", font=("Courier", 30, "normal"))
    score_board.sety(score_board.ycor() - 50)
    score_board.write(f"Your score was {score}", align="center", font=("Courier", 30, "normal"))

    high_scores = []
    try:
        with open("highscore.txt", 'r') as f:
            for line in f:
                high_scores.append(int(line.strip()))
    except FileNotFoundError:
        print("LOG: Could not load save file\n")
        high_scores = []

    if score > 0 and difficulty == "hard":  # scores contribute to the leaderboard only in hard mode
        high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:5]  # list only shows top five

    score_board.sety(score_board.ycor() - 50)
    score_board.write("These are your highest scores:", align="center", font=("Courier", 20, "normal"))
    score_board.sety(score_board.ycor() - 60)
    for i in range(len(high_scores)):
        score_board.write(f"{i + 1}. {high_scores[i]}", align="center",
                          font=("Courier", 18, "normal"))
        score_board.sety(score_board.ycor() - 40)

    try:
        with open("highscore.txt", 'w') as f:
            for high_score in high_scores:
                f.write(str(high_score) + '\n')
        score_board.write("Click 'r' to Play Again!", align="center", font=("Courier", 20, "normal"))
    except FileNotFoundError:
        print("LOG: Could not write in save file\n")


def move_ball():
    global ball_speed
    global score

    if game_state != "playing":
        return

    window.update()
    ball.move(ball_speed)

    if ball.ycor() > screen_height - 10 or ball.ycor() < -screen_height + 10:
        ball.bounce_y()
    if ball.xcor() < -screen_width + 40 and ball.distance(player) < 50:
        ball.bounce_x(-screen_width + 41)
        update_score(True)

        if ball_speed < 15:  # makes sure the ball speed is less than 15 (this is too fast)
            ball_speed += speed_increase  # increases by difficulty amount
    if ball.xcor() > screen_width - 40 and ball.distance(cpu) < 50:
        ball.bounce_x(screen_width - 41)
        ball.adjust_angle()  # makes sure the ball does not go almost straight up
    if ball.xcor() < -screen_width:
        game_over()
        return

    window.ontimer(move_ball, 15)  # repeatedly calls the function every 15 milliseconds until stopped


def move_up():
    if game_state == "playing":
        player.move_up(paddle_speed)


def move_down():
    if game_state == "playing":
        player.move_down(paddle_speed)


def move_computer():
    if game_state == "playing":
        if abs(cpu.ycor() - ball.ycor()) > random.randint(5, 20):
            if cpu.ycor() < ball.ycor() and cpu.ycor() < screen_height - 25:
                cpu.move_up(paddle_speed)
            elif cpu.ycor() > ball.ycor() and cpu.ycor() > -screen_height + 25:
                cpu.move_down(paddle_speed)

    window.ontimer(move_computer, 15)


def on_click(x, y):
    window.listen()
    start_game()


window.title("Turtle Pong")

window.listen()
window.onkey(move_up, "Up")
window.onkey(move_down, "Down")
window.onkey(move_up, 'w')
window.onkey(move_down, 's')

window.onkey(play_again, 'r')
window.onclick(on_click)

show_instructions()
window.mainloop()
