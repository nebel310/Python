import pyautogui
import time

time.sleep(2)

long_press_duration = 10  # В минутах
long_press_duration *= 60 # Перевод в секунды

# Функция для эмуляции долгого нажатия на левую кнопку мыши
def long_press():
    pyautogui.mouseDown(button='left')
    time.sleep(long_press_duration)
    pyautogui.mouseUp(button='left')


long_press()