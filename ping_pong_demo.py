from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
 
class PongPaddle(Widget):
    score = NumericProperty(0) # player points
 
    # Ball bounce when colliding with the player's panel
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
 
            ball.velocity = vel.x, vel.y + offset
 
 
class PongBall(Widget):
 
    # The speed of movement of our ball along two axes
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
 
    # Create a conditional vector
    velocity = ReferenceListProperty(velocity_x, velocity_y)
 
    # Let's make the ball move
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
 
class PongGame(Widget):
    ball = ObjectProperty(None) # this will be our connection with the ball object
    player1 = ObjectProperty(None) # Player 1
    player2 = ObjectProperty(None) # Player 2
 
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(vel[0], vel[1]).rotate(randint(0, 360))
 
    def update(self, dt):
        self.ball.move() # move the ball in every screen update
 
        # checking the ball rebound from the players' panels
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
 
        # ball bounce along the axis Y
        if(self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1 # инверсируем текущую скорость по оси Y
 
        # ball bounce along the axis X
        # here if the ball was able to go beyond the player's panel, that is, the player did not have time to hit the ball
        # it means that he lost and we will add +1 point to the enemy
        if self.ball.x < self.x:
            # The first player lost, add 1 point to the second player
            self.player2.score += 1
            self.serve_ball(vel=(4,0)) # re-spawn the ball in the center
        if self.ball.x > self.width:
            # The second player lost, add 1 point to the first player
            self.player1.score += 1
            self.serve_ball(vel=(-4,0)) # re-spawn the ball to the center
 
    # Screen touch event
    def on_touch_move(self, touch):
        # the first player can only touch his part of the screen (left)
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
 
        # the second player can only touch his own part of the screen (right)
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
 
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60) # 60 FPS
        return game
 
if __name__ == '__main__':
    PongApp().run()
