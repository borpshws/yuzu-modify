from tkinter import *
import os, sys, requests, logging, easygui

def splash():
    splash_root = Tk()
    splash_root.overrideredirect(1)
    splash_root.geometry("512x512")
    splash_root.lift()
    splash_root.image = PhotoImage(file='splash.png')
    splash_label = Label(splash_root, image=splash_root.image, bg='white')
    splash_root.eval('tk::PlaceWindow . center')
    splash_root.wm_attributes("-topmost", True)
    splash_root.wm_attributes("-disabled", True)
    splash_root.wm_attributes("-transparentcolor", "white")
    splash_label.pack()

    def splash2():
        splash_root.destroy()
        logging.info('splash end')
        main()

    splash_root.after(3000, splash2)
    mainloop()

def main():
    logging.info('main function entered, calling for keys...')
    keys = callForKeys()
    path = requestPath()
    valid = validateDirectory(path)
    print(valid)

def validateDirectory(path):
    if os.listdir(path) == []:
        return False
    else:
        if 'maintenancetool.exe' in os.listdir(path) and 'metadata.json' in os.listdir(path):
            return True
        else:
            return False

def callForKeys() -> bytes:
    res = requests.get('https://raw.githubusercontent.com/emuworld/aio/master/prod.keys')
    if res.status_code != 200:
        logging.critical('call to key server resulted in a status code ≠ 200, cannot proceed')
        end(False)
    else:
        logging.info('keys successfully retrived from server')
        return res.content

def requestPath() -> str:
    logging.info('await directory selection...')
    open_file = easygui.diropenbox(title='Select yuzu install directory', msg='Cancel to use default install location')
    if open_file is None:
        return os.getenv('LOCALAPPDATA') + '\yuzu'
    else:
        return open_file

def end(cond):
    if cond is True:
        input('\nScript finished successfully, press enter to exit >')
        exit()
    else:
        input('\nScript failed, press enter to exit >')
        exit()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(msecs)03d %(levelname)s: %(message)s')
    logging.info('creating splash for 3s')
    splash()