# imports
from scipy import interpolate
import threading
from random import randint, random, uniform, choice
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
import pyautogui
import math
import pyautogui as pag
import scipy.interpolate
import pytweening
import time
from time import sleep
import sys

pyautogui.FAILSAFE = True #failsafe, go to 0, 0

s_key = KeyCode(char='s')  # start and stop key
e_key = KeyCode(char='e')  # exit key


#bounds on screen
start_x = 588
end_x = 1335
start_y = 300
end_y = 1009


def getPos(): #gets the positions
    img = pyautogui.screenshot()
    pix = img.load()

    pos = [] #list of a collection of pixels, all next to each other and have the same color

    for i in range(start_x, end_x):
        for j in range(start_y, end_y):
            pixel = pix[i, j]
            if pixel == (255,219,195): #a target pixel
                has_home = -1 #see if it belongs to a collection previously found
                for z in range(0, len(pos)): #checks every collection
                    collection = pos[z]
                    if abs(collection[len(collection) - 1][0] - i) <= 2 or abs(collection[len(collection) - 1][1] - j) <= 2: #belongs(in proximity)
                        has_home = z #has a home
                        break
                if has_home >= 0:
                    pos[has_home].append([i,j]) #adds to collection
                else:
                    pos.append([[i,j]]) #creates new collection

    allPos = []

    for i in range(0, len(pos)): #gets the near center of every collection
        collection = pos[i]
        middle = int((len(collection) / 2))
        allPos.append(collection[middle])  # adds all

    return allPos

pag.MINIMUM_DURATION = 0.01
pag.MINIMUM_SLEEP = 0.01

def moveThrough(points, duration=0.1, neonate=pytweening.easeInOutQuad):
    n = len(points)
    if n == 0: raise Exception("No points to move through")
    elif n == 1: moveThrough([pag.position(), points[0]], duration); return
    elif n == 2: interpkind = "linear"
    elif n == 3: interpkind = "quadratic"
    else: interpkind = "cubic"

    ts = [i/(n-1) for i in range(n)]
    interp = scipy.interpolate.interp1d(ts, points, axis=0, kind=interpkind, assume_sorted=True)
    steps = duration / pag.MINIMUM_SLEEP
    for i in range(int(steps)):
        x, y = interp(neonate(i / (steps-1)))
        x, y = (int(round(x)), int(round(y)))
        if last_check(points, x, y):
            RND = 5
            # RND_duration = duration * 2
            # RND_steps = RND_duration / pag.MINIMUM_SLEEP
            # x, y = interp(neonate(i / (RND_steps - 1)))
            # x, y = (int(round(x)), int(round(y)))
            x = x + randint(-RND, RND)
            y = y + randint(-RND, RND)

        pag.platformModule._moveTo(x, y)
        sleep(pag.MINIMUM_SLEEP)


time_diff = 0.450
blacklist = [[0, 0], [0, 0], [0, 0]]


def last_check(points, x, y):
    finished_number = 0
    z = [x, y]
    for i in points:
        z_number = -1
        finished_number += 1
        for y in i:
            z_number += 1
            difference = y - z[z_number]
            if 1 > difference > -1:
                # print(f"{points} RND no")
                return False

            if finished_number == len(blacklist):
                # print(f"{points} RND pass")
                return True


def blacklist_check(blacklist, z):
    finished_number = 0
    for i in blacklist:
        z_number = -1
        finished_number += 1
        for y in i:
            z_number += 1
            difference = y - z[z_number]
            if 4 > difference > -4:
                return False

            if finished_number == len(blacklist):
                return True


# mouse click code
class Bot(threading.Thread):  # class that extends threading, allows us to mouse click
    def __init__(self):
        super(Bot, self).__init__()
        self.running = False
        self.program_running = True

    def start_clicking(self):  # start clicking
        print("Started")
        self.running = True

    def stop_clicking(self):  # stop clicking
        self.running = False
        print("Paused")

    def exit(self):  # exit the program
        print("Exiting")
        self.stop_clicking()
        self.program_running = False
        quit()
        exit()
        sys.exit("Exiting by 'e'")

    def run(self):  # running
        global time_diff
        while self.program_running:  # program isn't exited
            while self.running: #while the program is running
                pos = getPos() #gets the positions needed to be clicked
                for z in pos:
                    pos.remove(z)
                    if blacklist_check(blacklist, z):
                        first = True
                        if first:
                            tempz1, tempz2 = pag.position()
                            old_coordinates = [tempz1, tempz2]
                            first = False
                        else:
                            old_coordinates = [z[0], z[1]]
                        if len(old_coordinates) != 0:
                            distance = math.dist(old_coordinates, z)
                            random_duration = distance / 1800
                            if random_duration < 0.13:
                                random_duration = 0.13
                        else:
                            random_duration = 0.12

                        offset0 = randint(-4, 4)
                        offset1 = randint(-4, 4)
                        chance = randint(0, 100)
                        if chance > 95:
                            offset0 = offset0 + choice([-15, 15])
                            offset1 = offset1 + choice([-15, 15])
                            print("Chance = True")
                        else:
                            blacklist.append(z)
                            blacklist.pop(0)

                        z[0] = z[0] + offset0
                        z[1] = z[1] + offset1

                        if z[0] < old_coordinates[0]:
                            curve_offset0 = -35
                        else:
                            curve_offset0 = 35
                        if z[1] < old_coordinates[1]:
                            curve_offset1 = -35
                        else:
                            curve_offset1 = 35

                        z_curve = [z[0] + curve_offset0, z[1] + curve_offset1]

                        points = [old_coordinates, z_curve, z]
                        # sleep(0.05)
                        moveThrough(points, duration=random_duration)

                        mouse.click(Button.left, count = 1)

                        if z == 3:
                            getPos()
                    # time.sleep(0.05) #delay in between, needed big time because the actual website must register the click
            time.sleep(0.00001)  # delay


#creates everything
mouse = Controller()  # the mouse
click_thread = Bot()  # thread
click_thread.start()  # starts the thread


#for stopping and starting

def key_press(key):  # key press
    if key == s_key:
        if click_thread.running:
            click_thread.stop_clicking()  # stop
        else:
            click_thread.start_clicking()  # start
    elif key == e_key:  # exit
        click_thread.exit()
        listener.stop()


with Listener(on_press=key_press) as listener:  # listener
    listener.join()
