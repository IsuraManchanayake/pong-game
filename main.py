#!/usr/bin/env python

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongGame(Widget):

    ball = ObjectProperty(None)

    def serve_ball(self):
        self.ball.center = self.center
        self.ball.v = Vector(7, 0).rotate(randint(0, 360))

    def update(self, dt):
        self.ball.move()

        if self.ball.y < 0 or self.ball.top > self.height:
            self.ball.vy *= -1

        if self.ball.x < 0 or self.ball.right > self.width:
            self.ball.vx *= -1


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