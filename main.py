from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (NumericProperty, ReferenceListProperty, ObjectProperty, ColorProperty)
from kivy.vector import Vector
from random import randint
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader


class PongPaddle(Widget):
    score = NumericProperty(0)
    color = ColorProperty((1, 1, 1, 1))  # Default color is white

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.15
            ball.velocity = vel.x, vel.y + offset
            


Window.clearcolor = (0.1, 0.1, 0.15, 1)


class PongBall(Widget):

    #velocity in x and y axis
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    #referance list property so we can use ball.velocity as a shorthand, just like e.g w.pos for w.x and w.y
    velocity = ReferenceListProperty(velocity_x, velocity_y)


    # "move" function will move the ball one step. This will be called in equal intervals to animate the ball
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)


    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        #call ball.move and other stuff
        self.ball.move()



    #bounce off paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)







        #bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1
        
        # went off to the left or right side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width /3: 
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width /3:
            self.player2.center_y = touch.y

    #Adding sound effects to the game
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.sound = SoundLoader.load('bounce.wav') 
    

class PongApp(App):


    def build(self):
        game = PongGame()
        game.serve_ball()
        self.music = SoundLoader.load('sounds\music.wav.wav')
        if self.music:
            self.music.loop = True
            self.music.play()

        Clock.schedule_interval(game.update, 1.0/60.0)
         
        
        return game
    



if __name__ == "__main__":

    PongApp().run()