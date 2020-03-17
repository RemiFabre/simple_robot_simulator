#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, math, pygame
import pygame.draw
from pygame.locals import *
import sys
import os
import copy
import motor
import model
from constants import *


class SimpleRobotControl:
    def __init__(self):
        self.control_modes = [XY_GOAL, WHEEL_CONTROL]
        self.control_mode_id = 0
        self.m = model.Model()
        self.m.x_goal = 50
        self.m.y_goal = 50
        self.mode = self.get_mode()
        self.clock = pygame.time.Clock()
        self.t0 = pygame.time.get_ticks() / 1000.0
        # initialize and prepare screen
        pygame.init()
        self.screen = pygame.display.set_mode(WINSIZE)
        pygame.display.set_caption("Cubi simulation")
        # Font init
        self.font = pygame.font.SysFont("monospace", 30)
        self.screen.fill(BLACK)

    def get_mode(self):
        return self.control_modes[self.control_mode_id]

    def set_next_mode(self):
        self.control_mode_id = (self.control_mode_id + 1) % len(self.control_modes)

    def draw_robot(self, m=None, fake=False):
        if m == None:
            m = self.m
        # Usually, we have X in front of us and Y to the left. Let's keep that : y = -y, theta = theta-pi/2
        center_pos = [int(m.x + WINCENTER[0]), int(-m.y + WINCENTER[1])]
        color = CENTER_COLOR
        size = CENTER_SIZE
        if fake:
            color = FAKE_COLOR
            size = int(FAKE_SIZE)
        pygame.draw.circle(self.screen, color, center_pos, int(size), 0)

        r = int(m.l / 2)
        theta = m.theta - math.pi / 2
        wheel_pos = [
            int(center_pos[0] + r * math.cos(theta)),
            int(center_pos[1] - r * math.sin(theta)),
        ]
        color = WHEEL_COLOR
        size = WHEEL_SIZE
        if fake:
            color = FAKE_COLOR
            size = FAKE_SIZE
        pygame.draw.circle(self.screen, color, wheel_pos, int(size), 0)

        wheel_pos = [
            int(center_pos[0] - r * math.cos(theta)),
            int(center_pos[1] + r * math.sin(theta)),
        ]
        pygame.draw.circle(self.screen, color, wheel_pos, int(size), 0)

    def draw_goal(self):
        # Usually, we have X in front of us and Y to the left. Let's keep that : y = -y, theta = theta-pi/2
        center_pos = [
            int(self.m.x_goal + WINCENTER[0]),
            int(-self.m.y_goal + WINCENTER[1]),
        ]
        pygame.draw.circle(self.screen, GOAL_COLOR, center_pos, int(GOAL_SIZE), 0)

    def draw_state(self):
        self.draw_robot()
        self.draw_goal()

    def play(self):
        print("Current mode is '{}'".format(self.get_mode()))
        while True:
            mode = self.get_mode()
            # 'e' for 'event'
            for e in pygame.event.get():
                if e.type == QUIT:
                    sys.exit()
                elif e.type == KEYDOWN:
                    key = e.dict["unicode"]
                    if key == "q":
                        print("Rage quit!")
                        return 0
                    if key == "r":
                        None
                    if e.key == pygame.K_SPACE:
                        self.set_next_mode()
                    if e.key == pygame.K_RETURN:
                        self.m.theta = float(raw_input("theta = "))
                    if e.key == pygame.K_UP:
                        self.m.m1.speed = self.m.m1.speed + WHEEL_SPEED_INC
                    if e.key == pygame.K_DOWN:
                        self.m.m1.speed = self.m.m1.speed - WHEEL_SPEED_INC
                    if e.key == pygame.K_RIGHT:
                        self.m.m2.speed = self.m.m2.speed + WHEEL_SPEED_INC
                    if e.key == pygame.K_LEFT:
                        self.m.m2.speed = self.m.m2.speed - WHEEL_SPEED_INC
                elif e.type == pygame.MOUSEMOTION:
                    mx, my = e.pos
                elif e.type == MOUSEBUTTONDOWN and e.button == 1:
                    self.m.x_goal = mx - WINCENTER[0]
                    self.m.y_goal = -(my - WINCENTER[1])

            self.screen.fill(BLACK)
            if mode == XY_GOAL:
                self.asserv()
            elif mode == WHEEL_CONTROL:
                None
            else:
                print("ERROR: mode '{}' is unknown".format(mode))
                sys.exit()
            self.m.update(1)

            # Creating a fake robot to trace the future :)
            fake_m = copy.deepcopy(self.m)
            for i in range(20):
                if mode == XY_GOAL:
                    self.asserv(m=fake_m)
                fake_m.update(20)
                self.draw_robot(m=fake_m, fake=True)

            self.draw_state()
            # print(self.m)
            text = self.font.render("Cubi !", 1, gold)
            self.screen.blit(text, [0, 0])

            t = pygame.time.get_ticks() / 1000.0 - self.t0
            time_pos = [20, 30]

            try:
                # Erasing the previous text
                time_text.fill(BLACK)
                self.screen.blit(time_text, time_pos)
            except Exception:
                None
            # Writing new text
            str_time = "{0:.2f}".format(t)
            time_text = self.font.render("Time : " + str_time, 1, (0, 150, 0))
            self.screen.blit(time_text, time_pos)

            pygame.display.update()
            # That juicy 60 Hz :D
            self.clock.tick(60)

    def asserv(self, m=None):
        if m == None:
            m = self.m
        distance = math.sqrt(
            (m.x_goal - m.x) * (m.x_goal - m.x) + (m.y_goal - m.y) * (m.y_goal - m.y)
        )
        if distance < XY_TOL:
            # Close enough
            m.m1.speed = 0
            m.m2.speed = 0
            return

        # The angle goal depends on the X Y goals
        dy = m.y_goal - m.y
        dx = m.x_goal - m.x
        if not (dx == 0 and dy == 0):
            m.theta_goal = math.atan2(dy, m.x_goal - m.x)

        # TODO implement go backwards when (theta_goal - theta) > pi. And debug this.
        # Turn asserv
        err = self.angle_diff(m.theta, m.theta_goal)
        # print("***err = {}, goal = {}, theta = {}".format(err*180/math.pi, m.theta_goal*180/math.pi, m.theta*180/math.pi))
        # model.acc += turni * err;
        # _limit(&model.acc, turnacc);
        p_contribution = TURN_P * err

        """
        if ((p_contribution < 0 && model.acc >= 0) || (p_contribution > 0 && model.acc <= 0)) {
            // Astuce !
            model.acc = 0;
        }
        """
        local_turn = p_contribution + m.acc

        local_speed = 0
        # linear speed asserv
        # model.speed_acc += speedi * distance;
        # _limit(&model.acc, speedacc);
        p_contribution = SPEED_P * distance

        """
        if ((p_contribution < 0 && model.speed_acc >= 0) || (p_contribution > 0 && model.speed_acc <= 0)) {
            // Astuce !
            model.speed_acc = 0;
        }
        """

        local_speed = p_contribution + m.speed_acc

        m1_speed, m2_speed = m.ik(local_speed, local_turn)
        m.m1.speed = m1_speed
        m.m2.speed = m2_speed

    # Returns the smallest distance between 2 angles
    def angle_diff(self, a, b):
        d = a - b
        d = ((d + math.pi) % (2 * math.pi)) - math.pi
        return d


def main():
    robot = SimpleRobotControl()

    result = robot.play()

    sys.exit()


# if python says run, then we should run
if __name__ == "__main__":
    main()
