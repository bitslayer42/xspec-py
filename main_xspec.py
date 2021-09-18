import pygame
import os
import math
import random
from matrix import matrix_multiplication
from math import acos,atan2,sqrt,cos,sin
fieldOfView = 0.63
# from icosphere import points

os.environ["SDL_VIDEO_CENTERED"]='1'  # Center window
black, white, blue  = (20, 20, 20), (230, 230, 230), (0, 154, 255)
scr_width, scr_height = 1680, 1050

pygame.init()
pygame.display.set_caption("Xspec")
screen = pygame.display.set_mode((scr_width, scr_height))
clock = pygame.time.Clock()
fps = 60

angle = 0
scr_center = [scr_width//2, scr_height//2]
scale = 600
speed = 0.01
points = []

for i in range(-5,5):
    for j in range(-5,5):
        for k in range(-5,5):
            points.append([[i], [j], [k]])



def connect_point(i, j, projected_points):
    a = projected_points[i]
    b = projected_points[j]
    pygame.draw.line(screen, black, (a[0], a[1]), (b[0], b[1]), 1)

def getCameraCoords(x,y,z):
    x1 = (acos(-(z / sqrt(x**2 + y**2 + z**2)))) * fieldOfView * cos( atan2(y,x) )
    y1 = (acos(-(z / sqrt(x**2 + y**2 + z**2)))) * fieldOfView * sin( atan2(y,x) )
    return [x1,y1]

run = True
while run:
    clock.tick(fps)
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    index = 0
    projected_points = [j for j in range(len(points))]

    rotation_x = [[1, 0, 0],
                  [0, math.cos(angle), -math.sin(angle)],
                  [0, math.sin(angle), math.cos(angle)]]

    rotation_y = [[math.cos(angle), 0, -math.sin(angle)],
                  [0, 1, 0],
                  [math.sin(angle), 0, math.cos(angle)]]

    rotation_z = [[math.cos(angle), -math.sin(angle), 0],
                  [math.sin(angle), math.cos(angle), 0],
                  [0, 0 ,1]]

    for point in points:
        rotated_2d = matrix_multiplication(rotation_y, point)
        rotated_2d = matrix_multiplication(rotation_x, rotated_2d)
        rotated_2d = matrix_multiplication(rotation_z, rotated_2d)
        # distance = 5
        # z = 1/(distance - rotated_2d[2][0])
        # projection_matrix = [[z, 0, 0],
        #                     [0, z, 0]]
        # projected_2d = matrix_multiplication(projection_matrix, rotated_2d)
        # x = int(projected_2d[0][0] * scale) + scr_center[0]
        # y = int(projected_2d[1][0] * scale) + scr_center[1]
        
        projected_2d = getCameraCoords(rotated_2d[0][0],rotated_2d[1][0],rotated_2d[2][0]-6.1)
        x = int(projected_2d[0] * scale) + scr_center[0]
        y = int(projected_2d[1] * scale) + scr_center[1]

        projected_points[index] = [x, y]
        pygame.draw.circle(screen, blue, (x, y), 4)
        index += 1
    #draw edges
    # for m in range(len(points)):
    #     connect_point(m, random.randint(0, len(points)-1), projected_points)

    angle += speed
    pygame.display.update()

pygame.quit()
