import win32con
import win32service

def ListServices():
	resume = 0
	accessSCM = win32con.GENERIC_READ
	accessSrv = win32service.SC_MANAGER_ALL_ACCESS

	#Open Service Control Manager
	hscm = win32service.OpenSCManager(None, None, accessSCM)

	#Enumerate Service Control Manager DB
	typeFilter = win32service.SERVICE_WIN32
	stateFilter = win32service.SERVICE_STATE_ALL

	statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)
	num_of_services = len(statuses)
	for (short_name, desc, status) in statuses:
		print(short_name, "     ", desc, "     ", status)
        
	print(num_of_services)

ListServices()