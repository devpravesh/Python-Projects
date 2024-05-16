# WhatsApp Message Scheduler

import time
import pywhatkit
import pyautogui
from pynput.keyboard import Key, Controller

keyboard = Controller()


def send_whatsapp_message(msg: str, phone_numbers: list):
    try:
        for phone_no in phone_numbers:
            pywhatkit.sendwhatmsg_instantly(
                phone_no=phone_no,
                message=msg,
                tab_close=False
            )
            time.sleep(0)
            pyautogui.click()
            time.sleep(0)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            print(f"Message sent to {phone_no}!")
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    # List of phone numbers of your friends
    friend_numbers = ["+918652513863", "+918369780517"]
    message = "Hey bro, have you completed your Python task?"
    send_whatsapp_message(msg=message, phone_numbers=friend_numbers)

