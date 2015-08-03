'''A png image file scroller and slideshow viewer'''

import sys, os, glob, pygame, datetime
from pygame import display, image, event, time
from PIL import Image

display.init()
highest_res = display.list_modes()[0]
SCREEN_WIDTH = 1024 #highest_res[0]
SCREEN_HEIGHT = 768 #highest_res[1]
#SCROLL_PERCENT = .01
#SCROLL_INCREMENT = int(SCREEN_HEIGHT * SCROLL_PERCENT)
SCROLL_INCREMENT = 5 #3px

SCROLL_PAUSE = 100
KEY_PRESS_POLL_TIME = 10
RGB_BLACK = (0,0,0)
IMG_DISPLAY_MILLISECONDS = 3000

def get_center_width_offset(pil_image):
    iwidth = pil_image.size[0]
    return (SCREEN_WIDTH - iwidth) / 2

def get_center_height_offset(pil_image):
    iheight = pil_image.size[1]

    #Don't center if the image is longer than the screen
    if iheight > SCREEN_HEIGHT:
        return 0

    return (SCREEN_HEIGHT - iheight) / 2

def display_image(pygame_img, x_offset, y_offset, screen, pause_time=SCROLL_PAUSE):
    screen.blit(pygame_img, (x_offset, y_offset))
    display.flip()
    pause_scroll(pause_time)

def check_for_exit(poll_time=KEY_PRESS_POLL_TIME):
    time.wait(poll_time)
    if not event.peek():
        return

    ev = event.poll()
    if ev.type == pygame.KEYDOWN and ev.key == pygame.K_SPACE:
        sys.exit(0)

def pause_scroll(pause_time=SCROLL_PAUSE):
    while pause_time >= 0:
        check_for_exit(KEY_PRESS_POLL_TIME)
        pause_time -= KEY_PRESS_POLL_TIME

def scroll_image(pygame_img, x_offset, img_height, screen):
    pixels_offscreen = img_height - SCREEN_HEIGHT
    scroll_intervals = pixels_offscreen / SCROLL_INCREMENT
    scroll_remainder = pixels_offscreen - scroll_intervals * SCROLL_INCREMENT

    display_image(pygame_img, x_offset, 0, screen, IMG_DISPLAY_MILLISECONDS)

    for i in range(0, scroll_intervals+1):
        display_image(pygame_img, x_offset, -i*SCROLL_INCREMENT, screen)

    if scroll_remainder:
        display_image(pygame_img, x_offset, -(scroll_intervals*SCROLL_INCREMENT + scroll_remainder), screen)

    pause_scroll(IMG_DISPLAY_MILLISECONDS)

    if scroll_remainder:
         display_image(pygame_img, x_offset, -(scroll_intervals*SCROLL_INCREMENT), screen)

    for i in range(scroll_intervals, -1, -1):
        display_image(pygame_img, x_offset, -i*SCROLL_INCREMENT, screen)

    pause_scroll(IMG_DISPLAY_MILLISECONDS)

def run():
    ansi_dir = sys.argv[1]
    os.chdir(ansi_dir)
    ansis = glob.glob("*.png") + glob.glob("*.PNG")

    screen = display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
    for ansi_img in ansis:

        pil_image = Image.open(ansi_img)
        x_offset = get_center_width_offset(pil_image)
        y_offset = get_center_height_offset(pil_image)

        img_height = pil_image.size[1]
        pil_image.close()
        pygame_image = image.load(ansi_img)
        screen.fill(RGB_BLACK)

        if img_height > SCREEN_HEIGHT:
            scroll_image(pygame_image, x_offset, img_height, screen)
        else:
            display_image(pygame_image, x_offset, y_offset, screen, IMG_DISPLAY_MILLISECONDS)


    os.chdir('..')

if __name__ == '__main__':
    run()



