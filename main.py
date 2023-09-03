import cv2
import mediapipe as mp
import pyautogui as pag
from keys import *
import os
import winsound
import time

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

wait = False
for_wait = 0
pred_key = ""


def press(key):
    winsound.Beep(1000, 250)
    if key == "Backspace":
        pag.press("backspace")
    elif key == "Enter":
        pag.press("enter")
    elif key == "<":
        pag.press("left")
    elif key == ">":
        pag.press("right")
    elif key == "^":
        pag.press("up")
    elif key == "\\/":
        pag.press("down")
    elif key == "CapsLk":
        pag.press("capslock")
    elif key == "Tab":
        pag.press("tab")
    elif key == "Win":
        pag.press("win")
    elif key == "Copy":
        pag.hotkey('ctrl', 'c')
    elif key == "Paste":
        pag.hotkey('ctrl', 'v')
    elif key == "Cut":
        pag.hotkey('ctrl', 'x')
    elif key == "CtA":
        pag.hotkey('ctrl', 'a')
    elif key == "CtZ":
        pag.hotkey('ctrl', 'z')
    elif key == "Exit":
        winsound.PlaySound("SystemExit", winsound.SND_ALIAS)
        time.sleep(2)
        exit()
    elif key == "Settings":
        os.system("python3 set_config.py")
    else:
        pag.write(key)


fontScale = HEIGHT_KEY / 200


def draw_keys(img, x, y, z):
    global wait, for_wait, pred_key, fontScale

    for k in VK:
        if ((VK[k]['x'] < x < VK[k]['x'] + VK[k]['w']) and (VK[k]['y'] < y < VK[k]['y'] + VK[k]['h']) and (
                z <= THRESHOLD_PRESS)):
            cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x'] + VK[k]['w'], VK[k]['y'] + VK[k]['h']),
                          COLOR_OUT_DOWN, -1)  # thickness -1 means filled rectangle
            cv2.putText(img, f"{k}", (VK[k]['x'] + 30, VK[k]['y'] + 70), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                        COLOR_IN_DOWN, 1, cv2.LINE_AA)
            cv2.circle(img, (x, y), 10, CURSOR_DOWN, -1)

            if k != pred_key:
                press(k)
            pred_key = k
        else:
            cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x'] + VK[k]['w'], VK[k]['y'] + VK[k]['h']),
                          COLOR_IN_UP, -1)
            cv2.rectangle(img, (VK[k]['x'], VK[k]['y']), (VK[k]['x'] + VK[k]['w'], VK[k]['y'] + VK[k]['h']),
                          COLOR_OUT_UP, KEY_BORDER)  # thickness -1 means filled rectangle
            cv2.putText(img, f"{k}", (VK[k]['x'] + 30, VK[k]['y'] + 70), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                        COLOR_OUT_UP, 1,
                        cv2.LINE_AA)
            cv2.circle(img, (x, y), 10, CURSOR_UP, -1)
            if k == pred_key:
                pred_key = "Rr"


def main():
    global pred_key
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        x = 0
        y = 0
        z = 0

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)  # DEBUG
                try:
                    finger_tip = handLms.landmark[INDEX_FINGER_TIP]
                    x = int(finger_tip.x * FRAME_WIDTH)
                    y = int(finger_tip.y * FRAME_HEIGHT)
                    z = int(finger_tip.z * FRAME_WIDTH)
                    # print(f"x={x} , y={y} , z={z}")
                    # cv2.putText(img, f"{x[-1]}, {y[-1]}, {z[-1]}", (x[-1] + 5, y[-1] - 5), cv2.FONT_HERSHEY_SIMPLEX,
                    #             0.5, color, 1,cv2.LINE_AA)
                except IndexError:
                    finger_tip = None

        draw_keys(img, x, y, z)

        cv2.imshow("Zhaba Klava", img)
        cv2.setWindowProperty("Zhaba Klava", cv2.WND_PROP_TOPMOST, 1)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break


main()
