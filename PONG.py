import pygame
import random

pygame.display.set_caption('PONG')

# Game Window
s_width= 900
s_height= 600
screen= pygame.display.set_mode((s_width, s_height))

# Game Components
top_border= pygame.Rect(0, 0, 900, 5)
bottom_border= pygame.Rect(0, 595, 900, 5)



class Ball:
    def __init__(self):
        self.ball_xspeed= 0.4 * random.choice((1,-1))
        self.ball_yspeed= 0.5 * random.choice((1,-1))
        self.ball_width= 15
        self.ball_height= 15
        self.ball_x= ((s_width/2)-(self.ball_width/2))
        self.ball_y= ((s_height/2)-(self.ball_height/2))
        self.ball= pygame.Rect(self.ball_x, self.ball_y, self.ball_width, self.ball_height)

    def draw_ball(self):
        global scoretime
        tsec= 0
        self.current_time = pygame.time.get_ticks() #Continuous recording of time

        if scoretime is not None: #if the scoretime has been recorded
            time_since_reset = self.current_time - scoretime
            if time_since_reset < 3300:  # Ball pause duration
                if time_since_reset<= 1000:
                    tsec=3
                    tsecs= mini_text.render(f"{tsec}", False, "grey")
                    screen.blit(tsecs, (446,315))
                elif 1000 < time_since_reset<= 2000:
                    tsec=2
                    tsecs= mini_text.render(f"{tsec}", False, "grey")
                    screen.blit(tsecs, (446,315))
                elif 2000 < time_since_reset<= 3000:
                    tsec=1
                    tsecs= mini_text.render(f"{tsec}", False, "grey")
                    screen.blit(tsecs, (446,315))
                else:
                    tsec="GO"
                    tsecs= mini_text.render(f"{tsec}", False, "grey")
                    screen.blit(tsecs, (439,315))



                # Reset ball position and stop movement temporarily
                self.ball_x, self.ball_y = (s_width / 2 - self.ball_width / 2), (s_height / 2 - self.ball_height / 2)
                self.ball_xspeed = 0
                self.ball_yspeed = 0
    
            else:
                # Restart the ball movement after the delay
                self.ball_xspeed = 0.4 * random.choice((1, -1))
                self.ball_yspeed = 0.5 * random.choice((1, -1))
                scoretime = None  # Reset scoretime to allow normal ball movement

        # Move the ball normally if scoretime is None
        self.ball_x += self.ball_xspeed
        self.ball_y += self.ball_yspeed
        self.ball.topleft = (self.ball_x, self.ball_y)
        pygame.draw.rect(screen, (250, 200, 80), self.ball)

    def ball_collisions(self):
#set global variables for the player and cpu score --> updates whenever the ball is scored
        global player_score , cpu_score, scoretime
        if self.ball.bottom >= (s_height - 7):
            pygame.draw.rect(screen, (250,100,200), bottom_border)
            if self.ball.bottom > s_height:
                self.ball_yspeed *= -1
        if self.ball.top <= 7:
            pygame.draw.rect(screen, (250,100,200), top_border)
            if self.ball.top < 0:
                self.ball_yspeed *= -1

#Change ball velocity to add variation (only when the user of cpu successfully hits ball)
        if self.ball.colliderect(player_rect):
            self.ball_x += 3  # Push the ball slightly away from the paddle
            self.ball_xspeed *= -1.05  # Reverse and slightly increase speed
            self.ball_yspeed *= random.uniform(0.9, 1.1)  # Add variation to y-speed
        if self.ball.colliderect(cpu_rect):
            self.ball_x -= 3
            self.ball_xspeed *= -1.05
            self.ball_yspeed *= random.uniform(0.9, 1.1)

#Out of Bounds
        if self.ball_x > 930:
            player_score += 1
            #set ball position back to the middle, and then set scoretime to the current moment (one time)
            self.ball_x, self.ball_y= ((s_width/2)-(self.ball_width/2)), ((s_height/2)-(self.ball_height/2))  
            scoretime= pygame.time.get_ticks()
        if self.ball_x < -30:
            cpu_score += 1
            self.ball_x, self.ball_y= ((s_width/2)-(self.ball_width/2)), ((s_height/2)-(self.ball_height/2))  
            scoretime= pygame.time.get_ticks() 



class CPU:
    def __init__(self):
        self.cpu_width= 10
        self.cpu_height= 80
        self.cpu_x= 840
        self.cpu_y= (s_height/2)- (self.cpu_height/2)
        
    def draw_cpu(self):
        global cpu_rect
        cpu_rect= pygame.Rect(self.cpu_x, self.cpu_y, self.cpu_width, self.cpu_height)
        pygame.draw.rect(screen, (50, 250, 130), cpu_rect)
    
    def cpu_movement(self, ball_x, ball_y, ball_speed):
        # Move only if the ball is on the CPU side of the screen
        if ball_x > s_width / 1.95:
            if ball_speed > 0:
                if ball_y > self.cpu_y + self.cpu_height / 2:
                    # Ball is below the paddle center, move down
                    self.cpu_y += 0.4
                elif ball_y < self.cpu_y + self.cpu_height / 2:
                    # Ball is above the paddle center, move up
                    self.cpu_y -= 0.5

            # Prevent the paddle from going out of bounds
            if self.cpu_y < 0:
                self.cpu_y = 0
            elif self.cpu_y > s_height - self.cpu_height:
                self.cpu_y = s_height - self.cpu_height



class Player:
    def __init__(self):
        self.player_width= 10
        self.player_height= 80
        self.player_x= 40
        self.player_y= (s_height/2)- (self.player_height/2)

    def draw_player(self):
        global player_rect
        player_rect= pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        pygame.draw.rect(screen, (130,50,250), player_rect)

    def player_movement(self):
        key= pygame.key.get_pressed()

        if key[pygame.K_w] or key[pygame.K_UP]:
            self.player_y -= 0.6
            if self.player_y < 0:
                self.player_y= 0
        elif key[pygame.K_s]== True or key[pygame.K_DOWN]== True:
            self.player_y += 0.6
            if self.player_y >= 520:
                self.player_y= (s_height- 80)


#Initialize classes and game
pygame.init()

player1= Player()
cpu= CPU()
ball= Ball()
scoretime = pygame.time.get_ticks()


#Game Board Variable
player_score= 0
cpu_score= 0
text= pygame.font.Font("freesansbold.ttf", 34)
mini_text= pygame.font.Font("freesansbold.ttf", 19)


#Game Loop
run= True
while run:
    screen.fill((30,30,30))

    pygame.draw.rect(screen, (100,200,250), top_border)
    pygame.draw.rect(screen, (100,200,250), bottom_border)
    #draw the border line on the scree, with the colour grey, xtart position = half of the scren width and at the top- and ends at the half of the screen width, and the full screen height
    pygame.draw.aaline(screen, "grey", (s_width/2, 0), (s_width / 2, s_height))



    player1.draw_player()
    player1.player_movement()

    cpu.draw_cpu()
    cpu.cpu_movement(ball.ball_x, ball.ball_y, ball.ball_xspeed)

    ball.draw_ball()
    ball.ball_collisions()


    if player_score < 4 or cpu_score < 4:
        #render the player's score as a text on a new screen, and place that screen over the game
        player_text= text.render(f"{player_score}", False, "grey")
        screen.blit(player_text, (410, 200))
        #same but for cpu score
        cpu_text= text.render(f"{cpu_score}", False, "grey")
        screen.blit(cpu_text, (470, 200))
        if player_score >= 3 or cpu_score >= 3:
            winner= "Player" if player_score >= 3 else "CPU"
            end_text= text.render(f"{winner} Wins!", True, "white")
            screen.blit(end_text, (s_width / 2 - 100, s_height / 2 - 50))
            pygame.display.update()
            pygame.time.wait(3000)  # Pause for 3 seconds before quitting
            run= False

    


    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False

    pygame.display.update()

pygame.quit()