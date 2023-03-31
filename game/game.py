import sys

import matplotlib as mpl
import pygame

from problem import Problem
from ucs import UniformCostSearch
from bts import BacktrackingS
from dfs import DepthFirstSearch
from bfs import BreadthFirstSearch
from dfsi import DepthFirstSearchIterative
from astar import AstarSearch
from dp import DynamicProgrammingSearch

cmap = mpl.colormaps["inferno"]
hcells = 15
vcells = 15
cellw = 60
cellh = 60


class Button:
    def __init__(self, path, width, height, x, y):
        self.image = pygame.image.load(path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.hover = False
        self.enabled = True
        self.active = False
        self.rect = pygame.Rect(x, y, width, height)

    def setEnabled(self, enabled):
        self.enabled = bool(enabled)

    def setActive(self, active):
        self.active = bool(active)

    def isInside(self, x, y):
        insideX = self.x <= x <= self.x + self.width
        insideY = self.y <= y <= self.y + self.height
        return self.enabled and insideX and insideY

    def handleHover(self, x, y):
        if self.enabled and self.isInside(x, y):
            self.hover = True
        else:
            self.hover = False

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (233, 227, 27), self.rect)  # #e9e31b
        elif not self.enabled:
            pygame.draw.rect(screen, (175, 187, 210), self.rect)  # #afbbd2
        elif self.hover:
            pygame.draw.rect(screen, (96, 145, 236), self.rect)  # #6091ec
        else:
            pygame.draw.rect(screen, (76, 93, 125), self.rect)  # #4c5d7d
        screen.blit(self.image, (self.x, self.y))


class Game:
    def __init__(self):
        pygame.init()
        w = max(hcells * cellw, 640 + 32)
        h = (vcells * cellh) + 32
        self.screen = pygame.display.set_mode((w, h))
        self.problem = Problem(hcells, vcells)
        self.clock = pygame.time.Clock()
        self.bg_color = pygame.Color((76, 93, 125))  # #4c5d7d
        self.mousex = 0
        self.mousey = 0

        self.pen_btn = Button("./assets/pen.png", 32, 32, 0 * 32, 0)
        self.eraser_btn = Button("./assets/eraser.png", 32, 32, 1 * 32, 0)
        self.play_btn = Button("./assets/play.png", 32, 32, 2 * 32, 0)
        self.pause_btn = Button("./assets/pause.png", 32, 32, 3 * 32, 0)
        self.step_btn = Button("./assets/step.png", 32, 32, 4 * 32, 0)
        self.stop_btn = Button("./assets/stop.png", 32, 32, 5 * 32, 0)
        self.trash_btn = Button("./assets/trash.png", 32, 32, 6 * 32, 0)
        self.bt_btn = Button("./assets/route-bt.png", 64, 32, 7 * 32, 0)
        self.dfs_btn = Button("./assets/route-dfs.png", 64, 32, 7 * 32 + 64, 0)
        self.bfs_btn = Button("./assets/route-bfs.png", 64, 32, 7 * 32 + 2 * 64, 0)
        self.dfsid_btn = Button("./assets/route-dfsid.png", 64, 32, 7 * 32 + 3 * 64, 0)
        self.dp_btn = Button("./assets/route-dp.png", 64, 32, 7 * 32 + 4 * 64, 0)
        self.ucs_btn = Button("./assets/route-ucs.png", 64, 32, 7 * 32 + 5 * 64, 0)
        self.astar_btn = Button("./assets/route-astar.png", 64, 32, 7 * 32 + 6 * 64, 0)

        self.pause_btn.setEnabled(False)
        self.bt_btn.setEnabled(True)
        self.dfs_btn.setEnabled(True)
        self.bfs_btn.setEnabled(True)
        self.dfsid_btn.setEnabled(True)
        self.dp_btn.setEnabled(True)
        self.astar_btn.setEnabled(True)

        self.buttons = [
            self.pen_btn,
            self.eraser_btn,
            self.play_btn,
            self.pause_btn,
            self.step_btn,
            self.stop_btn,
            self.trash_btn,
            self.bt_btn,
            self.dfs_btn,
            self.bfs_btn,
            self.dfsid_btn,
            self.dp_btn,
            self.ucs_btn,
            self.astar_btn,
        ]

        self.algorithms = [
            (self.bt_btn, BacktrackingS),
            (self.dfs_btn, DepthFirstSearch),
            (self.bfs_btn, BreadthFirstSearch),
            (self.dfsid_btn, DepthFirstSearchIterative),
            (self.dp_btn, DynamicProgrammingSearch),
            (self.ucs_btn, UniformCostSearch),
            (self.astar_btn, AstarSearch),
        ]

        self.algorithmButton = None
        self.algorithm = None
        self.selectAlgorithm(self.ucs_btn)

        self.tool = "pen"
        self.pen_btn.setActive(True)

        self.running = False
        self.minCost = 0
        self.maxCost = 0
        self.path = []

    def selectAlgorithm(self, btn):
        btn.setActive(True)
        self.algorithmButton = btn
        for btn2, _ in self.algorithms:
            if btn is btn2:
                continue
            btn2.setActive(False)
        for btn2, cons in self.algorithms:
            if btn2 is btn:
                self.algorithm = cons(self.problem)
        self.path = []

    def shutdown(self):
        pygame.quit()
        sys.exit()

    def handle_click(self):
        x = self.mousex
        y = self.mousey
        if self.pen_btn.isInside(x, y):
            self.tool = "pen"
            self.pen_btn.setActive(True)
            self.eraser_btn.setActive(False)
        if self.eraser_btn.isInside(x, y):
            self.tool = "eraser"
            self.pen_btn.setActive(False)
            self.eraser_btn.setActive(True)
        if self.play_btn.isInside(x, y):
            self.play_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.step_btn.setEnabled(False)
            self.running = True
        if self.pause_btn.isInside(x, y):
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.step_btn.setEnabled(True)
            self.running = False
        if self.step_btn.isInside(x, y):
            self.running = False
            self.path = self.algorithm.step()
        if self.stop_btn.isInside(x, y):
            self.running = False
            self.play_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            self.step_btn.setEnabled(True)
            self.selectAlgorithm(self.algorithmButton)
            self.minCost = 0
            self.maxCost = 0
            self.path = []
        if self.trash_btn.isInside(x, y):
            self.problem = Problem(hcells, vcells)

        for btn, _ in self.algorithms:
            if btn.isInside(x, y):
                self.selectAlgorithm(btn)

        inGridX = 0 <= self.mousex <= hcells * cellw
        inGridY = 0 <= self.mousey - 32 <= vcells * cellh
        if inGridX and inGridY:
            gridx = self.mousex // cellw
            gridy = (self.mousey - 32) // cellh
            if self.tool == "pen":
                self.problem.blockState((gridx, gridy))
            if self.tool == "eraser":
                self.problem.unblockState((gridx, gridy))

    def handle_click_drag(self):
        inGridX = 0 <= self.mousex <= hcells * cellw
        inGridY = 0 <= self.mousey - 32 <= vcells * cellh
        if inGridX and inGridY:
            gridx = self.mousex // cellw
            gridy = (self.mousey - 32) // cellh
            if self.tool == "pen":
                self.problem.blockState((gridx, gridy))
            if self.tool == "eraser":
                self.problem.unblockState((gridx, gridy))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return self.shutdown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.shutdown()
            if event.type == pygame.MOUSEMOTION:
                (x, y) = pygame.mouse.get_pos()
                self.mousex = x
                self.mousey = y
                (clicked, _, _) = pygame.mouse.get_pressed()
                if clicked:
                    self.handle_click_drag()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click()

    def update(self):
        for btn in self.buttons:
            btn.handleHover(self.mousex, self.mousey)
        if self.running:
            self.path = self.algorithm.step()
        self.clock.tick(30)

    def draw(self):
        self.screen.fill(self.bg_color)
        for btn in self.buttons:
            btn.draw(self.screen)
        for cellx in range(hcells):
            x = cellx * cellw
            for celly in range(vcells):
                y = celly * cellh + 32
                if self.problem.isBlocked((cellx, celly)):
                    pygame.draw.rect(
                        self.screen, (0, 0, 0), pygame.Rect(x, y, cellw, cellh)
                    )
                    continue
                cost = self.algorithm.stateCost((cellx, celly))
                if cost is None:
                    pygame.draw.rect(
                        self.screen, (255, 255, 255), pygame.Rect(x, y, cellw, cellh)
                    )
                else:
                    self.minCost = min(cost, self.minCost)
                    self.maxCost = max(cost, self.maxCost)
                    v = (cost - self.minCost) / (self.maxCost - self.minCost + 1)
                    color = cmap(1.0 - 0.8 * v + 0.1)[:-1]
                    color = tuple(int(255 * c) for c in color)
                    pygame.draw.rect(
                        self.screen, color, pygame.Rect(x, y, cellw, cellh)
                    )

        inGridX = 0 <= self.mousex <= hcells * cellw
        inGridY = 0 <= self.mousey - 32 <= vcells * cellh
        if inGridX and inGridY:
            pygame.draw.rect(
                self.screen,
                (233, 227, 27),
                pygame.Rect(
                    cellw * (self.mousex // cellw),
                    cellh * ((self.mousey - 32) // cellh) + 32,
                    cellw,
                    cellh,
                ),
                2,
            )
        (cellx, celly) = self.problem.startState()
        pygame.draw.rect(
            self.screen,
            (32, 227, 36),
            pygame.Rect(
                cellw * cellx,
                cellh * celly + 32,
                cellw,
                cellh,
            ),
            3,
        )

        (cellx, celly) = self.problem.endState()
        pygame.draw.rect(
            self.screen,
            (63, 141, 65),
            pygame.Rect(
                cellw * cellx,
                cellh * celly + 32,
                cellw,
                cellh,
            ),
            3,
        )

        if len(self.path) > 1:
            pygame.draw.lines(
                self.screen,
                (32, 227, 36),
                False,
                [
                    (x * cellw + cellw // 2, y * cellh + 32 + cellh // 2)
                    for (x, y) in self.path
                ],
                3,
            )

        pygame.display.flip()
