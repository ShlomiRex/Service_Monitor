import platform
import os
import sys
import psutil # For Windows service library
import datetime
import time
import subprocess # For Linux services




'''
Windows function
Log_file = Write to this file
Returns dictionary of Service name and Service status
'''
def Win_SampleToLog(log_file):
    dict = {}
    for it in psutil.win_service_iter():
        date = datetime.datetime.now()
        service_name = it.name()
        service_status = it.status()
        #service_description = it.description()
        line_to_write = "{}: {} {}\n".format(date, service_name,service_status)
        log_file.write(line_to_write)
        dict[service_name] = service_status
    log_file.close()
    return dict

'''
Linux function
Log_file = Write to this file
Returns directory of Service name and Service status
'''
def Linux_SampleToLog(log_file):
	output = subprocess.check_output(["service", "--status-all"])
	str = "Output = {}".format(output)
	print(str)


'''
Diffirentiate between 2 samples.
log_file = Log file to append the changes in the services status
sample1 = Old sample
sample2 = New sample
Return dict 
'''
def DiffSamples(log_file, sample1, sample2):
	for key, value in sample1.items():
		date = datetime.datetime.now()
		if key not in sample2:
			str = "Service {} is found at sample 1 but not sample 2. This service probably was uninstalled".format(key)
			print(str)
			log_file.write(str+"\n")
			log_file.flush()
		elif value != sample2[key]:
			str = "{}: Service '{}' changed status from '{}' to '{}'".format(date, key, value, sample2[key])
			print(str)
			log_file.write(str+"\n")
			log_file.flush()

    #for key, value in sample2.items():
        #date = datetime.datetime.now()
        #if key not in sample1:
        	#str = "Service {} is found at sample 2 but not sample 1. This service probably was uninstalled".format(key)
            #print(str)
            #log_file.write(str)

# Choose mode: manual or monitor
if(len(sys.argv) <= 1):
	print("Choose mode: monitor or manual")
	exit()

seconds = -1
# Monitor mode
if("monitor" == sys.argv[1]):
	print("> Monitor mode")
	if(len(sys.argv) <= 2):
		print("Enter how much seconds to refresh monitor")
		exit()
    # Get seconds
	seconds = sys.argv[2]
	str = "> Monitor mode: Refresh rate of {} seconds".format(seconds)
	print(str)
elif("manual" == sys.argv[1]):
	print("> Manual mode")
else:
	print("Use 'manual' or 'monitor' mode")
	exit()

platform = platform.system()
###################################### Windows Platform ######################################
if(platform == "Windows"):
	print("> Windows detected")
	status_log = open("statusLog.log", "a")
	log_file = open("serviceList.log", "w")
	dict = Win_SampleToLog(log_file)
	while True:
		my_dict = Win_SampleToLog(open("serviceList.log", "w"))
		time.sleep(float(seconds)) # Sleep for 10 seconds
		my_dict2 = Win_SampleToLog(open("serviceList.log", "w"))
		DiffSamples(status_log, my_dict, my_dict2)



###################################### Linux Platform ######################################
else:
	print("> Linux detected")