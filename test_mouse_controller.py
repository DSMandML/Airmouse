import pyautogui
import time


screen_width, screen_height = pyautogui.size()
print(f'Screen size: {screen_height}x{screen_width}')
time.sleep(5)
print('Moving to screen center..')
pyautogui.moveTo(screen_width / 2, screen_height / 2)
time.sleep(5)
print('Scroll..')
pyautogui.hscroll(1000)
time.sleep(5)
exit()
print('Dragging..')
pyautogui.drag(100, 100, button='left')
time.sleep(5)
exit()
print('Perform left click..')
pyautogui.click()
time.sleep(5)
print('Moving 100 pixels to right')
pyautogui.move(100, 0)  # Move 100 pixels to the right
time.sleep(5)
print('Perform right click..')
pyautogui.rightClick()
# pyautogui.doubleClick()

# Check the documentation for more options and functions: https://pyautogui.readthedocs.io/en/latest/
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
#cdlllllllllllllllll
