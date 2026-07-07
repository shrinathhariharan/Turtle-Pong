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

    def bounce_y(self): # bounces from the top or bottom wall
        self.setheading(360 - self.heading())

    def bounce_x(self, x_position): # bounces from the player or cpu paddle
        self.setheading(180 - self.heading() + random.randint(-30, 30))
        self.setx(x_position)

    def adjust_angle(self): # prevents vertical-like ball movement
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
        if self.ycor() < screenHeight - 25:
            self.sety(self.ycor() + amount)

    def move_down(self, amount):
        if self.ycor() > -screenHeight + 25:
            self.sety(self.ycor() - amount)

    def reset(self, x_position):
        self.goto(x_position, 0)


# ---SETUP---
gameState = "menu"  # menu, playing, or gameOver

screenWidth = 500
screenHeight = 300
ballSpeed = 4  # starting ball speed
speedIncrease = 0.75  # standard amount the ball's speed increases by
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
boundry.pencolor("orange")  # boundary color

paddleSpeed = 15  # how fast the player and cpu move

player = Paddle(-screenWidth + 20, "blue")
cpu = Paddle(screenWidth - 20, "red")

score = 0
scoreBoard = turtle.Turtle()
scoreBoard.hideturtle()
scoreBoard.penup()
scoreBoard.goto(-screenWidth - 50, screenHeight + 40)  # goes outside the boundry (top left)
scoreBoard.color("white")
scoreBoard.write(f"Score: {score}", align="center", font=("Courier", 30, "bold"))  # retro bold font

menuText = [
    ["TURTLE PONG", "W / Up to Move Up"],
    ["S / Down Arrow to Move Down", "Click anywhere to Start!"],
    ["Leaderboard only tracks HARD mode scores", ""]
]

yPositions = [120, 40, -40]

# ---FUNCTIONS---

def chooseDifficulty():
    global ballSpeed
    global speedIncrease
    global difficulty

    choice = turtle.numinput("Select Difficulty", "Enter a number:\n(1 is easy, 2 is medium, 3 is hard)", 2, 1, 3) #asks for difficulty

    if choice is None:
        choice = 2 #default sets to medium if not entered

    if choice == 1:
        ballSpeed = 4
        speedIncrease = 0.4
        difficulty = "easy"
    elif choice == 2:
        ballSpeed = 5
        speedIncrease = 0.75
        difficulty = "medium"
    elif choice == 3:
        ballSpeed = 6
        speedIncrease = 1.1
        difficulty = "hard"

def showInstructions():
    scoreBoard.clear()
    scoreBoard.goto(0, 100)
    player.hideturtle()
    cpu.hideturtle()
    ball.hideturtle()

    for row in range(len(menuText)):
        for col in range(len(menuText[row])): # gets index of text and position
            text = menuText[row][col]

            scoreBoard.goto(0, yPositions[row] - col * 40) # gets the y position of the text
            scoreBoard.write(text, align="center", font=("Courier", 20, "normal")) # writes the text

def setBoundaries():
    boundry.clear()
    boundry.penup()
    boundry.goto(0, screenHeight)
    while boundry.ycor() > -screenHeight:  # creates dashed lines for the boundary
        boundry.sety(boundry.ycor() - 10)
        boundry.penup()
        boundry.sety(boundry.ycor() - 10)
        boundry.pendown()

    boundry.penup()
    boundry.goto(-screenWidth - 10, screenHeight)

    boundry.pendown()
    boundry.goto(screenWidth + 10, screenHeight)
    boundry.goto(screenWidth + 10, -screenHeight)
    boundry.goto(-screenWidth - 10, -screenHeight)
    boundry.goto(-screenWidth - 10, screenHeight)

def startGame():
    global gameState

    if gameState != "menu":
        return

    chooseDifficulty()

    scoreBoard.clear()
    setBoundaries()

    ball.reset()  # randomizes the direction (player or cpu)
    ball.showturtle()
    cpu.showturtle()
    player.showturtle()

    gameState = "playing"  # makes the game state to playing so playing functions run

    updateScore(False)  # writes the score but doesn't add a point

    # starts the ball and computer movement
    moveBall()
    moveComputer()


def playAgain():
    global score
    global ballSpeed
    global gameState

    score = 0
    ballSpeed = 4  # resets ball speed
    gameState = "menu"  # makes state menu so moveBall() and moveComputer() stop

    ball.reset()
    player.showturtle()
    cpu.showturtle()
    player.reset(-screenWidth + 20)
    cpu.reset(screenWidth - 20)

    updateScore(False)  # shows score but doesn't update score

    showInstructions()

def updateScore(addScore):
    global score

    if addScore:
        score += 1
    scoreBoard.clear()  # shows the score in the correct position
    scoreBoard.goto(-screenWidth - 50, screenHeight + 40)
    scoreBoard.write(f"Score: {score} | {difficulty.upper()} MODE", align="center", font=("Courier", 30, "bold"))

def gameOver():
    global gameState
    gameState = "gameOver"

    # hides paddles
    player.hideturtle()
    cpu.hideturtle()

    scoreBoard.clear()
    scoreBoard.goto(0, screenHeight - 50)

    scoreBoard.write("Game Over!", align="center", font=("Courier", 30, "normal"))
    scoreBoard.sety(scoreBoard.ycor() - 50)
    scoreBoard.write(f"Your score was {score}", align="center", font=("Courier", 30, "normal"))

    highScores = []
    try:
        with open("highscore.txt", 'r') as f:  # opens the highscore file
            for line in f:
                highScores.append(int(line.strip()))  # adds it to a list to be sorted (because every line is a number)
    except FileNotFoundError:
        print("LOG: Could not load save file\n")
        highScores = []  # empty list without saving the score

    if score > 0 and difficulty == "hard": # scores contribute to the leaderboard only in hard mode
        highScores.append(score)
    highScores.sort(reverse=True)  # sorts the list from highest to lowest
    highScores = highScores[:5]  # makes the list only five places long to show top five

    scoreBoard.sety(scoreBoard.ycor() - 50)
    scoreBoard.write("These are your highest scores:", align="center", font=("Courier", 20, "normal"))
    scoreBoard.sety(scoreBoard.ycor() - 60)
    for i in range(len(highScores)):
        scoreBoard.write(f"{i + 1}. {highScores[i]}", align="center",
                         font=("Courier", 18, "normal"))  # writes the position with the score
        scoreBoard.sety(scoreBoard.ycor() - 40)

    try:
        with open("highscore.txt", 'w') as f:
            for highScore in highScores:
                f.write(str(highScore) + '\n')  # writes the scores (highscore list has top five scores)
        scoreBoard.write("Click 'r' to Play Again!", align="center", font=("Courier", 20, "normal"))
    except FileNotFoundError:
        print("LOG: Could not write in save file\n")

def moveBall():
    global ballSpeed
    global score

    if gameState != "playing":
        return

    window.update()
    ball.move(ballSpeed)  # ball speed is increased over time for difficulty

    if ball.ycor() > screenHeight - 10 or ball.ycor() < -screenHeight + 10:
        ball.bounce_y()  # if the ball touches a top wall
    if ball.xcor() < -screenWidth + 40 and ball.distance(player) < 50:  # if the ball touches the player
        ball.bounce_x(-screenWidth + 41)  # move the ball the opposite direction with a random offset
        updateScore(True)

        if ballSpeed < 15:  # makes sure the ball speed is less than 15 (this is too fast)
            ballSpeed += speedIncrease  # increases by difficulty amount
    if ball.xcor() > screenWidth - 40 and ball.distance(cpu) < 50:  # if the ball touches the computer
        ball.bounce_x(screenWidth - 41)  # same logic as player collision
        ball.adjust_angle()  # makes sure the ball does not go almost straight up
    if ball.xcor() < -screenWidth:
        gameOver()  # game over if the ball has passed the width boundary
        return  # stops the ontimer call so the function ends

    window.ontimer(moveBall, 15)  # repeatedly calls the function every 15 milliseconds until stopped

def moveUp():
    if gameState == "playing":
        player.move_up(paddleSpeed)  # moves up if the game is running and player isn't touching the top

def moveDown():
    if gameState == "playing":
        player.move_down(paddleSpeed)  # moves down if the game is running and player isn't touching bottom

def moveComputer():
    if gameState == "playing":
        if abs(cpu.ycor() - ball.ycor()) > random.randint(5, 20):  # randomized computer movement
            if cpu.ycor() < ball.ycor() and cpu.ycor() < screenHeight - 25:
                cpu.move_up(paddleSpeed)  # goes up if the ball is above the computer and less than the screen height (safety check)
            elif cpu.ycor() > ball.ycor() and cpu.ycor() > -screenHeight + 25:
                cpu.move_down(paddleSpeed)  # same for going down

    window.ontimer(moveComputer, 15)  # does this at same rate as moveBall()

def onClick(x, y):
    window.listen()
    startGame()

# ---MAIN LOOP---
window.title("Turtle Pong")

window.listen()
window.onkey(moveUp, "Up")  # toggle keys
window.onkey(moveDown, "Down")
window.onkey(moveUp, 'w')
window.onkey(moveDown, 's')

window.onkey(playAgain, 'r')
window.onclick(onClick)

showInstructions()
window.mainloop() # continuously runs the program
