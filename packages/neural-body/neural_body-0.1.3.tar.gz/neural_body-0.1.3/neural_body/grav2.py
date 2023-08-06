import pygame
import sys
import pandas as pd
import numpy as np
from neural_body.BenrulesRealTimeSim_v3 import BenrulesRealTimeSim
import os
import time
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import math

# Set audio driver to avoid ALSA errors
os.environ['SDL_AUDIODRIVER'] = 'dsp'

# Check if DISPLAY has been detected.  If not, assume WSL with pycharm and grab
# display connection.
# Only needed for launching from pycharm
try:
    print(os.environ["DISPLAY"])
except KeyError as error:
    # If at this point, DISPLAY doesn't exist and needs to be set.
    line_list = []
    with open('/etc/resolv.conf') as f:
        for line in f:
            pass
        last_line = line
        line_list = last_line.split(' ')
        f.close()
    # Set the display
    os.environ["DISPLAY"] = line_list[-1].rstrip() + ":0"

pygame.init()


def main():
    """
        Main function of the program, where all of the fun begins. Basic
        environment attributes are set such as the screen dimensions, number
        of planets (total on screen, main view plus inner planet view), the
        planet tail length, and the program clock
    """
    # Set screen size and launch window
    scr_width = 1000
    scr_height = 700
    screen = pygame.display.set_mode((scr_width, scr_height))

    # Setting caption at top of window
    pygame.display.set_caption("AstroGators - Neural Body Simulator")

    # Creating clock variable.
    # Helps with tracking time and managing framerate.
    clock = pygame.time.Clock()

    # trackers for the planet trails
    num_planets = 13
    tail_length = 150

    pygame.draw.rect(screen,
                     (255, 255, 255),
                     pygame.Rect(
                         int(250),
                         int(260),
                         int(500),
                         int(140)
                     ),
                     2)
    text_handler(screen,
                 'Loading, Please Wait...',
                 int(305),
                 int(310),
                 35,
                 255)
    pygame.display.update(pygame.Rect(
        int(250),
        int(260),
        int(502),
        int(142)
    ))

    orbits(screen, num_planets, tail_length, clock, scr_width, scr_height)


def sun(screen, x, y):
    """
        Function to place the sun image on the screen
        A simple function for loading the sun image and placing it on the
        screen at a given coordinate. The size is static
        **List of input parameters:**
        :param screen: window created by pygame used to display application
        :param x: the integer x-coordinate pixel value where the sun should be
            placed
        :param y: the integer y-coordinate pixel value where the sun should be
            placed
    """
    current_working_directory = os.path.dirname(os.path.realpath(__file__))
    sun_img = pygame.image.load(current_working_directory + '/img/sun.png')
    sun_img = pygame.transform.scale(sun_img, (10, 10))
    screen.blit(sun_img, (x, y))


def orbits(screen, num_planets, tail_length, clock, scr_width, scr_height):
    """
        Function that runs the simulation. Handles function calls to display
        all visual elements and determine orbital locations.
        This class operates as the master of the program, containing the
        infinite loop that the program relies on in order to function. All
        important interactions between the various components of the program
        are routed through this class, and many vital mathematic operations
        reside within it. Because global variables are not used, this class
        acts as an intermediate to pass variables as parameters and receive
        them back as returned values.
        Methods used:
        - pygame.draw.circle - replicates the planets drawn on the screen
        - text_handler - names each of the replicated planets
        - BenrulesRealTimeSim - creates a real time simulator of the sun,
          planets, and pluto.
        - pygame.image.load - loads an image from a file
        - pygame.transform.scale - scales an image to a specified width and
          height
        - get_next_sim_state_v2 - updates the dictionary of current simulation
          data to the next time_step
        - screen.fill - changes the color of the entire pygame canvas
        - screen.blit - method to display a supplied image on the scren as
          output
        - pygame.draw.line - pygame method used to draw a line, here is used to
          draw the trails
        - pygame.draw.circle - pygame method used to draw circles, here used to
          represent the planets
        - current_time_step - Setter function used to change the point in time
          of the simulation
        - pygame.event.get() - method to handle a user interaction event
        - pygame.quit() - Pygame method used to quit running pygame
        - sys.exit() - Method used to exit the program
        - pygame.display.flip() - method to refresh the pygame display
        - clock.tick(60) - method used to set a frame rate of 60 frames per
          second
        **List of input parameters:**
        :param num_planets: Int representing the number of planet bodies on the
            entire screen, inner planets view + solar system view
        :param tail_length: Int representing the length of the tail to follow
            behind the orbiting planets
        :param clock: a local variable storing a copy of the pygame clock time
        :param screen: window created by pygame used to display application
        :param scr_width: An in that represents the width of the screen
        :param scr_height: An int that represents the height of the screen
        **List of internal variables:**
        - input_text - string containing user-entered filepath for a new init
          file
        - past_input - string used to store input_text between when it is reset
          and when it needs to be used to call a file
        - textbox_active - Int that determines whether the input textbox is to
          be displayed, 0 if no, 1 if yes
        - pause - An int that specifies whether or not the simulation runs, 0
          means it's running, 1 means it is paused
        - view - An int that determines what view is displayed, 0 for overhead
          view, 1 for side view
        - speed - An int that determines the speed of the simulation, 1x, 2x,
          4x, etc
        - click_now - An int that determines whether the mouse is being clicked
          , 0 means no click, 1 means click
        - input_active - An int that determines whether the file input text box
          shows, 0, means no show, 1 means it will show
        - nasa - String that activates pluto, Yes, means NASA is correct, and
          pluto is not a planet, No means NASA is incorrect and pluto is a
          planet
        - input2_active - An int that displays the travel to a day textbox, 0
          means no show, 1 means it shows
        - textbox2_active - An int that determines whether the travel to
          textbox is showing, 0 means no, 1 means yes
        - input2_text - String that determines what day will be traveled to
          after the travel to day is determined
        - zoom - Int used to scaled the planets to fit on the screen
        - zoom_factor - Int used to scale the zoom to give varying views of the
          solar system if changed
        - zoom_i - Int used to scale the inner planets coordinates to fit on
          the screen
        - num_planets - Number of total bodies being displayed on the screen,
          whole solar system view + inner planets view
        - time_step - Int used to determine length of time between
        - curr_time_step - Int that represents how many time steps have passed
          in the simulation
        - start_string - String containing the default path for an init file
        - simulation -  An object encompassing an n-body simulation that
          predicts a single body dependent on the state of all other simulated
          bodies in the system.
        - sunx - Int representing the x coordinate of the sun image
        - suny - Int representing the y coordinate of the sun image
        - sun_i_x - Int representing the x coordinate of the sun image for the
          inner planets view
        - sun_i_y - Int representing the x coordinate of the sun image for the
          inner planets view
        - sun_img - Object used to hold the image of the sun that is printed to
          the screen
        - current_positions - Dictionary that contains the name and a list of
          x, y coordinates for each non-predicted planet
        - current_positions - Dictionary that contains the name and list of
          x, y coordinates for the predicted planet(s)
        - x1 - X coordinate relative to the printed sun image for Mercury
        - xi1 - X coordinate relative to the printed sun image for Mercury for
          the inner planets view
        - y1 - Y coordinate relative to the printed sun image for Mercury
        - yi1 - Y coordinate relative to the printed sun image for Mercury for
          the inner planets view
        - x2 - X coordinate relative to the printed sun image for Venus
        - xi2 - X coordinate relative to the printed sun image for Venus for
          the inner planets view
        - y2 - Y coordinate relative to the printed sun image for Venus
        - yi2 - Y coordinate relative to the printed sun image for Venus for
          the inner planets view
        - x3 - X coordinate relative to the printed sun image for Earth
        - xi3 - X coordinate relative to the printed sun image for Earth for
          the inner planets view
        - y3 - Y coordinate relative to the printed sun image for Earth
        - yi3 - Y coordinate relative to the printed sun image for Earth for
          the inner planets view
        - x4 - X coordinate relative to the printed sun image for Mars
        - xi4 - X coordinate relative to the printed sun image for Mars for
          the inner planets view
        - y4 - Y coordinate relative to the printed sun image for Mars
        - yi4 - X coordinate relative to the printed sun image for Mars for
          the inner planets view
        - x5 - X coordinate relative to the printed sun image for Jupiter
        - y5 - Y coordinate relative to the printed sun image for Jupiter
        - x6 - X coordinate relative to the printed sun image for Saturn
        - y6 - Y coordinate relative to the printed sun image for Saturn
        - x7 - X coordinate relative to the printed sun image for Uranus
        - y7 - Y coordinate relative to the printed sun image for Uranus
        - x8 - X coordinate relative to the printed sun image for Pluto
        - y8 - Y coordinate relative to the printed sun image for Pluto
        - x9 - X coordinate relative to the printed sun image for Neptune
        - y9 - Y coordinate relative to the printed sun image for Neptune
        - x_track[] - List that contains the x coordinates for the planets to
          print the trails
        - y_track[] - List that contains the y coordinates fot the planets to
          print the trails
    """
    input_text = ""
    keep_running = True
    while keep_running:
        past_input = input_text
        textbox_active = 0
        input_text = ""
        simulation = None
        while (
                not (
                        input_text != "" and textbox_active == 0)) and \
                keep_running:

            pause = 0
            view = 0
            click_now = 0
            input_active = 0
            input2_active = 0
            textbox2_active = 0
            input2_text = ""
            pluto_real = 1
            nasa = "Yes"
            num_days = 0

            # Factor to setup view magnification for all planets.
            # Ranges from 15 to show all planets down to 1 to show only through
            # Mars.
            # Zooms are later used for scaling views from simulation space to
            # the view
            # of the inner planets and view of the outer planet.
            zoom_factor = 17
            zoom = 1000000000 * zoom_factor
            # Set inner planet view zoom
            zoom_i = 15000000000
            # Set time step and speed factor.
            # 1 is about a 35 second year (earth)
            speed = 1
            # time_step = 750000 * speed
            time_step = 86400 * speed
            # Keep track of how many simulation time steps have passed.
            curr_time_step = 0

            # Create simulation object that keeps track of simultion state and
            # predicts
            # position of satellite specified in config file.
            current_working_directory = os.path.dirname(
                os.path.realpath(__file__))
            start_string = current_working_directory + \
                           "/sim_configs/launch_sat_config.xlsx"
            if past_input != "":
                start_string = past_input
                del simulation
                pygame.draw.rect(screen,
                                 (0, 0, 0),
                                 pygame.Rect(
                                     int(scr_width / 2.6),
                                     int(scr_height / 2.7),
                                     int(scr_width / 1.8),
                                     int(scr_height / 5)
                                 ))
                pygame.draw.rect(screen,
                                 (255, 255, 255),
                                 pygame.Rect(
                                     int(scr_width / 2.6),
                                     int(scr_height / 2.7),
                                     int(scr_width / 1.8),
                                     int(scr_height / 5)
                                 ),
                                 2)
                text_handler(screen,
                             'Processing, Please wait',
                             int(scr_width / 2.2),
                             int(scr_height / 2.2),
                             35,
                             255)
                pygame.display.update(pygame.Rect(
                    int(scr_width / 2.6),
                    int(scr_height / 2.7),
                    int(scr_width / 1.8),
                    int(scr_height / 5)
                ))
            simulation = BenrulesRealTimeSim(
                sat_config_file=start_string
            )
            past_input = ""
            # Set offset so objects orbit the correct point.
            sunx = int(scr_width / 1.5)
            suny = int(scr_height / 2)

            sun_i_x = 185
            sun_i_y = 540
            sun_img = pygame.image.load(current_working_directory +
                                        '/img/sun.png')
            sun_img = pygame.transform.scale(sun_img, (10, 10))

            # Get next simulator state (positioning of all objects).
            current_positions, slow_down = simulation.get_next_sim_state_v2()
            x_track = [[0] * tail_length for i in
                       range(len(current_positions) + 5)]
            y_track = [[0] * tail_length for i in
                       range(len(current_positions) + 5)]

            while (
                    not (
                            input_text != "" and textbox_active == 0)) and \
                    keep_running:
                # the functions below will be replaced by neural net output
                curr_time_step += 1

                if speed == 0.5 and pause == 0:
                    # Only advance simulation every other time_step.
                    if curr_time_step % 2 == 0:
                        current_positions, slow_down = \
                            simulation.get_next_sim_state_v2()

                if speed == 1 and pause == 0:
                    # Advance simulation every time_step
                    current_positions, slow_down = \
                        simulation.get_next_sim_state_v2()

                if speed == 2 and pause == 0:
                    # Advance simulation twice per time_step
                    current_positions, slow_down = \
                        simulation.get_next_sim_state_v2()
                    current_positions, slow_down = \
                        simulation.get_next_sim_state_v2()

                if speed == 4 and pause == 0:
                    # Advance simulation 4 times every time_step
                    current_positions, slow_down = \
                        simulation.get_next_sim_state_v2()
                    current_positions, slow_down = \
                        simulation.get_next_sim_state_v2()
                    current_positions, slow_down = \
                        simulation.get_next_sim_state_v2()
                    current_positions, slow_down = \
                        simulation.get_next_sim_state_v2()

                # The simulator can burst for moments, but might need to slow
                # down if running out of output cache.
                if slow_down == True:
                    speed = 1

                # Set the framerate
                time.sleep(1 / simulation.max_fps)

                timePassed = simulation.current_time_step * simulation. \
                    time_step_duration
                num_days = int(timePassed / 86400)

                # Calculate the relative position of each body to the sun.
                # mercury

                scaled_x_pos = (current_positions[:, 0] - current_positions[0][
                    0]) / zoom + sunx
                scaled_y_pos = (current_positions[:, 1] - current_positions[0][
                    1]) / zoom + suny
                scaled_xi_pos = (current_positions[:, 0] -
                                 current_positions[0][
                                     0]) / zoom_i * 8 + sun_i_x
                scaled_yi_pos = (current_positions[:, 1] -
                                 current_positions[0][
                                     0]) / zoom_i * 8 + sun_i_y

                scaled_x_pos = scaled_xi_pos.astype(int)
                scaled_y_pos = scaled_yi_pos.astype(int)
                scaled_xi_pos = scaled_xi_pos.astype(int)
                scaled_yi_pos = scaled_yi_pos.astype(int)
                planet_colors = [(255, 136, 0), (196, 182, 108),
                                 (242, 197, 107),
                                 (11, 170, 255), (179, 67, 30), (252, 156, 66),
                                 (255, 194, 89), (108, 230, 219),
                                 (162, 141, 166), (108, 164, 204)]

                # Setting the stage.
                screen.fill((0, 0, 0))
                # Load and position the sun.
                screen.blit(sun_img, (int(scr_width / 1.5) - 5, int(scr_height
                                                                    / 2) - 5))
                screen.blit(sun_img, (sun_i_x - 5, sun_i_y - 5))

                # If simulation not paused, then continue with moving the
                # objects.
                if pause == 0:
                    # shifts all data points within the lists to the left to
                    # make room for the new trail data point
                    for j in range(0, len(scaled_x_pos)):
                        for i in range(0, tail_length - 1):
                            x_track[j][i] = x_track[j][i + 1]
                            y_track[j][i] = y_track[j][i + 1]
                        if abs(scaled_x_pos[j]) < 10000:
                            x_track[j][tail_length - 1] = scaled_x_pos[j]
                            y_track[j][tail_length - 1] = scaled_y_pos[j]

                sm_disp_left = int(scr_width / 60)
                sm_disp_right = int(scr_width / 60) + int(scr_width / 3.05)
                sm_disp_top = int(scr_height / 1.9)
                sm_disp_bottom = int(scr_height / 1.9) + int(scr_height / 2.23)

                lg_disp_left = int(scr_width / 2.8)
                lg_disp_right = int(scr_width / 2.8) + int(scr_width / 1.6)
                lg_disp_top = int(scr_width / 60)
                lg_disp_bottom = int(scr_width / 60) + int(scr_height / 1.05)

                int(scr_width / 2.8),
                int(scr_width / 60),
                int(scr_width / 1.60),
                int(scr_height / 1.05)

                if view == 0:
                    # Iterates through the 2D list and draws the planet's
                    # trails
                    for k in range(len(x_track)):
                        if k != 8 or nasa == "No":
                            for j in range(1, tail_length - 1):
                                i = tail_length - j
                                if x_track[k][j - 1] != 0:
                                    if (sm_disp_left <
                                        x_track[k][j] < sm_disp_right) and \
                                            (sm_disp_top <
                                             y_track[k][j] < sm_disp_bottom):
                                        pygame.draw.line(
                                            screen,
                                            (255 - 255 * (i / tail_length),
                                             255 - 255 * (i / tail_length),
                                             255 - 255 * (i / tail_length)),
                                            [x_track[k][j], y_track[k][j]],
                                            [x_track[k][j - 1],
                                             y_track[k][j - 1]],
                                            1)
                                    if (lg_disp_left <
                                        ((x_track[k][
                                              j] - sun_i_x) / 8 + sunx) <
                                        lg_disp_right) and \
                                            (lg_disp_top <
                                             ((y_track[k][
                                                   j] - sun_i_y) / 8 + suny) <
                                             lg_disp_bottom):
                                        pygame.draw.line(
                                            screen,
                                            (255 - 255 * (i / tail_length),
                                             255 - 255 * (i / tail_length),
                                             255 - 255 * (i / tail_length)),
                                            [(x_track[k][
                                                  j] - sun_i_x) / 8 + sunx, (
                                                     y_track[k][
                                                         j] - sun_i_y) / 8 +
                                             suny],
                                            [(x_track[k][
                                                  j - 1] - sun_i_x) / 8 + sunx,
                                             (y_track[k][
                                                  j - 1] - sun_i_y) / 8 +
                                             suny],
                                            1)
                    for k in range(len(scaled_x_pos)):
                        if k != 8 or nasa == "No":
                            size_planet = 2
                            if k > 4:
                                size_planet = 5

                            color = (255, 255, 255)
                            if k < len(planet_colors):
                                color = planet_colors[k]
                            if (lg_disp_left < ((scaled_x_pos[
                                                     k] - sun_i_x) / 8 +
                                                sunx) < lg_disp_right) and \
                                    (lg_disp_top <
                                     ((scaled_y_pos[
                                           k] - sun_i_y) / 8 +
                                      suny) < lg_disp_bottom):
                                pygame.draw.circle(screen, color,
                                                   [int((scaled_x_pos[
                                                         k] - sun_i_x) / 8 +
                                                    sunx),
                                                    int((scaled_y_pos[
                                                         k] - sun_i_y) / 8 +
                                                    suny)],
                                                   size_planet)
                            if (sm_disp_left < scaled_x_pos[
                                k] < sm_disp_right) and \
                                    (sm_disp_top <
                                     scaled_y_pos[k] < sm_disp_bottom):
                                pygame.draw.circle(screen, color,
                                                   [scaled_x_pos[k],
                                                    scaled_y_pos[k]],
                                                   5)

                else:
                    temp_y_pos = np.sort(current_positions[:, 1])
                    for i in range(len(temp_y_pos)):
                        k = \
                            np.where(current_positions[:, 1] == temp_y_pos[i])[
                                0][
                                0]
                        if k != 8 or nasa == "No":
                            size_planet = 2
                            if k > 4:
                                size_planet = 5

                            color = (255, 255, 255)
                            if k < len(planet_colors):
                                color = planet_colors[k]

                            pygame.draw.circle(screen, color,
                                               [(scaled_x_pos[
                                                     k] - sun_i_x) / 8 + sunx,
                                                suny],
                                               size_planet)
                            if abs(scaled_x_pos[k] - sun_i_x) < 125 and abs(
                                    scaled_y_pos[k] - sun_i_y) < 125:
                                pygame.draw.circle(screen, color,
                                                   [scaled_x_pos[k],
                                                    sun_i_y],
                                                   5)
                # Updates the display with the new frame
                states = menu(
                    screen,
                    [pause, view, speed, 0, 0, click_now, input_active,
                     textbox_active, input_text, nasa, input2_active,
                     textbox2_active, input2_text],
                    scr_width,
                    scr_height,
                    num_days
                )
                pause = states[0]
                speed = states[2]
                input_active = states[6]
                textbox_active = states[7]
                input_text = states[8]
                nasa = states[9]
                input2_active = states[10]
                textbox2_active = states[11]
                input2_text = states[12]

                if (input2_text != "" and input2_active == 0):
                    x_track = [[0] * tail_length for i in
                               range(len(current_positions) + 5)]
                    y_track = [[0] * tail_length for i in
                               range(len(current_positions) + 5)]

                    pygame.draw.rect(screen,
                                     (0, 0, 0),
                                     pygame.Rect(
                                         int(scr_width / 2.6),
                                         int(scr_height / 2.7),
                                         int(scr_width / 1.8),
                                         int(scr_height / 5)
                                     ))
                    pygame.draw.rect(screen,
                                     (255, 255, 255),
                                     pygame.Rect(
                                         int(scr_width / 2.6),
                                         int(scr_height / 2.7),
                                         int(scr_width / 1.8),
                                         int(scr_height / 5)
                                     ),
                                     2)
                    text_handler(screen,
                                 'Processing, Please wait',
                                 int(scr_width / 2.2),
                                 int(scr_height / 2.28),
                                 35,
                                 255)
                    text_handler(screen,
                                 '(Press ESC to Cancel)',
                                 int(scr_width / 1.83),
                                 int(scr_height / 1.95),
                                 20,
                                 255)
                    pygame.display.update(pygame.Rect(
                        int(scr_width / 2.6),
                        int(scr_height / 2.7),
                        int(scr_width / 1.8),
                        int(scr_height / 5)
                    ))
                    # Convert inputted day to simulation time step.
                    sim_time_step = int((int(input2_text) * 86400)
                                        // simulation.time_step_duration)
                    simulation.current_time_step = sim_time_step

                    timePassed = simulation.current_time_step * simulation. \
                        time_step_duration
                    num_days = int(timePassed / 86400)
                    input2_text = ""

                view = states[1]
                click_now = states[5]
                # for event in pygame.event.get():
                #     if event.type == pygame.QUIT:
                #         pygame.quit()
                #         sys.exit()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        keep_running = False
                if not keep_running:
                    pygame.quit()
                    del simulation
                else:
                    pygame.display.flip()


def print_key(screen):  # scr_width, scr_height
    """
        Method to display a planet key
        Method that displays a key of planet colors and names when selected in
        order to aid in user planet idenntification
        **List of input parameters:**
        :param screen: window created by pygame used to display application
    """

    planet_colors = [(255, 136, 0), (196, 182, 108), (242, 197, 107),
                     (11, 170, 255), (179, 67, 30), (252, 156, 66),
                     (255, 194, 89), (108, 230, 219), (162, 141, 166),
                     (108, 164, 204)]

    pygame.draw.circle(screen, planet_colors[2], [850, 70], 4)
    text_handler(screen, "- Venus", 857, 65, 11, 255)
    pygame.draw.circle(screen, planet_colors[3], [850, 90], 4)
    text_handler(screen, "- Earth", 857, 85, 11, 255)
    pygame.draw.circle(screen, planet_colors[4], [850, 110], 4)
    text_handler(screen, "- Mars", 857, 105, 11, 255)
    pygame.draw.circle(screen, planet_colors[5], [850, 130], 4)
    text_handler(screen, "- Jupiter", 857, 125, 11, 255)
    pygame.draw.circle(screen, planet_colors[1], [850, 50], 4)
    text_handler(screen, "- Mercury", 857, 45, 11, 255)
    pygame.draw.circle(screen, planet_colors[6], [850, 150], 4)
    text_handler(screen, "- Saturn", 857, 145, 11, 255)
    pygame.draw.circle(screen, planet_colors[7], [850, 170], 4)
    text_handler(screen, "- Uranus", 857, 165, 11, 255)
    pygame.draw.circle(screen, planet_colors[9], [850, 190], 4)
    text_handler(screen, "- Neptune", 857, 185, 11, 255)
    pygame.draw.circle(screen, planet_colors[8], [850, 210], 4)
    text_handler(screen, "- Pluto", 857, 205, 11, 255)


def menu(screen, states, scr_width, scr_height, numDays):
    """
        Method that will display main menu, as well as handles actions to the
        menu. If mouse is hovering over menu item the text for that menu item
        will change from grey to white. If clicked on or hovered over, menu
        item will activate.
        **Methods used:**
        - text_handler - displays text on the screen
        - pygame.draw - draws rectangles on the screen to separate parts of
          the application.
        **List of input parameters:**
        :param screen: window created by pygame used to display application
        :param states: A list of the current states of the system, see list
            of states below
        :param scr_width: An in that represents the width of the screen
        :param scr_height: An int that represents the height of the screen
        :param numDays: An int that represents how many Earth days have passed
            in the simulation
        **List of Menu Selection Areas:**
        - play_pause - List that contains the length and width parameters
            for the play/pause menu option
        - toggle - List that contains the length and width parameters for
            the view toggle menu option
        - adjust - List that contains the length and width parameters for
            the speed adjustment menu option
        - upload - List that contains the length and width parameters for
            the file upload menu option
        - nasa_right - List that contains the length and width parameters
            for the display pluto menu option
        - key_menu_option - List that contains the length and width
            parameters for the display key menu option
        - day_select - List that contains the length and width parameters
            for the point in time selection menu option
        **List of states of the application:**
        - pause - An int that specifies whether or not the simulation runs,
            0 means it's running, 1 means it is paused
        - view - An int that determines what view is displayed, 0 for
            overhead view, 1 for side view
        - speed - An int that determines the speed of the simulation,
            1x, 2x, 4x, etc
        - rev - An int that would determine if the simulation is running
            in reverse or not, not currently implemented
        - click_now - An int that determines whether the mouse is being
            clicked, 0 means no click, 1 means click
        - input_active - An int that determines whether the file input
            text box shows, 0, means no show, 1 means it will show
        - nasa - String that activates pluto, Yes, means NASA is correct,
            and pluto is not a planet, No means NASA is incorrect and pluto
            is a planet
        - input2_active - An int that displays the travel to a day
            textbox, 0 means no show, 1 means it shows
        - textbox2_active - An int that determines whether the travel to
            textbox is showing, 0 means no, 1 means yes
        - input2_text - String that determines what day will be traveled
            to after the travel to day is determined
        :return: returns the above list of states to feed information to the
            program for control of specific features
    """
    play_pause = [int(scr_width / 33), int(scr_height / 15 * 1.9)]
    toggle = [int(scr_width / 33), int(scr_height / 15 * 2.7)]
    adjust = [int(scr_width / 33), int(scr_height / 15 * 3.5)]
    upload = [int(scr_width / 33), int(scr_height / 15 * 4.3)]
    nasa_right = [int(scr_width / 33), int(scr_height / 15 * 5.1)]
    key_menu_option = [int(scr_width / 33), int(scr_height / 15 * 5.9)]
    day_select = [int(scr_width / 33), int(scr_height / 15 * 6.7)]

    # [pause, view, speed, reverse, upload, click_now, input_active]
    pause = states[0]
    view = states[1]
    speed = states[2]
    rev = states[3]
    upl = states[4]
    click_now = states[5]
    input_active = states[6]
    textbox_active = states[7]
    input_text = states[8]
    nasa = states[9]
    input2_active = states[10]
    textbox2_active = states[11]
    input2_text = states[12]

    action_flag, click_now, click_x, click_y = click_handler(click_now)
    boxes(screen, scr_width, scr_height)
    menu_text(screen, scr_width, scr_height)
    text_handler(screen, "(" + str(speed) + "x)", int(scr_width / 4.3),
                 int(scr_height / 15 * 3.5), 30, 120)
    text_handler(screen, "(" + nasa + ")", int(scr_width / 3.85),
                 nasa_right[1], 30, 120)
    text_handler(screen, "Days Passed: ", 375, 33, 14, 255)
    if numDays < 100:
        text_handler(screen, str(numDays), 408, 51, 14, 255)
    elif numDays > 100 and numDays <= 999:
        text_handler(screen, str(numDays), 402, 51, 14, 255)  # done
    elif numDays > 999:
        text_handler(screen, str(numDays), 398, 51, 14, 255)
    if input_active != 1 and input2_active != 1:
        if play_pause[0] + 200 > click_x > play_pause[0] and play_pause[
            1] + 30 > \
                click_y > play_pause[1]:
            text_handler(screen, 'Pause/ Play', play_pause[0], play_pause[1],
                         30,
                         255)
            if action_flag == 1:
                pause = abs(pause - 1)

        elif toggle[0] + 200 > click_x > toggle[0] and toggle[
            1] + 30 > click_y > \
                toggle[1]:
            text_handler(screen, 'Toggle View', toggle[0], toggle[1], 30, 255)
            if action_flag == 1:
                view = abs(view - 1)

        elif adjust[0] + 260 > click_x > adjust[0] and adjust[
            1] + 30 > click_y > \
                adjust[1]:
            text_handler(screen, 'Adjust Speed', adjust[0], adjust[1], 30, 255)
            text_handler(screen, "(" + str(speed) + "x)", int(scr_width / 4.3),
                         adjust[1], 30, 255)
            if action_flag == 1:
                speed = speed * 2
                if speed > 4:
                    speed = 0.5
        elif upload[0] + 250 > click_x > upload[0] and upload[
            1] + 30 > click_y > \
                upload[1]:
            text_handler(screen, 'New Simulation', upload[0], upload[1], 30,
                         255)
            if action_flag == 1:
                input_active = 1
                action_flag = 0
        elif nasa_right[0] + 310 > click_x > nasa_right[0] and nasa_right[
            1] + 30 \
                > click_y > nasa_right[1]:
            text_handler(screen, 'Is NASA Right?', nasa_right[0],
                         nasa_right[1],
                         30, 255)
            text_handler(screen, "(" + nasa + ")", int(scr_width / 3.85),
                         nasa_right[1], 30, 255)
            if action_flag == 1:
                if nasa == "Yes":
                    nasa = "No"
                else:
                    nasa = "Yes"
        elif key_menu_option[0] + 250 > click_x > key_menu_option[0] and \
                key_menu_option[1] + 30 > click_y > \
                key_menu_option[1]:
            text_handler(screen, 'Show Planet Key', key_menu_option[0],
                         key_menu_option[1], 30, 255)
            print_key(screen)
        elif day_select[0] + 250 > click_x > day_select[0] and day_select[
            1] + 30 \
                > click_y > day_select[1]:
            text_handler(screen, 'Travel to A Day', day_select[0],
                         day_select[1],
                         30, 255)
            if action_flag == 1:
                input2_active = 1

    # Asking for new simulation config file.
    if input_active == 1:
        current_working_directory = os.path.dirname(
            os.path.realpath(__file__)) + "/sim_configs/"
        pause = 1
        root = Tk()
        root.withdraw()
        root.filename = filedialog.askopenfilename(
            initialdir=current_working_directory,
            title="Select a File",
            filetypes=(
                ("xlsx files", "*.xlsx"),
                ("all files", "*.*")
            )
        )
        # If cancel is selected, then just return back to simulator.
        if not root.filename:
            input_active = 0
            textbox_active = 0
            pause = 0
        else:
            # Try opening the file and reading.  If successful, then pass
            # directory onto simulator.
            try:
                input_text = root.filename
                temp_sheets = pd.read_excel(input_text, sheet_name=None)
                # Loop over all sheets and make sure it is a
                # valid config file.
                for key_idx, key in enumerate(temp_sheets):
                    curr_sheet = temp_sheets[key]
                    if key_idx == 0:
                        # Make sure first sheet is the sim config.
                        if not key == "SimConfig":
                            raise FileNotFoundError
                        # Make sure only a single column with the UseNeuralNet
                        if (len(curr_sheet.columns) > 1) or not (
                                curr_sheet.columns[0] == "UseNeuralNet"):
                            raise FileNotFoundError
                        if (
                                not (
                                        curr_sheet['UseNeuralNet'][
                                            0] == 'yes' or
                                        curr_sheet['UseNeuralNet'][
                                            0] == 'Yes' or
                                        curr_sheet['UseNeuralNet'][
                                            0] == 'no' or
                                        curr_sheet['UseNeuralNet'][0] == 'No'
                                )
                        ):
                            raise FileNotFoundError
                    if key_idx > 0:
                        expected_cols = [
                            'Name',
                            'Mass',
                            'Altitude',
                            'StartSpeed',
                            'MStart',
                            'DeltaVX',
                            'DeltaVY',
                            'DeltaVZ'
                        ]
                        if not all(expected_cols == curr_sheet.columns):
                            raise FileNotFoundError
                        # Check each column to make sure a value exists.
                        if math.isnan(curr_sheet['Mass'][0]):
                            raise FileNotFoundError
                        if math.isnan(curr_sheet['Altitude'][0]):
                            raise FileNotFoundError
                        if math.isnan(curr_sheet['StartSpeed'][0]):
                            raise FileNotFoundError

            except FileNotFoundError:
                messagebox.showerror(
                    title='Config File Warning',
                    message='Incompatible or missing config file.  Try '
                            'another. '
                )
                input_text = ""
                textbox_active = 0
                pause = 0
            else:
                input_active = 0
                textbox_active = 0
                pause = 0

        # stops the explorer from endlessly opening, and destroy closes the
        # box.
        input_active = 0
        root.destroy()

    # Option to travel to a specific day selected
    if input2_active == 1:
        pause = 1

        prompt = "Please type the time travel day #:"
        pygame.draw.rect(screen,
                         (0, 0, 0),
                         pygame.Rect(
                             int(scr_width / 2.6),
                             int(scr_height / 2.7),
                             int(scr_width / 1.8),
                             int(scr_height / 5)
                         )
                         )
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         pygame.Rect(
                             int(scr_width / 2.6),
                             int(scr_height / 2.7),
                             int(scr_width / 1.8),
                             int(scr_height / 5)
                         ),
                         2)
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         pygame.Rect(
                             int(scr_width / 2.51),
                             int(scr_height / 2.2),
                             int(scr_width / 1.9),
                             int(scr_height / 15)
                         ),
                         2)
        pygame.draw.rect(screen,
                         (200, 0, 0),
                         pygame.Rect(
                             int(scr_width / 1.124),
                             int(scr_height / 2.7),
                             int(scr_width / 20),
                             int(scr_height / 26)
                         )
                         )
        pygame.draw.rect(screen,
                         (255, 255, 255),
                         pygame.Rect(
                             int(scr_width / 1.124),
                             int(scr_height / 2.7),
                             int(scr_width / 20),
                             int(scr_height / 26)
                         ),
                         2)
        text_handler(screen,
                     "X",
                     int(scr_width / 1.101),
                     int(scr_height / 2.65),
                     18,
                     255)
        if (int(scr_width / 1.124) < click_x < int(scr_width / 1.124) +
            int(scr_width / 20)) and (int(scr_height / 2.7) < click_y <
                                      int(scr_height / 2.7) + int(
                    scr_height / 26)) and action_flag == 1:
            input2_text = ""
            input2_active = 0
            textbox2_active = 0
            pause = 0
        text_handler(screen,
                     prompt,
                     int(scr_width / 2.6) + 10,
                     int(scr_height / 2.7) + 10,
                     25,
                     255)
        if int(scr_width / 2.51) + int(scr_width / 1.9) > click_x > int(
                scr_width / 2.51) and int(scr_height / 2.2) + \
                int(scr_height / 15) > click_y > int(scr_height / 2.2):
            if action_flag == 1:
                textbox2_active = 1
            pygame.draw.rect(screen, (100, 100, 100),
                             pygame.Rect(int(scr_width / 2.51) + 1,
                                         int(scr_height / 2.2) + 1,
                                         int(scr_width / 1.9) - 1,
                                         int(scr_height / 15) - 1))
        if input2_text != "":
            try:
                temp_num = int(input2_text)
            except:
                valid_File = 2
                text_handler(screen,
                             "Invalid number, please try again!",
                             int(scr_width / 2.6) + 10,
                             int(scr_height / 1.9) + 10,
                             12,
                             255)
        if textbox2_active == 1:
            pygame.draw.rect(screen, (100, 100, 100),
                             pygame.Rect(int(scr_width / 2.51) + 1,
                                         int(scr_height / 2.2) + 1,
                                         int(scr_width / 1.9) - 1,
                                         int(scr_height / 15) - 1))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if input2_active == 1:
                        if event.key == pygame.K_RETURN or event.key == pygame \
                                .K_KP_ENTER:
                            try:
                                temp_num = int(input2_text)
                            except:
                                valid_File = 2
                                text_handler(screen,
                                             "Invalid number, please try "
                                             "again!",
                                             int(scr_width / 2.6) + 10,
                                             int(scr_height / 1.9) + 10,
                                             12,
                                             255)
                            else:
                                input2_active = 0
                                textbox2_active = 0
                                pause = 0

                        elif event.key == pygame.K_BACKSPACE:
                            input2_text = input2_text[:-1]
                        else:
                            input2_text += event.unicode
                        keys = pygame.key.get_pressed()
                        if (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and \
                                keys[pygame.K_v]:
                            root = tk.Tk()
                            # keep the window from showing
                            root.withdraw()
                            input2_text += root.clipboard_get()
            temp_text = input2_text
            if len(input2_text) > 30:
                temp_text = input2_text[-30:]
            text_handler(screen, temp_text + "|", int(scr_width / 2.51) + 3,
                         int(scr_height / 2.17) + 3, 30, 255)
        else:
            text_handler(screen, input2_text, int(scr_width / 2.51) + 3,
                         int(scr_height / 2.17) + 3, 30, 255)

    return [pause, view, speed, rev, upload, click_now, input_active,
            textbox_active, input_text, nasa, input2_active,
            textbox2_active, input2_text]


def click_handler(click_now):
    """
        Function to capture characteristics of user clicks
        Function to easily capture mouse location and actions. click_now is
        used to prevent clicks from being repeated each time the simulation
        screen is re-rendered.
        **List of input parameters:**
        :param click_now: contains an integer of either 0 or 1 that denotes
            whether or not the mouse was pressed down during the previous
            program cycle in order to handle sustained presses
        **List of returned values:**
        :returns:
        - action_flag - Flag is set to 0 if the click is a continued press,
          1 if the click is new
        - click_now - Set to 0 if the left mouse button is released, 1 if
          pressed
        - click_x - The inetger x-coordinate of the mouse
        - click_y - The integer y-coordinate of the mouse
    """
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if click[0] == 1:
        if click_now == 0:
            return 1, 1, mouse[0], mouse[1]
        else:
            return 0, 1, mouse[0], mouse[1]
    else:
        return 0, 0, mouse[0], mouse[1]


def text_handler(screen, text, scr_x, scr_y, size, color):
    """
        Function to place text on the screen at a desired location
        Function to place custom text on the screen at any desired location.
        The color of the text is currently restricted to shades of grey and
        white to match the visual theme we are pursuing.
        **List of input parameters:**
        :param screen: the usable area for drawing within the application
            window
        :param text: string of text to be displayed on the screen. One line
            only.
        :param scr_x: the x coordinate for the text to be located at. Must be
            an integer
        :param scr_y: the y coordinate for the text to be located at. Must be
            an integer
        :param size: the size of the text to be displayed, in pixels (height).
            Must be an integer
        :param color: grey shade of the output. Must be an integer between 0
            and 255.
    """
    large_text = pygame.font.Font('freesansbold.ttf', size)
    text_surf = large_text.render(text, True, (color, color, color))
    text_rect = text_surf.get_rect()
    text_rect.topleft = (scr_x, scr_y)
    screen.blit(text_surf, text_rect)


def boxes(screen, scr_width, scr_height):
    """
        Function that places UI divider boxes on the screen
        Function to draw the boundries of the three areas of the application.
        These being the menu, solar system view, and inner planet view. These
        views are static and rendered first, putting them at the bottom of the
        visual instnaces
        **List of input parameters:**
        :param screen: the usable area for drawing within the application
            window
        :param scr_width: the width of the screen in pixels. This will always
            be an integer used for object placement math.
        :param scr_height: the height of the screen in pixels. This will always
            be an integer used for object placement math.
        :param scr_height: the height of the screen in pixels. This will always
            be an integer used for object placement math.
    """
    pygame.draw.rect(screen,
                     (255, 255, 255),
                     pygame.Rect(
                         int(scr_width / 60),
                         int(scr_width / 60),
                         int(scr_width / 3.05),
                         int(scr_height / 2.07)
                     ),
                     2)
    pygame.draw.rect(screen,
                     (255, 255, 255),
                     pygame.Rect(
                         int(scr_width / 60),
                         int(scr_height / 1.9),
                         int(scr_width / 3.05),
                         int(scr_height / 2.23)
                     ),
                     2)
    pygame.draw.rect(screen,
                     (255, 255, 255),
                     pygame.Rect(
                         int(scr_width / 2.8),
                         int(scr_width / 60),
                         int(scr_width / 1.60),
                         int(scr_height / 1.05)
                     ),
                     2)


def menu_text(screen, scr_width, scr_height):
    """
        Function to place menu option text on the screen
        Function to display the base text of the menu on the screen. All
        values start out as light grey but are overlaid with
        white text by another method when moused over
        **List of input parameters:**
        :param screen: the usable area for drawing within the application
            window
        :param scr_width: the width of the screen in pixels. This will always
            be an integer used for object placement math.
        :param scr_height: the height of the screen in pixels. This will
            always be an integer used for object placement math.
    """
    text_handler(screen,
                 'Inner Planets',
                 int(scr_width / 13.8),
                 int(scr_height / 1.8),
                 35,
                 255)
    text_handler(screen,
                 'The Solar System',
                 int(scr_width / 2),
                 int(scr_height / 22),
                 35,
                 255)
    text_handler(screen,
                 'Menu',
                 int(scr_width / 33),
                 int(scr_height / 22),
                 50,
                 255)
    text_handler(screen,
                 'Pause/ Play',
                 int(scr_width / 33),
                 int(scr_height / 15 * 1.9),
                 30,
                 120)
    text_handler(screen,
                 'Toggle View',
                 int(scr_width / 33),
                 int(scr_height / 15 * 2.7),
                 30,
                 120)
    text_handler(screen,
                 'Adjust Speed',
                 int(scr_width / 33),
                 int(scr_height / 15 * 3.5),
                 30,
                 120)
    text_handler(screen,
                 'New Simulation',
                 int(scr_width / 33),
                 int(scr_height / 15 * 4.3),
                 30,
                 120)
    text_handler(screen,
                 'Is NASA Right?',
                 int(scr_width / 33),
                 int(scr_height / 15 * 5.1),
                 30,
                 120)
    text_handler(screen,
                 'Show Planet Key',
                 int(scr_width / 33),
                 int(scr_height / 15 * 5.9),
                 30,
                 120)
    text_handler(screen,
                 'Travel to A Day',
                 int(scr_width / 33),
                 int(scr_height / 15 * 6.7),
                 30,
                 120)


if __name__ == "__main__":
    main()
    sys.exit()
