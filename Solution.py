import platform
import os
import sys
import psutil




print(list(psutil.win_service_iter()))

# Choose mode: manual or monitor
if(len(sys.argv) <= 1):
	print("Choose mode: monitor or manual")
	exit()

# Get seconds
if("monitor" == sys.argv[1]):
	print("> Monitor mode")
	if(len(sys.argv) <= 2):
		print("Enter how much seconds to refresh monitor")
		exit()
	seconds = sys.argv[2]
elif("manual" == sys.argv[1]):
	print("> Manual mode")
else:
	print("Use 'manual' or 'monitor' mode")
	exit()

platform = platform.system()
###################################### Windows Platform ######################################
if(platform == "Windows"):
	print("> Windows detected")



###################################### Linux Platform ######################################
else:
	print("> Linux detected")