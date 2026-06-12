import turtle
import random

# ---SETUP---
gameState = "menu"  # menu, playing, or gameOver

screenWidth = 500
screenHeight = 300
ballSpeed = 4  # starting ball speed
speedIncrease = 0.75 #standard amount the ball's speed increases by
difficulty = "medium"

window = turtle.Screen()
window.bgcolor("black")
window.tracer(0) #for smooth movement

ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
turtle.colormode(255)
ball.color(57, 255, 0)  # green color
ball.penup()
ball.setheading(random.choice([0, 180]))  # either goes to player or cpu first

boundry = turtle.Turtle()
boundry.hideturtle()
boundry.speed(0)
boundry.pencolor("orange")  # boundary color

player = turtle.Turtle()
player.penup()
player.speed(0)
player.color("blue")
player.shape("square")
player.shapesize(stretch_wid=3, stretch_len=0.25)  # player hitbox and shape
player.goto(-screenWidth + 20, 0)

paddleSpeed = 15  # how fast the player and cpu move

cpu = turtle.Turtle()
cpu.penup()
cpu.speed(0)
cpu.color("red")
cpu.shape("square")
cpu.shapesize(stretch_wid=3, stretch_len=0.25)  # player hitbox and shape
cpu.goto(screenWidth - 20, 0)

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
        for col in range(len(menuText[row])): #nested for loop to get index of the text and position
            text = menuText[row][col] #sets text to the x, y coordinate

            scoreBoard.goto(0, yPositions[row] - col * 40) #uses the index with scaling to make the text to go to the necessary area
            scoreBoard.write(text, align="center", font=("Courier", 20, "normal")) #writes the text

def setBoundaries():
    boundry.clear()
    boundry.penup()
    boundry.goto(0, screenHeight)
    while boundry.ycor() > -screenHeight:  # loop that makes dash lines from top to bottom
        boundry.sety(boundry.ycor() - 10)
        boundry.penup()
        boundry.sety(boundry.ycor() - 10)
        boundry.pendown()

    boundry.penup()
    boundry.goto(-screenWidth - 10, screenHeight)

    boundry.pendown()
    boundry.goto(screenWidth + 10, screenHeight)  # makes a box
    boundry.goto(screenWidth + 10, -screenHeight)
    boundry.goto(-screenWidth - 10, -screenHeight)
    boundry.goto(-screenWidth - 10, screenHeight)

def startGame():
    global gameState  # global so it can be modified

    if gameState != "menu":  # makes sure the game hasn't already started
        return
    
    chooseDifficulty()

    scoreBoard.clear()  # clears to prevent overlapping
    setBoundaries()

    ball.goto(0, 0)
    ball.setheading(random.choice([0, 180]))  # randomizes the direction (player or cpu)
    ball.showturtle()
    cpu.showturtle()
    player.showturtle()

    gameState = "playing"  # makes the game state to playing so playing functions run

    updateScore(False)  # writes the score but doesn't add a point

    moveBall()  # starts the function that moves the ball
    moveComputer()  # starts the function that makes the computer track the ball

def playAgain():
    global score  # makes variables modifiable
    global ballSpeed
    global gameState

    score = 0  # resets score
    ballSpeed = 4  # resets ball speed
    gameState = "menu"  # makes state menu so moveBall() and moveComputer() stop

    ball.goto(0, 0)  # resets ball position
    ball.setheading(random.choice([0, 180]))
    player.showturtle()
    cpu.showturtle()
    player.goto(-screenWidth + 20, 0)
    cpu.goto(screenWidth - 20, 0)

    updateScore(False)  # shows score but doesn't update score

    showInstructions()  # reshows instructions when playing again

def updateScore(addScore):
    global score

    if addScore:  # increments the score if told
        score += 1
    scoreBoard.clear()  # shows the score in the correct position
    scoreBoard.goto(-screenWidth - 50, screenHeight + 40)
    scoreBoard.write(f"Score: {score} | {difficulty.upper()} MODE", align="center", font=("Courier", 30, "bold"))

def gameOver():
    global gameState
    gameState = "gameOver"  # makes the state gameover for functions to react appropriately

    player.hideturtle()  # hides paddles
    cpu.hideturtle()

    scoreBoard.clear()
    scoreBoard.goto(0, screenHeight - 50)

    scoreBoard.write("Game Over!", align="center", font=("Courier", 30, "normal"))
    scoreBoard.sety(scoreBoard.ycor() - 50)
    scoreBoard.write(f"Your score was {score}", align="center", font=("Courier", 30, "normal"))

    highScores = []
    try:
        with open("highscore.txt", 'r') as f:  # opens the highscore file
            for line in f:  # takes each line in the file
                highScores.append(int(line.strip()))  # adds it to a list to be sorted (because every line is a number)
    except FileNotFoundError:  # if the file couldn't be found
        print("LOG: Could not load save file\n")  # prints so it can be found in terminal
        highScores = []  # just has empty list without save

    if score > 0 and difficulty == "hard": #only counts as high score if is in hard mode
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
    ball.forward(ballSpeed)  # ball speed is increased over time for difficulty

    if ball.ycor() > screenHeight - 10 or ball.ycor() < -screenHeight + 10:
        ball.setheading(360 - ball.heading())  # if the ball touches a top wall
    if ball.xcor() < -screenWidth + 40 and ball.distance(player) < 50:  # if the ball touches the player
        ball.setheading(
            180 - ball.heading() + random.randint(-30, 30))  # move the ball the opposite direction with a random offset
        ball.setx(-screenWidth + 41)  # in case of glitching make it go away from edge
        updateScore(True)

        if ballSpeed < 15:  # makes sure the ball speed is less than 15 (this is too fast)
            ballSpeed += speedIncrease  # increases by difficulty amount
    if ball.xcor() > screenWidth - 40 and ball.distance(cpu) < 50:  # if the ball touches the computer
        ball.setheading(180 - ball.heading() + random.randint(-30, 30))  # same logic as player collision

        # makes sure the ball does not go almost straight up (making it boring and long for players to watch)
        angle = ball.heading()
        if 0 < angle < 20:
            ball.setheading(20)
        elif 160 < angle < 180:
            ball.setheading(160)
        elif 180 < angle < 200:
            ball.setheading(200)
        elif 340 < angle < 360:
            ball.setheading(340)

        ball.setx(screenWidth - 41)  # prevents glitching
    if ball.xcor() < -screenWidth:
        gameOver()  # game over if the ball has passed the width boundary
        return  # stops the ontimer call so the function ends


    window.ontimer(moveBall, 15)  # repeatedly calls the function every 15 milliseconds until stopped

def moveUp():
    if player.ycor() < screenHeight - 25 and gameState == "playing":
        player.sety(player.ycor() + paddleSpeed)  # moves up if the game is running and player isn't touching the top
def moveDown():
    if player.ycor() > -screenHeight + 25 and gameState == "playing":
        player.sety(player.ycor() - paddleSpeed)  # moves down if the game is running and player isn't touching bottom
        

def moveComputer():
    if gameState == "playing":
        if abs(cpu.ycor() - ball.ycor()) > random.randint(5, 20):  # randomized computer movement
            if cpu.ycor() < ball.ycor() and cpu.ycor() < screenHeight - 25:
                cpu.sety(
                    cpu.ycor() + paddleSpeed)  # goes up if the ball is above the computer and less then the screen height (safety check)
            elif cpu.ycor() > ball.ycor() and cpu.ycor() > -screenHeight + 25:
                cpu.sety(cpu.ycor() - paddleSpeed)  # same for going down


    window.ontimer(moveComputer, 15)  # does this at same rate as moveBall()]

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

showInstructions()  # shows the instructions to start the loop
window.mainloop() #continuously runs the program


