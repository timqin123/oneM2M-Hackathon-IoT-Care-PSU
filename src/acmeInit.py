from acmeLib import init
from acmeLib.config import *

def initAcme():

	print("Connecting to server....")
	connected = False
	while not connected:
		try:
			init.RETRIEVE (
			    to                      = cseBaseName,        
			    originator              = defaultOriginator, 
			    requestIdentifier       = '123',
			    releaseVersionIndicator = '3',
			)
			connected = True
			print("Connected!")
		except Exception:
			print("--> Probably Connection Refused")
			print("retrying....")
	
	print("Creating AE")
	init.CREATE (
	    to                      = cseBaseName,
	    originator              = aeOriginator,  # Assign an originator ID, must start with 'C'
	    requestIdentifier       = '123',                  
	    releaseVersionIndicator = '3',              
	    resourceType            = init.Type.AE,
	    primitiveContent = 
		{   
		    'm2m:ApplicationEntity': {
		        'resourceName':             'roboCar',  
		        'App-ID':                   'NroboCar',# Application ID, must start with 'N'
		        'requestReachability':      True,            
		        'supportedReleaseVersions': [ '3' ]  
		    }
		}
	)

	init.DELETE (
		to                      = cseBaseName + '/roboCar/Container', 
		originator              = aeOriginator,            
		requestIdentifier       = '123',                
		releaseVersionIndicator = '3',                  
	)

	print("Creating container")
	init.CREATE (
	    to                      = cseBaseName + '/roboCar', 
	    originator              = aeOriginator,       
	    requestIdentifier       = '123',               
	    releaseVersionIndicator = '3',                 
	    resourceType            = init.Type.Container, 
	    primitiveContent = 
		{
		    'm2m:Container': {
		        'resourceName': 'Container'
		    }
		},
	)



print("Initializing ACME server")
initAcme()
