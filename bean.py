from tkinter import *
import os, requests, logging, easygui

def splash():
    try:
        splash_root = Tk()
        
        windowWidth = splash_root.winfo_reqwidth()
        windowHeight = splash_root.winfo_reqheight()
        logging.info(f"Width{windowWidth},Height{windowHeight}")

        positionRight = int(splash_root.winfo_screenwidth()/2 - windowWidth/2)
        positionDown = int(splash_root.winfo_screenheight()/2 - windowHeight/2)

        splash_root.overrideredirect(1)
        splash_root.geometry("+{}+{}".format(positionRight, positionDown))
        splash_root.lift()
        splash_root.image = PhotoImage(file='splash.png')
        splash_label = Label(splash_root, image=splash_root.image, bg='white')
        #splash_root.eval('tk::PlaceWindow . center')
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
    except TclError:
        main()

def main():
    logging.info('main function entered, calling for keys...')
    keys = callForKeys()
    path = requestPath()
    valid = validateDirectory(path)
    if valid is False:
        logging.critical('the yuzu install directory is invalid or is missing critical files, cannot proceed')
        end(False)
    else:
        logging.info('install directory passed validation')
        os.chdir(path + r'\keys')
        logging.info('asking for confirmation to continue operation')
        confirmation = easygui.ynbox('Continuing will place a valid prod.keys file in the keys directory of yuzu which will allow the emulator to run. Select yes to proceed, select no to cancel.', 'yuzu-patcher')
        if confirmation is False:
            logging.info('confirmation resulted in a cancel')
            end(True)
        
        if checkForExistingKeys(os.getcwd()) is True:
            logging.warning('an existing prod.keys file was found, asking for override')
            override = easygui.ynbox('The file prod.keys already exists in the yuzu directory, do you want to override?', 'yuzu-patcher')
            if override is True:
                logging.info('override is true, proceeding...')
                createFile(os.getcwd(), keys, override=True)
            else:
                logging.info('override is false, exiting...')
                end(True)
        else:
            createFile(os.getcwd(), keys, override=False)
        
        filevalidation = validateFile("prod.keys", keys)
        if filevalidation is True:
            logging.info('file validation completed and returned no errors, script finished')
            end(True)
        else:
            logging.critical('file validation completed and returned errors, script finished improperly')
            end(False)

def checkForExistingKeys(path) -> bool:
    if 'prod.keys' in os.listdir(path):
        return True
    else:
        return False

def createFile(path, data, override) -> None:
    if override is False:
        logging.info('creating file without override')
        f = open("prod.keys", "a")
        f.write(data.decode("utf-8"))
        f.close()
    else:
        logging.info('creating file with override')
        f = open("prod.keys", "w")
        f.write(data.decode("utf-8"))
        f.close()

def validateFile(file, data) -> bool:
    logging.info('validating the created file...')
    f = open(file, "r")
    if f.read() == data.decode('utf-8'):
        return True
    else:
        return False

def validateDirectory(path) -> bool:
    logging.info('validating install directory...')
    if os.listdir(path) == []:
        return False
    else:
        if 'sdmc' in os.listdir(path) and 'log' in os.listdir(path):
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
    open_file = easygui.diropenbox(title='yuzu-patcher', msg='Select yuzu install directory, Cancel to use default install location')
    if open_file is None:
        p = os.getenv('APPDATA') + '\yuzu'
        logging.info('no directory specified defaulting to: ' + f'\'{p}\'')
        return os.getenv('APPDATA') + '\yuzu'
    else:
        logging.info('path specified: ' + f'\'{open_file}\'')
        return open_file

def end(cond) -> None:
    if cond is True:
        input('\nScript finished successfully, press enter to exit >')
        exit()
    else:
        input('\nScript failed, press enter to exit >')
        exit()

if __name__ == '__main__':
    print('decode > PY')
    print('Copyright (c) 2022, borpshws')
    logging.basicConfig(level=logging.INFO, format='%(msecs)03d %(levelname)s: %(message)s')
    logging.info('creating splash for 3s')
    splash()