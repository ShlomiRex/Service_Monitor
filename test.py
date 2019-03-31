import platform
import os
import sys
import psutil

print(list(psutil.win_service_iter()))
for it in psutil.win_service_iter():
    print(it.name(), it.status())
    