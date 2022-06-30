import os
from datetime import datetime


def Request_gvm_image(display_id):
    if display_id == 1:
        filepath = 'IMG_HOME.png'
    if display_id == 0:
        filepath = 'temp15_10_29_01.png'

    return filepath



