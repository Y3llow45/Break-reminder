from win10toast import ToastNotifier
import time
text = "TAKE A BREAK"
subtext = "5 min break"

def main():
    time.sleep(1800)
    notification()
    time.sleep(292)
    start()
    main()

def notification():
    toast = ToastNotifier()
    toast.show_toast(text,subtext,duration=4)
    
def start():
    toast = ToastNotifier()
    toast.show_toast("Started","You have 30 mins",duration=4)
    
start()
main()