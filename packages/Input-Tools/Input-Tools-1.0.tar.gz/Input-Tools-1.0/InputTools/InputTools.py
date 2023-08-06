import autopy
from pynput.keyboard import Key, Controller

keyboard = Controller()
def move_mouse(x_coordinate:int, y_coordinate:int, should_animate:bool):
    if should_animate:
        autopy.mouse.smooth_move(x_coordinate, y_coordinate)
    else:
        autopy.mouse.move(x_coordinate, y_coordinate)

def left_click_mouse():
    autopy.mouse.click()


def keyboard_type(type_string:str):
    keyboard.type(type_string)

def keyboard_press_enter():
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def keyboard_multi_type(type_string:str, number_of_times:int, press_enter:bool, show_type_fraction:bool):
    if press_enter:
        for i in range(number_of_times):
            number_fraction = " " + str(i+1) + "/" + str(number_of_times)
            if show_type_fraction:
                keyboard.type(type_string+number_fraction)
            else:
                keyboard.type(type_string)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

    else:
        for i in range(number_of_times):
            number_fraction = " " + str(i+1) + "/" + str(number_of_times)
            if show_type_fraction:
                keyboard.type(type_string+number_fraction)
            else:
                keyboard.type(type_string)




