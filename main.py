#!/usr/bin/env python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock


class PongGame(Widget):

    """The main game object class"""

    """ObjectProperties are initially set to None and set to corresponding type in pong.kv. ObjectProperty classes are
    defined in the kivy library. The GUI updates automatically when ObjectProperties changes.
    """
    # PongBall type object set at pong.kv
    ball = ObjectProperty(None)
    # PongPaddle type object set at pong.kv. p1 is the player 1 object
    p1 = ObjectProperty(None)
    # PongPaddle type object set at pong.kv. p2 is the player 2 object
    p2 = ObjectProperty(None)

    def serve_ball(self):
        """Call at the start of the game and start of each round"""
        # Placing ball at the center
        self.ball.center = self.center
        # Velocity of the object is set
        self.ball.v = Vector(7, 0)  # .rotate(randint(0, 360))

    def update(self, dt):
        """Call at the required time intervals ie. frame rate"""
        # move the ball
        self.ball.move()

        # bounce if collided with a PongPaddle object
        self.p1.bounce_ball(self.ball)
        self.p2.bounce_ball(self.ball)

        # bounce if collided with upper and lower boundaries
        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.vy *= -1

        # bounce if collided with left and right boundaries
        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.vx *= -1

        # add to the player1 score if ball hits the left boundary. As score is a NumericProperty, the GUI updates
        #  automatically.
        if self.ball.x < 0:
            self.p2.score += 1
            # ball is served to start the next round
            self.serve_ball()

        # add to the player2 score if ball hits the right boundary. As score is a NumericProperty, the GUI updates
        #  automatically. Note ball.right is checked instead of ball.x which is the left boundary value.
        if self.ball.right > self.width:
            self.p1.score += 1
            # ball is served to start the next round
            self.serve_ball()

    def on_touch_move(self, touch):
        """User touch event definition. The corresponding PongPaddle is supposed to move when the right area is
        touched"""

        # space of p1 is the left third
        if touch.x < self.width / 3:
            self.p1.dy = self.p1.center_y - touch.y
            self.p1.center_y = touch.y
        # space of p2 is the right third
        if touch.x > self.width * 2 / 3:
            self.p2.dy = self.p2.center_y - touch.y
            self.p2.center_y = touch.y


class PongPaddle(Widget):

    """The player class"""

    # score of the player. Initialized with 0. GUI updates automatically as score is a NumericProperty. Score str
    #  is bound at pong.kv
    score = NumericProperty(0)
    # speed of the paddle
    dy = 0

    def bounce_ball(self, ball):
        """Call at each update()"""
        # if the pong paddle is collided with a ball, ball bounces with a different velocity than reflected velocity
        if self.collide_widget(ball):
            vx, vy = ball.v
            bounced = Vector(-vx, vy + self.dy)
            ball.v = bounced
            # ball.v = vel.x, vel.y


class PongBall(Widget):

    """The ball class"""

    # horizontal velocity of the ball initialized with 0
    vx = NumericProperty(0)
    # vertical velocity of the ball initialized with 0
    vy = NumericProperty(0)
    # velocity as a list
    v = ReferenceListProperty(vx, vy)

    def move(self):
        """Call at each time interval"""
        self.pos = Vector(*self.v) + self.pos


class PongApp(App):

    """The main application class"""

    def build(self):
        """called initially"""
        # main game object
        game = PongGame()
        # creating the ball at the center
        game.serve_ball()
        # scheduled game.update() 60 times per second
        Clock.schedule_interval(game.update, 1 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
