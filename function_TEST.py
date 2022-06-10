import os
from datetime import datetime


def Request_gvm_image(display_id):
    print("function_Request_gvm_image")
    if display_id == 1:
        filepath = 'C:\python_dev\imageCroptool(GVM)\\bike.png'
    if display_id == 0:
        filepath = 'C:\python_dev\imageCroptool(GVM)\\car.png'

    return filepath



