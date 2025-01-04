import RPi.GPIO as GPIO
button_GPIO=24
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_GPIO, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def on_button_press(func):
    """Wrapper für Funktionen, die bei Knopfdruck ausgeführt werden sollen

    Args:
        func (callable): Funktion, die bei Knopfdruck ausgeführt werden soll

    Returns:
       callable: Funktion
    """
    funcs.append(func)
    return func

funcs=[]

def run_funcs(_):
    """führt die Funktionen aus"""
    if not GPIO.input(button_GPIO):
        return
    for func in funcs:
        func()
GPIO.add_event_detect(button_GPIO,GPIO.RISING,run_funcs,100)
