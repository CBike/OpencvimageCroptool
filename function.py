import os
from datetime import datetime


def Request_gvm_image(display_id):
    now = datetime.now()
    timestamp = now.strftime("%d_%H_%M_%S")
    filepath =  'D:\excelrunner_report\captured_image\\temp{}.png'.format(timestamp)
    os.system('adb exec-out screencap -p -d {} > {}'
              .format(display_id, filepath))

    return filepath


