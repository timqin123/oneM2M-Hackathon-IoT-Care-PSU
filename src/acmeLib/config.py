# ACME Local
cseRN                 = 'cse-in'
host                  = "http://44.203.203.28:8080/"
cseBaseName           = "cse-in"
defaultOriginator     = "CAdmin"
aeOriginator          = "CroboCarClient"
upperTester           = f'{host}/__ut__'                            # Or None if not defined

# Extra Configurations
showLongNames         = True                                        # Use attribute names instead of their short name versions

# Notification Server
notificationURLBase   = 'http://localhost'                          # The base URL for the Notification Server
notificationPort      = 9999                                        # Notification port
notificationURL       = f'{notificationURLBase}:{notificationPort}' # Notification full URL

# Proxy configuration
httpProxy             = None
httpsProxy            = None

# OAuth2 Server
doOAuth               = False
oauthServerUrl        = None
clientSecret          = None
clientId              = None

