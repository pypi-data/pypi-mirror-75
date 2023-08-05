# -*- coding: utf-8 -*-

import sys
import logging
from .framework import Init, Log, System, Serial, GPIO, Camera, Socket, Ai, EP, ServoRobot, Message

logging.getLogger("requests").setLevel(logging.ERROR)

if len(sys.argv) < 3:
    sys.exit(0)

