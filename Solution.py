import platform
import os
import sys
import psutil # For Windows service library
import datetime
import time
import subprocess # For Linux services

SERVICE_LIST_FILE = "serviceList.log"
STATUS_LOG_FILE = "statusLog.log"

def initFiles():
	if os.path.exists(SERVICE_LIST_FILE):
		os.remove(SERVICE_LIST_FILE)
	if os.path.exists(STATUS_LOG_FILE):
		os.remove(STATUS_LOG_FILE)

	open(SERVICE_LIST_FILE, "w").close()
	open(STATUS_LOG_FILE, "w").close()

'''
Windows function
Log_file = Write to this file
Returns dictionary of Service name and Service status
'''
def Win_SampleToLog(log_file):
	dict = {}
	date = datetime.datetime.now()
	log_file.write("{}\n".format(date))
	for it in psutil.win_service_iter():
		service_name = it.name()
		service_status = it.status()
		#service_description = it.description()
		line_to_write = "{} {}\n".format(service_name,service_status)
		log_file.write(line_to_write)
		dict[service_name] = service_status
	log_file.write("\n")
	log_file.close()
	return dict

'''
Linux function
Log_file = Write to this file
Returns directory of Service name and Service status
'''
def Linux_SampleToLog(log_file):
	dict = {}
	output = subprocess.check_output(["service", "--status-all"])
	date = datetime.datetime.now()
	log_file.write("{}\n".format(date))
	for line in output.split('\n'):
		service_name = line[8:]
		service_status = line[3:4]
		line_to_write = "{} {}\n".format(service_name,service_status)
		log_file.write(line_to_write)
		dict[service_name] = service_status
	log_file.write("\n")
	log_file.close()
	return dict

'''
Diffirentiate between 2 samples.
log_file = Log file to append the changes in the services status
sample1 = Old sample
sample2 = New sample
Return dict 
'''
def DiffSamples(log_file, sample1, sample2, platform):
	for key, value in sample1.items():
		date = datetime.datetime.now()
		if key not in sample2:
			str = "Service {} is found at sample 1 but not sample 2. This service probably was uninstalled".format(key)
			print(str)
			log_file.write(str+"\n")
			log_file.flush()
		elif value != sample2[key]:
			if platform == "Windows":
				str = "{}: Service '{}' changed status from '{}' to '{}'".format(date, key, value, sample2[key])
			else:
				status1 = value
				status2 = sample2[key]
				if status1 == "+":
					status1 = "running"
				else:
					status1 = "stopped"

				if status2 == "+":
					status2 = "running"
				else:
					status2 = "stopped"
				str = "{}: Service '{}' changed status from '{}' to '{}'".format(date, key, status1, status2)
			print(str)
			log_file.write(str+"\n")
			log_file.flush()



############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################

# Choose mode: manual or monitor
if(len(sys.argv) <= 1):
	print("Choose mode: monitor or manual")
	exit()

# Monitor mode
if("monitor" == sys.argv[1]):
	if(len(sys.argv) <= 2):
		print("Enter how much seconds to refresh monitor")
		exit()
	# Get seconds
	seconds = sys.argv[2]
	str = "> Monitor mode: Refresh rate of {} seconds".format(seconds)
	print(str)

	initFiles()
	platform = platform.system()
	status_log = open(STATUS_LOG_FILE, "a")
	log_file = open(SERVICE_LIST_FILE, "a")
	###################################### Windows Platform ######################################
	if(platform == "Windows"):
		print("> Windows detected")
		dict = Win_SampleToLog(log_file)
		while True:
			my_dict = Win_SampleToLog(open(SERVICE_LIST_FILE, "a"))
			time.sleep(float(seconds)) 
			my_dict2 = Win_SampleToLog(open(SERVICE_LIST_FILE, "a"))
			DiffSamples(status_log, my_dict, my_dict2, platform)



	###################################### Linux Platform ######################################
	else:
		print("> Linux detected")
		dict = Linux_SampleToLog(log_file)
		while True:
			my_dict = Linux_SampleToLog(open(SERVICE_LIST_FILE, "a"))
			time.sleep(float(seconds)) 
			my_dict2 = Linux_SampleToLog(open(SERVICE_LIST_FILE, "a"))
			DiffSamples(status_log, my_dict, my_dict2, platform)
	
elif("manual" == sys.argv[1]):
	print("> Manual mode")
else:
	print("Use 'manual' or 'monitor' mode")
	exit()
