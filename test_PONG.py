import pytest
import pygame
from PONG import Ball, CPU, Player

pygame.init()

s_width = 900
s_height = 600


def test_ball_init():
    ball= Ball()

    assert abs(ball.ball_xspeed)== 0.4
    assert abs(ball.ball_yspeed)== 0.5

    assert ball.ball_width== 15
    assert ball.ball_height== 15

    assert ball.ball_x== (s_width / 2 - ball.ball_width / 2)
    assert ball.ball_y== (s_height / 2 - ball.ball_height / 2)


def test_ball_movement():
    ball= Ball()

    initial_x= ball.ball_x
    initial_y= ball.ball_y
    ball.ball_xspeed= 1.0 
    ball.ball_yspeed= 1.0

    ball.ball_x += ball.ball_xspeed
    ball.ball_y += ball.ball_yspeed

    assert ball.ball_x== initial_x + 1.0
    assert ball.ball_y== initial_y + 1.0


def test_cpu_initialization():
    cpu= CPU()

    assert cpu.cpu_width== 10
    assert cpu.cpu_height== 80
    assert cpu.cpu_x== 840
    assert cpu.cpu_y== (s_height / 2 - cpu.cpu_height / 2)


def test_player_initialization():
    player = Player()

    assert player.player_width== 10
    assert player.player_height== 80
    assert player.player_x== 40
    assert player.player_y== (s_height / 2 - player.player_height / 2)


def test_cpu_movement():
    cpu= CPU()

    ball_x= 850
    ball_y= 300
    cpu.cpu_y= 290

    cpu.cpu_movement(ball_x, ball_y, 0.4)

    assert cpu.cpu_y > 290

    cpu.cpu_y= 0
    cpu.cpu_movement(ball_x, -10, 0.4)
    assert cpu.cpu_y== 0 


def test_player_movement():
    player= Player()

    player.player_y= 200
    pygame.key.set_mods(pygame.K_w)
    player.player_movement()
    assert player.player_y < 200 

    player.player_y= 500
    pygame.key.set_mods(pygame.K_s)
    player.player_movement()
    assert player.player_y > 500 

    player.player_y= 0
    player.player_movement()
    assert player.player_y== 0  

    player.player_y= s_height - player.player_height
    player.player_movement()
    assert player.player_y== s_height - player.player_height 