# A pygame based ball hitting game
# Get points for hitting the ball, with the ability to save high scores


import pygame
import random
import sys
import os

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

MENU_SCREEN = 0
GAME_SCREEN = 1
HIGH_SCORE_SCREEN = 2
SAVE_SCORE_SCREEN = 3

# Stores the required winning score
WINNING_SCORE = 100
# The maximum play time for a round in seconds
PLAY_TIME = 10

HIGH_SCORE_FILE = 'highscores.txt'

# Set the max speed the player can move - changing this value can increase/decrease difficulty
PLAYER_SPEED = 25

# set the max speed the AI can move - changing this value can increase/decrease difficulty
AI_SPEED = 1

# set the max speed the ball can move - changing this value can increase/decrease difficulty
BALL_SPEED = 1

# set the size of the ball - changing this value can increase/decrease difficulty
BALL_SIZE = 100


# Used to get all the high scores from a file
# returns a list of high scores and their creators in the form {'1st':[name, score], '2nd':[name, score], '3rd':[name, score]}
# The file itself is in the form 1st:name:score, 2nd:name:score, 3rd:name:score
def get_high_scores(file_name):
    content = ""  # Used to store content from the file

    # Check if the file exists, if it does exist...
    if os.path.isfile(file_name):
        # We open the file and save its contents to the content variable
        # When we open a file using with, the file is automatically closed after we
        # are finished, so we don't need to wory about closing it. If you're not accessing
        # a file in this way, you must remember to close it after use
        with open(file_name, 'r') as content_file:
            content = content_file.read()
    # If it doesn't exist, we create the file and populate it with default values
    else:
        f = open(file_name, 'w')
        content = "1st::0,2nd::0,3rd::0"  # We also set content with the default values to avoid any errors in future code
        f.write(content)  # write the contents to file
        f.close()  # close the file

    content_list = content.split(',')  # Split the content into different parts by splitting at every ','

    to_return = {}  # create an empty dictionary that will be populated and then returned

    for element in content_list:  # For each element in list
        l = element.split(
            ':')  # Split the element into the title name and score sections, which are stored as a list in the variable l
        # use the first variable in the list l as the key in the dictionary to_return, which references a
        # list containing the second and third values
        to_return[l[0]] = [l[1], l[2]]

    return to_return  # return the dictionary


# writes the high scores out to the high score file, taking the score dictionary and file_name as input
def write_high_scores(file_name, scores):
    f = open(file_name, 'w')  # open the file for writing
    to_write = ""  # create an empty string to store the data we will write to our file
    # cycle through the different scores, writing the values in the correct format and adding them to the string
    for name in ('1st', '2nd', '3rd'):
        to_write += name
        to_write += ':'
        to_write += str(scores.get(name)[0])
        to_write += ':'
        to_write += str(scores.get(name)[1])
        to_write += ','

    print(to_write)
    to_write = to_write[
               :-1]  # Remove the last character from the two_write string - this is an unnecessary comma created by our loop
    f.write(to_write)  # write the string to the file
    f.close()  # close the file


# Updates the high score file with a new score, placing it in the relevant location (i.e. highest, next highest etc.)
# Depending on the score
def set_high_score(file_name, player_name, score):
    scores = get_high_scores(file_name)  # get a dictionary of the current high scores

    # If we have a new high score, update the values in the dictionary
    if (int(score) >= int(scores.get('1st')[1])):
        scores['1st'][0] = player_name
        scores['1st'][1] = score
    # Else if we have a new next highest score, update this value
    elif (int(score) >= int(scores.get('2nd')[1])):
        scores['2nd'][0] = player_name
        scores['2nd'][1] = score
    # Else if our score is lower than anyone elses, update this value.
    elif (int(score) >= int(scores.get('3rd')[1])):
        scores['3rd'][0] = player_name
        scores['3rd'][1] = score

    write_high_scores(file_name, scores)
    print(scores)


def draw_set_high_scores(screen, player_name, high_score):
    font = pygame.font.Font(None, 36)  # Choose the font for the title

    # Draw the title
    text = font.render("Save Your Score of " + str(high_score), 1, BLACK)  # Create the text
    screen.blit(text, (200, 100))  # Draw the text on the screen

    # Set up the font for the text
    font = pygame.font.Font(None, 30)  # Choose the font for the text, making it a bit smaller than the title

    text = font.render("First type your name.", 1, BLACK)  # Create the text
    screen.blit(text, (220, 200))  # Draw the text on the screen

    text = font.render("Name: " + player_name, 1, BLACK)  # Create the text
    screen.blit(text, (260, 250))  # Draw the text on the screen

    text = font.render("Press Enter to save your score", 1, BLACK)  # Create the text
    screen.blit(text, (190, 400))  # Draw the text on the screen


# Draws the high scores on the screen
def draw_high_scores(screen, file_name):
    scores = get_high_scores(file_name)  # Get the high scores as a dictionary

    # Set up the font for the title
    font = pygame.font.Font(None, 36)  # Choose the font for the title

    # Draw the title
    text = font.render("HIGH SCORES", 1, BLACK)  # Create the text
    screen.blit(text, (250, 100))  # Draw the text on the screen

    # Set up the font for the text
    font = pygame.font.Font(None, 30)  # Choose the font for the text, making it a bit smaller than the title

    # Draw the rest of the options
    # Draw the highest score
    text = font.render("1st: " + scores.get('1st')[0] + " - " + scores.get('1st')[1], 1, BLACK)  # Create the text
    screen.blit(text, (290, 200))  # Draw the text on the screen

    # draw the next highest score
    text = font.render("2nd: " + scores.get('2nd')[0] + " - " + scores.get('2nd')[1], 1, BLACK)  # Create the text
    screen.blit(text, (290, 250))  # Draw the text on the screen

    # Draw the lowest score
    text = font.render("3rd: " + scores.get('3rd')[0] + " - " + scores.get('3rd')[1], 1, BLACK)  # Create the text
    screen.blit(text, (290, 300))  # Draw the text on the screen

    # Add instructions on how to escape the high scores screen and return to the menu
    text = font.render("Press E to return to the menu.", 1, BLACK)  # Create the text
    screen.blit(text, (200, 400))  # Draw the text on the screen


# Draws the menu on the screen
def draw_main_menu(screen):
    # Set up the font for the title
    font = pygame.font.Font(None, 36)  # Choose the font for the title

    # Draw the title
    text = font.render("WELCOME", 1, BLACK)  # Create the text
    screen.blit(text, (280, 100))  # Draw the text on the screen

    # Set up the font for the text
    font = pygame.font.Font(None, 30)  # Choose the font for the text, making it a bit smaller than the title

    # Draw the rest of the options
    text = font.render("1. P to Play", 1, BLACK)  # Create the text
    screen.blit(text, (290, 200))  # Draw the text on the screen

    text = font.render("2. Q to Quit", 1, BLACK)  # Create the text
    screen.blit(text, (290, 250))  # Draw the text on the screen

    text = font.render("3. S to Save", 1, BLACK)  # Create the text
    screen.blit(text, (290, 300))  # Draw the text on the screen

    text = font.render("4. V to View High Scores", 1, BLACK)  # Create the text
    screen.blit(text, (230, 350))  # Draw the text on the screen


# Draws the timer on the screen, showing the amount of time left to the player
def draw_timer(screen, x, y, time_left):
    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render("Time Left = " + str(time_left), 1, WHITE)  # Create the text
    screen.blit(text, (x, y))  # Draw the text on the screen


# Draws the game over box on the screen for when we have collided
# With the AI player or the game runs out of time, we have added message_1 and message_2
# paramaters to the function definition so we can set which message to display to the user
def draw_game_over(screen, message_1, message_2):
    pygame.draw.rect(screen, WHITE, (150, 200, 400, 100), 0)  # Draw a white box for the text to sit in

    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render(message_1, 1, BLACK)  # Create the text for "GAME OVER"
    screen.blit(text, (170, 220))  # Draw the text on the screen
    text = font.render(message_2, 1, BLACK)  # Create the text for "You hit the other player"
    screen.blit(text, (170, 260))  # Draw the text on the screen

    font = pygame.font.Font(None, 28)  # Make the font a bit smaller for this bit
    text = font.render("Press S to save your score. "
                       "Press P to play again. "
                       "Press E to return to the menu.", 1,
                       WHITE)  # Create text for instructions on what to do now
    screen.blit(text, (100, 350))  # Draw the text on the screen


# Create the text used to display the score and draw it on the screen
def draw_score(screen, x, y, score):
    font = pygame.font.Font(None, 36)  # Choose the font for the text
    text = font.render("Score = " + str(score), 1, WHITE)  # Create the text
    screen.blit(text, (x, y))  # Draw the text on the screen


# This function draws the ball
def draw_ball(screen, x, y):
    pygame.draw.circle(screen, GREEN, [x, y], BALL_SIZE, 0)


background_image = 'background.jpeg'  # file name of the background image


# This function draws the background on the screen
# max_x and max_y are the maximum x and y values of the screen
def draw_background(screen, file_name):
    myimage = pygame.image.load(file_name)
    imagerect = myimage.get_rect()
    screen.blit(myimage, imagerect)


# This function draws the smaller user-controllable stick figure on the screen
# Colour and scale paramaters have been added to the stick figure so that different varieties of stick figure
# can be produced whilst using the same function, with the scale being used
# to adjust the size of the stick figure, and the colour being used to set the colour of the stick figures body.
def draw_stick_figure(screen, x, y, colour, scale):
    # Draw the Head
    # Each value is adjusted by the scale paramater to adjust the size of the stick figure
    # We have to convert this value to an int as scale may be a float, a type that is not
    # accepted by pygame.draw.ellipse
    pygame.draw.ellipse(screen, BLACK, [int(1 * scale) + x, y, int(10 * scale), int(10 * scale)], 0)

    # Legs
    # Right leg (colour, length of leg....)
    pygame.draw.line(screen, BLACK, [int(5 * scale) + x, int(17 * scale) + y],
                     [int(10 * scale) + x, int(27 * scale) + y], int(2 * scale))
    # Left Leg
    pygame.draw.line(screen, BLACK, [int(5 * scale) + x, int(17 * scale) + y], [x, int(27 * scale) + y], int(2 * scale))

    # Body
    pygame.draw.line(screen, colour, [int(5 * scale) + x, int(17 * scale) + y],
                     [int(5 * scale) + x, int(7 * scale) + y], int(2 * scale))

    # Arms
    pygame.draw.line(screen, colour, [int(5 * scale) + x, int(7 * scale) + y],
                     [int(9 * scale) + x, int(17 * scale) + y], int(2 * scale))
    pygame.draw.line(screen, colour, [int(5 * scale) + x, int(7 * scale) + y],
                     [int(1 * scale) + x, int(17 * scale) + y], int(2 * scale))


# This function ensures that the number entered is between the range of the min and max values (inclusive).
# If the number is outside of this range, we return the closest allowed value. I.e. if the max was 10 and the number
# entered was 12, 10 would be returned as this is the maximum value allowed
def keep_in_range(number, min_no, max_no):
    if (number < min_no):
        return min_no
    elif (number > max_no):
        return max_no
    else:
        return number


# Setup
pygame.init()

# Set the width and height of the screen [width,height]

screen_size = [700, 500]
screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption("My Game")

# A boolean variable that stores whever the game is over
# Starts off set to False
game_over = False

# A boolean variable that stores whether the game has ended due to time running out
game_ended = False

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Counts the number of times the screen has been redrawn, incremented for every pygame.display.flip()
step = 0

# Stores the score of the player
score = 0

# keeps track of the current game 'room', this is either the menu or the game
room = MENU_SCREEN

# Stores the player name
player_name = ""

# the users highest score whilst playing the game
high_score = 0

# Stores the step at which the last score was made
# Starts with a value of -100 so we can score on the first step of the game
last_score_step = -100

# Hide the mouse cursor
pygame.mouse.set_visible(0)

# Speed in pixels per frame
x_speed = 0
y_speed = 0

# Current position
x_coord = 300
y_coord = 1

# AI Players current position
ai_x_coord = 300
ai_y_coord = 300

# The AI players last position
old_ai_x_coord = 300
old_ai_y_coord = 300

ai_moves = (-AI_SPEED, 0, AI_SPEED)  # A list of moves that the ai player can make each turn

# stores the current direction the ai character is moving
ai_x_direction = 0
ai_y_direction = 0

# Balls current position
ball_x_coord = 300
ball_y_coord = 300

old_ball_x_coord = 300
old_ball_y_coord = 300

# Controls the different moves the ball can make, change these values
# To change the ball speed
ball_moves = (-BALL_SPEED, BALL_SPEED)

ball_x_directon = 0
ball_y_direction = 0

# Stores the start time of the game in milliseconds
start_time = pygame.time.get_ticks()

# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():

        # If we are in the menu screen
        if room == MENU_SCREEN:
            if event.type == pygame.QUIT:
                done = True
                # User pressed down on a key

            elif event.type == pygame.KEYDOWN:

                # if p is pressed, the user wants to play the game
                if event.key == pygame.K_p:
                    room = GAME_SCREEN  # we therefore move to the game screen

                    # And we reset all the variables ready for the game to be played
                    score = 0
                    step = 0
                    last_score_step = 0
                    x_coord = 300
                    y_coord = 1

                    ai_x_coord = 300
                    ai_y_coord = 300

                    game_over = False
                    game_ended = False

                    start_time = pygame.time.get_ticks()  # reset the start time

                # If q is pressed, the user wants to quit the game
                elif event.key == pygame.K_q:
                    done = True  # we set done = True to exit the loop

                # If s is pressed the user wants to save their score
                elif event.key == pygame.K_s:
                    room = SAVE_SCORE_SCREEN

                # If v is pressed, the user wants to view the high scores
                elif event.key == pygame.K_v:
                    room = HIGH_SCORE_SCREEN  # set the room to the high score screen

        # If we are in the high score room, displaying the high score screen
        elif room == HIGH_SCORE_SCREEN:
            if event.type == pygame.QUIT:
                done = True
                # User pressed down on a key

            elif event.type == pygame.KEYDOWN:
                # If e is pressed, return to the menu screen
                if event.key == pygame.K_e:
                    room = MENU_SCREEN

        # If we are saving our high score, deal with inputs relevent to saving the score
        # Saving the score and getting the users name is more tricky than the rest of the game, to do it without any external
        # libraries, you have to convert object keys to chars and ensure they are within range of the alphabet.
        elif room == SAVE_SCORE_SCREEN:
            if event.type == pygame.QUIT:
                done = True
            # if the user presses down on a key
            elif event.type == pygame.KEYDOWN:
                # Check if the key is within range of the alphabet
                # This works as event.key is really just the ordinal value of an ascii character
                if (event.key >= pygame.K_a) and (event.key <= pygame.K_z):
                    player_name += chr(event.key)  # Convert the ordinal value to a char and append it to player name

                # If the key pressed is backspace, delete the last character
                elif (event.key == pygame.K_BACKSPACE):
                    if (len(player_name) > 1):
                        player_name = player_name[:-1]
                    else:
                        player_name = ""
                # If they press enter, save the name and high score and return to the menu screen
                elif (event.key == pygame.K_RETURN):
                    set_high_score(HIGH_SCORE_FILE, player_name, high_score)
                    room = MENU_SCREEN



        # If we are playing the game, deal with all game inputs relevant to the game
        elif room == GAME_SCREEN:
            if event.type == pygame.QUIT:
                done = True
                # User pressed down on a key

            elif event.type == pygame.KEYDOWN:

                # Figure out if it was an arrow key. If so
                # adjust speed.

                if event.key == pygame.K_LEFT:
                    x_speed = -PLAYER_SPEED
                elif event.key == pygame.K_RIGHT:
                    x_speed = PLAYER_SPEED
                elif event.key == pygame.K_UP:
                    y_speed = -PLAYER_SPEED
                elif event.key == pygame.K_DOWN:
                    y_speed = PLAYER_SPEED

                # If the game_over or the game_ended boolean is true, then we are on the game over screen
                # Players therefore have multiple options for what to do on these screens
                if (game_over or game_ended):
                    # If they press p, they have decided to play again, therefore we reset all the variables
                    # and set game_over to False so the player can try again
                    if event.key == pygame.K_p:
                        score = 0
                        step = 0
                        last_score_step = 0
                        x_coord = 300
                        y_coord = 1

                        ai_x_coord = 300
                        ai_y_coord = 300

                        game_over = False
                        game_ended = False

                        start_time = pygame.time.get_ticks()  # reset the start time
                    # If they press e, they have decided to return to the menu, so we change the room to menu
                    elif event.key == pygame.K_e:
                        room = MENU_SCREEN
                    elif event.key == pygame.K_s:
                        room = SAVE_SCORE_SCREEN

            # User let up on a key
            elif event.type == pygame.KEYUP:
                # If it is an arrow key, reset vector back to zero
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_speed = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_speed = 0

    # --- Game Logic
    # Only execute the game logic if we are on the game screen
    if room == GAME_SCREEN:
        # Check if Games time is up (it has been more than 30 seconds from when we started the game)
        if (start_time + (PLAY_TIME * 1000) <= pygame.time.get_ticks()):
            # If the time is up, set the boolean game_ended to True
            # so we can display the correct game over screen
            game_ended = True

            # Move the object according to the speed vector.
        x_coord = x_coord + x_speed
        y_coord = y_coord + y_speed

        if (x_coord < 0):
            x_coord = 0

        if (y_coord < 0):
            y_coord = 0

        # Adjust the x and y co-ordinates to ensure that the stick figure is kept on the screen and can't
        # travel off of it
        x_coord = keep_in_range(x_coord, 0, screen_size[
            0] - 10)  # We adjust the upper limit of our allowed range to match the stick figures width
        y_coord = keep_in_range(y_coord, 0, screen_size[
            1] - 27)  # We adjust the upper limit of our allowed range to match the stick figures height

        # MOVE THE AI PLAYER
        # Every 30 steps (screen draws) we change the direction the ai player is moving in
        # This makes the movement of the ai player look more realistic. This works because
        # step % 30 is gives the remained when the value step is divided by 30, which will only
        # occur every 30 steps. You can experiment with changing this value and seeing how the ai
        # character moves
        if (step % 30 == 0):
            ai_x_direction = random.choice(ai_moves)
            ai_y_direction = random.choice(ai_moves)

        # Update the old ai co-ordinate values
        old_ai_x_coord = ai_x_coord
        old_ai_y_coord = ai_y_coord

        # move the ai player in the chosen direction
        ai_x_coord = ai_x_coord + ai_x_direction
        ai_y_coord = ai_y_coord + ai_y_direction

        # Limit the ai character to ensure it stays on the screen
        ai_x_coord = keep_in_range(ai_x_coord, 0, screen_size[0] - 20)
        ai_y_coord = keep_in_range(ai_y_coord, 0, screen_size[1] - 54)

        # If our x co-ordinate has not changed, then we could have collided with a screen edge so we reverse the direction
        # This helps to keep the movement looking natural by preventing the ai player from repeatedly
        # moving along the edge of the screen
        if (ai_x_coord == old_ai_x_coord):
            ai_x_direction *= -1;
        # the same is true for the y co-ordinate
        if (ai_y_coord == old_ai_y_coord):
            ai_y_direction *= -1;

        # MOVE THE BALL
        # Randomly move the ball basically in the same way as the ai player
        # Every 50 steps update the ball direction with a new random one
        if (step % 50 == 0):
            ball_x_direction = random.choice(ball_moves)
            ball_y_direction = random.choice(ball_moves)

        # update the old ball coord
        old_ball_x_coord = ball_x_coord
        old_ball_y_coord = ball_y_coord

        # Move the ball in the chosen direction
        ball_x_coord += ball_x_direction
        ball_y_coord += ball_y_direction

        ball_x_coord = keep_in_range(ball_x_coord, 0, screen_size[0])
        ball_y_coord = keep_in_range(ball_y_coord, 0, screen_size[1])

        # If our x co-ordinate has not changed, then we could have collided with a screen edge so we reverse the direction
        # This helps to keep the movement looking natural by preventing the ai player from repeatedly
        # moving along the edge of the screen
        if (ball_x_coord == old_ball_x_coord):
            ball_x_direction *= -1;
        # the same is true for the y co-ordinate
        if (ball_y_coord == old_ball_y_coord):
            ball_y_direction *= -1;

        # Tests if the ball has collided with the player
        if (ball_x_coord - BALL_SIZE <= x_coord + 5) and (ball_x_coord + BALL_SIZE >= x_coord - 5) and (
                ball_y_coord - BALL_SIZE <= y_coord + 27) and (ball_y_coord + BALL_SIZE >= y_coord):
            # Register the score if it is more than 10 steps after the last score
            # This is necessary as the ball has a habit of double bouncing against the player
            # Meaning that we register multiple hits with only one true collision
            if (last_score_step + 10 < step):
                score += 10;  # increment the score
                # reverse the ball direction
                ball_x_directon *= -1
                ball_y_direction *= -1
                last_score_step = step  # record the step at which this score is made

                print(score)

        # Test if the player has collided with the ai
        if (x_coord - 5 <= ai_x_coord + 10) and (x_coord + 5 >= ai_x_coord) and (y_coord - 3 <= ai_y_coord + 54) and (
                y_coord + 27 >= ai_y_coord):
            print("COLLIDED WITH AI")
            game_over = True  # set the game over boolean to True so we can trigger the end of the game

    # --- Drawing Code

    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)  # erase the previous screen

    # If the current room is the menu, draw the menu
    if room == MENU_SCREEN:
        draw_main_menu(screen)

    # If the current room is the high score screen, draw the high scores
    elif room == HIGH_SCORE_SCREEN:
        draw_high_scores(screen, HIGH_SCORE_FILE)
    # Else if we are in the set high scores room
    elif room == SAVE_SCORE_SCREEN:
        draw_set_high_scores(screen, player_name, high_score)  # Draw the set high scores screen

    # if the current room is the game, draw the game
    elif room == GAME_SCREEN:
        draw_background(screen, background_image)  # draw the background

        # If the game isn't over we draw the game
        if not game_over and not game_ended:
            draw_stick_figure(screen, x_coord, y_coord, RED, 1)  # draw the user controlled stick figure on the screen
            draw_stick_figure(screen, ai_x_coord, ai_y_coord, BLUE,
                              2)  # draw the ai controlled stick figure on the screen

            draw_ball(screen, ball_x_coord, ball_y_coord)

            # Draw the score on the screen
            draw_score(screen, 550, 450, score)

            # Calculate how much time is left by subtracting the current time
            # from the start time, and then this value from the maximum allowed time (30 seconds).
            # As these times are stored in milliseconds, we then
            # divide by 1000 to convert to seconds, and convert the result to an integer
            # value so that only whole seconds are shown.
            time_left = pygame.time.get_ticks() - start_time  # find out how much time has passed since the start of the game
            time_left = time_left / 1000  # Convert this time from milliseconds to seconds
            time_left = PLAY_TIME - time_left  # Find out how much time is remaining by subtracting total time from time thats passed
            time_left = int(time_left)  # Convert this value to an integer
            draw_timer(screen, 50, 450, time_left)  # Once we have calculated how much time is left, draw the timer

        # Else if the game is over (i.e. because we collided with the ai player)
        # We print the game over screen
        elif game_over:
            draw_game_over(screen, "YOU LOSE, SORRY TRY AGAIN",
                           "You hit the other player!")  # draw the game over screen
        # Else if the game has ended because the player has run out of time, we print a different game over
        # screen
        elif game_ended:
            # If the score is >= 100, the player has one the game
            if score >= WINNING_SCORE:
                draw_game_over(screen, "YOU WIN THE GAME!", "Final Score: " + str(score))

                # If this score is the highest that has been achieved during this execution of the game
                # Update the high score variable
                if (score > high_score):
                    high_score = score
            # Otherwise they didn't win, so we draw a you lose screen
            else:
                draw_game_over(screen, "YOU LOSE, SORRY TRY AGAIN", "You didn't score enough points")

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    step += 1  # increment step

    # Limit frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()