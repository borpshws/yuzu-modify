from tkinter import *
import os, sys, requests, logging

def main():
    splash_root = Tk()
    splash_root.overrideredirect(1)
    splash_root.geometry("200x200")
    splash_label = Label(splash_root, text='Splash Screen', font=18)
    splash_label.pack()

    def main2():
        splash_root.destroy()
        fly()

    splash_root.after(3000, main2)
    mainloop()

def fly():
    logging.info('main function entered, calling for keys...')
    callForKeys()

def callForKeys() -> str:
    res = requests.get('https://raw.githubusercontent.com/emuworld/aio/master/prod.key')
    if res.status_code != 200:
        logging.critical('call to key server failed')
        end(False)
    else:
        print(str(res.content))

def end(cond):
    if cond is True:
        input('\nScript finished successfully, press enter to exit >')
    else:
        input('\nScript failed, press enter to exit >')

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()