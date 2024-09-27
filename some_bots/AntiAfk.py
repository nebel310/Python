import random as rn
import time
from pyautogui import *


def move_mouse():
    time.sleep(0.2)
    
    rx = [x for x in range(80, 563)]
    ry = [y for y in range(80, 563)]
    
    x = rn.choice(rx)
    y = rn.choice(ry)
    move(x, y, 0.5)
    time.sleep(1)


def walk():
    time.sleep(0.2)
    
    keys = ['w', 'a', 's', 'd']
    r = [t for t in range(1, 4)]
    
    v = rn.choice([True, False])
    v = True
    if v == True:
        keyDown('shift')
        key = rn.choice(keys)
        t = rn.choice(r)
        keyDown(key)
        time.sleep(t)
        keyUp(key)
        keyUp('shift')
    else:
        key = rn.choice(keys)
        t = rn.choice(r)
        keyDown(key)
        time.sleep(t)
        keyUp(key)


def oneShoot():
    time.sleep(0.2)
    
    press('q')
    time.sleep(0.5)
    press('1')
    time.sleep(1.1)
    
    values = [i for i in range(1, 5)]
    
    a = rn.choice(values)
    while a != 0:
        click()
        time.sleep(1.5)
        a -= 1


while True:
    walk()
    oneShoot()
    press('4')
    time.sleep(0.5)
    press('g')