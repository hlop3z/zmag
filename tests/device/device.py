# -*- coding: utf-8 -*-
"""
ZMAG Device
"""

# Python
import os

# Set Env for Device Mode
os.environ["ZMAG_TYPE"] = "1"

# ZMAG
from zmag import Device  # pylint: disable=C

# import time
# from pathlib import Path

proxy = Device(
    mode="forwarder",  # queue, forwarder, streamer
    publickey="2x.Y>2(J]I:$7i+CS<BVZMJyXEX)H8?31k5o)?mQ",
    secretkey="B.)wGr$@cYiy(<$ES*$pZ3UmIPEIy+lt1qNY!!Kn",
)

proxy.start()
