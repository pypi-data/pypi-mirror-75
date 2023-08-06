# Def to check inGSettings and update structure to the backward compatibility
# !!! ATTENTION: Backward compatibility has been started from v1.1.13 !!!
# So you can use config of the orchestrator 1.1.13 in new Orchestrator versions and all will be ok :) (hope it's true)
def Update(inGSettings):
    lL = inGSettings["Logger"] # Alias for logger
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # v1.1.13 to v1.1.14
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    if "Autocleaner" not in inGSettings: # Add "Autocleaner" structure
        inGSettings["Autocleaner"] = { # Some gurbage is collecting in g settings. So you can configure autocleaner to periodically clear gSettings
            "IntervalSecFloat": 600.0, # Sec float to periodically clear gsettings
        }
        if lL: lL.warning(f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'Autocleaner' structure") # Log about compatibility
    if "Client" not in inGSettings: # Add "Client" structure
        inGSettings["Client"] = { # Settings about client web orchestrator
            "Session":{ # Settings about web session. Session algorythms works only for special requests (URL in ServerSettings)
                "LifetimeSecFloat": 600.0, # Client Session lifetime in seconds. after this time server will forget about this client session
                "LifetimeRequestSecFloat": 120.0, # 1 client request lifetime in server in seconds
                "ControlPanelRefreshIntervalSecFloat": 1.5, # Interval to refresh control panels for session,
                "TechnicalSessionGUIDCache": { # TEchnical cache. Fills when web browser is requesting
                    #"SessionGUIDStr":{ # Session with some GUID str. On client session guid stored in cookie "SessionGUIDStr"
                    #    "InitDatetime": None, # Datetime when session GUID was created
                    #    "DatasetLast": {
                    #        "ControlPanel": {
                    #            "Data": None, # Struct to check with new iterations. None if starts
                    #            "ReturnBool": False # flag to return, close request and return data as json
                    #        }
                    #    },
                    #    "ClientRequestHandler": None, # Last client request handler
                    #    "UserADStr": None, # User, who connect. None if user is not exists
                    #    "DomainADStr": None, # Domain of the user who connect. None if user is not exists
                    #}
                }
            }
        }
        if lL: lL.warning(f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'Client' structure")  # Log about compatibility
    if "RequestTimeoutSecFloat" not in inGSettings["Server"]: # Add Server > "RequestTimeoutSecFloat" property
        inGSettings["Server"]["RequestTimeoutSecFloat"] = 300 # Time to handle request in seconds
        if lL: lL.warning(
            f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'Server' > 'RequestTimeoutSecFloat' property")  # Log about compatibility
    if "DefSettingsUpdatePathList" not in inGSettings["OrchestratorStart"]:  # Add OrchestratorStart > "DefSettingsUpdatePathList" property
        inGSettings["OrchestratorStart"]["DefSettingsUpdatePathList"] = []  # List of the .py files which should be loaded before init the algorythms
        if lL: lL.warning(f"Backward compatibility (v1.1.13 to v1.1.14): Add default 'OrchestratorStart' > 'DefSettingsUpdatePathList' property list")  # Log about compatibility