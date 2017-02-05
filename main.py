#!/usr/bin/env python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongGame(Widget):

    ball = ObjectProperty(None)
    p1 = ObjectProperty(None)
    p2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.v = Vector(7, 0)  # .rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        self.p1.bounce_ball(self.ball)
        self.p2.bounce_ball(self.ball)

        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.vy *= -1

        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.vx *= -1

        if self.ball.x < self.x:
            self.p2.score += 1
            self.serve_ball()

        if self.ball.x > self.width:
            self.p1.score += 1
            self.serve_ball()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.p1.center_y = touch.y
        if touch.x > self.width * 2 / 3:
            self.p2.center_y = touch.y


class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.v
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.v = vel.x, vel.y + offset


class PongBall(Widget):

    vx = NumericProperty(0)
    vy = NumericProperty(0)

    v = ReferenceListProperty(vx, vy)

    def move(self):
        self.pos = Vector(*self.v) + self.pos


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
