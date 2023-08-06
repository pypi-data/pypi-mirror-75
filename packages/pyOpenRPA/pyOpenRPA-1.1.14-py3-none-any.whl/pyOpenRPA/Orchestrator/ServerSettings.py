import json
from inspect import signature # For detect count of def args
#ControlPanelDict
from desktopmagic.screengrab_win32 import (
	getDisplayRects, saveScreenToBmp, saveRectToBmp, getScreenAsImage,
	getRectAsImage, getDisplaysAsImages)
from http import cookies
import uuid # generate UUID4
import time # sleep functions
import datetime # datetime functions
import threading # Multi-threading

# /Orchestrator/RobotRDPActive/ControlPanelDictGet
def RobotRDPActive_ControlPanelDictGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    lResultDict = {
        "DataList":[
            # {"SessionKeyStr":"", "SessionHexStr": "", "IsFullScreenBool": False, "IsIgnoredBool": False}
        ]
    }
    # Iterate throught the RDP List
    for lRDPSessionKeyStrItem in inGlobalDict["RobotRDPActive"]["RDPList"]:
        lRDPConfiguration = inGlobalDict["RobotRDPActive"]["RDPList"][lRDPSessionKeyStrItem] # Get the configuration dict
        lDataItemDict = {"SessionKeyStr":"", "SessionHexStr": "", "IsFullScreenBool": False, "IsIgnoredBool": False} # Template
        lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem # Session key str
        lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"] # Session Hex
        lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGlobalDict["RobotRDPActive"]["FullScreenRDPSessionKeyStr"] else False # Check  the full screen for rdp window
        lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"] # Is ignored
        lResultDict["DataList"].append(lDataItemDict)
    # Send message back to client
    message = json.dumps(lResultDict)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")

# def to check control panels for selected session
def Monitor_ControlPanelDictGet_SessionCheckInit(inRequest,inGlobalDict):
    lL = inGlobalDict["Logger"]  # Alias for logger
    lLifetimeSecFloat = inGlobalDict["Client"]["Session"]["LifetimeSecFloat"]
    lLifetimeRequestSecFloat = inGlobalDict["Client"]["Session"]["LifetimeRequestSecFloat"]
    lControlPanelRefreshIntervalSecFloat = inGlobalDict["Client"]["Session"]["ControlPanelRefreshIntervalSecFloat"]
    lCookieSessionGUIDStr = None  # generate the new GUID
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Technicaldef - interval check control panels + check actuality of the session by the datetime
    def TechnicalCheck():
        lItemValue = inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr]
        # Lifetime is ok - check control panel
        lDatasetCurrentBytes = Monitor_ControlPanelDictGet(inRequest,inGlobalDict) # Call the control panel
        if lDatasetCurrentBytes != lItemValue["DatasetLast"]["ControlPanel"]["Data"]: # Check if dataset is changed
            lItemValue["DatasetLast"]["ControlPanel"]["Data"] = lDatasetCurrentBytes # Set new datset
            lItemValue["DatasetLast"]["ControlPanel"]["ReturnBool"] = True # Set flag to return the data
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # Technicaldef - Create new session struct
    def TechnicalSessionNew(inSessionGUIDStr):
        lCookieSessionGUIDStr = inSessionGUIDStr  # Generate the new GUID
        lSessionNew = { # Session with some GUID str. On client session guid stored in cookie "SessionGUIDStr"
            "InitDatetime": datetime.datetime.now(), # Datetime when session GUID was created
            "DatasetLast": {
                "ControlPanel": {
                    "Data": None, # Struct to check with new iterations. None if starts
                    "ReturnBool": False # flag to return, close request and return data as json
                }
            },
            "ClientRequestHandler": inRequest, # Last client request handler
            "UserADStr": inRequest.OpenRPA["User"], # User, who connect. None if user is not exists
            "DomainADStr": inRequest.OpenRPA["Domain"], # Domain of the user who connect. None if user is not exists
        }
        inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr] = lSessionNew # Set new session in dict
        inRequest.OpenRPAResponseDict["SetCookies"]["SessionGUIDStr"] = lCookieSessionGUIDStr # Set SessionGUIDStr in cookies
        if lL: lL.info(f"New session GUID is created. GUID {lCookieSessionGUIDStr}")
        return lCookieSessionGUIDStr
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    lCreateNewSessionBool = False # Flag to create new session structure
    # step 1 - get cookie SessionGUIDStr
    lSessionGUIDStr = inRequest.headers.get("SessionGUIDStr", None)
    if lSessionGUIDStr is not None: # Check if GUID session is ok
        lCookieSessionGUIDStr = lSessionGUIDStr # Get the existing GUID
        if lSessionGUIDStr not in inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"]:
            lCookieSessionGUIDStr= TechnicalSessionNew(inSessionGUIDStr = lSessionGUIDStr) # Create new session
        else: # Update the datetime of the request session
            inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr]["InitDatetime"]=datetime.datetime.now()
    else:
        lCookieSessionGUIDStr = TechnicalSessionNew(inSessionGUIDStr = lSessionGUIDStr) # Create new session
    # Init the RobotRDPActive in another thread
    #lThreadCheckCPInterval = threading.Thread(target=TechnicalIntervalCheck)
    #lThreadCheckCPInterval.daemon = True  # Run the thread in daemon mode.
    #lThreadCheckCPInterval.start()  # Start the thread execution.

    # Step 2 - interval check if data is exist
    lTimeStartSecFloat = time.time()
    lDoWhileBool = True # Flag to iterate throught the lifetime of the request
    while lDoWhileBool:
        #print(lTechnicalSessionGUIDCache)
        #print(lCookieSessionGUIDStr)
        if lCookieSessionGUIDStr in inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"]:
            lItemValue = inGlobalDict["Client"]["Session"]["TechnicalSessionGUIDCache"][lCookieSessionGUIDStr]
            if (time.time() - lTimeStartSecFloat) >= lLifetimeRequestSecFloat: # Check if lifetime client request is over or has no key
                if lL: lL.debug(f"Client request lifetime is over")
                lDoWhileBool = False # Stop the iterations
            if lDoWhileBool:
                TechnicalCheck() # Calculate the CP
                if lItemValue["DatasetLast"]["ControlPanel"]["ReturnBool"] == True: # Return data if data flag it True
                    lDatasetCurrentBytes = lItemValue["DatasetLast"]["ControlPanel"]["Data"]  # Set new dataset
                    inResponseDict = inRequest.OpenRPAResponseDict
                    inResponseDict["Body"] = lDatasetCurrentBytes
                    lItemValue["DatasetLast"]["ControlPanel"]["ReturnBool"] = False  # Set flag that data was returned
                    lDoWhileBool = False  # Stop the iterations
        else:
            lCookieSessionGUIDStr = TechnicalSessionNew(inSessionGUIDStr = lCookieSessionGUIDStr) # Create new session
        if lDoWhileBool:  # Sleep if we wait hte next iteration
            time.sleep(lControlPanelRefreshIntervalSecFloat)  # Sleep to the next iteration

def Monitor_ControlPanelDictGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    lL = inGlobalDict["Logger"] # Alias for logger
    # Create result JSON
    lResultJSON = {"RenderRobotList": [], "RenderRDPList": []}
    lRenderFunctionsRobotList = inGlobalDict["ControlPanelDict"]["RobotList"]
    for lItem in lRenderFunctionsRobotList:
        lUACBool = True # Check if render function is applicable User Access Rights (UAC)
        if inGlobalDict["Server"]["AccessUsers"]["FlagCredentialsAsk"] is True:
            lUserRights = inGlobalDict["Server"]["AccessUsers"]["RuleDomainUserDict"][(inRequest.OpenRPA["Domain"].upper(),inRequest.OpenRPA["User"].upper())]
            if len(lUserRights["ControlPanelKeyAllowedList"]) > 0 and lItem["KeyStr"] not in lUserRights["ControlPanelKeyAllowedList"]:
                lUACBool = False # UAC Check is not passed - False for user
        if lUACBool: # Run function if UAC is TRUE
            # Выполнить вызов и записать результат
            # Call def (inRequest, inGSettings) or def (inGSettings)
            lItemResultDict = None
            lDEFSignature = signature(lItem["RenderFunction"]) # Get signature of the def
            lDEFARGLen = len(lDEFSignature.parameters.keys()) # get count of the def args
            try:
                if lDEFARGLen == 1: # def (inGSettings)
                    lItemResultDict = lItem["RenderFunction"](inGlobalDict)
                elif lDEFARGLen == 2: # def (inRequest, inGSettings)
                    lItemResultDict = lItem["RenderFunction"](inRequest, inGlobalDict)
                elif lDEFARGLen == 0: # def ()
                    lItemResultDict = lItem["RenderFunction"]()
                # RunFunction
                lResultJSON["RenderRobotList"].append(lItemResultDict)
            except Exception as e:
                if lL: lL.exception(f"Error in control panel. CP item {lItem}. Exception is below")
    # Iterate throught the RDP list
    for lRDPSessionKeyStrItem in inGlobalDict["RobotRDPActive"]["RDPList"]:
        lRDPConfiguration = inGlobalDict["RobotRDPActive"]["RDPList"][
            lRDPSessionKeyStrItem]  # Get the configuration dict
        lDataItemDict = {"SessionKeyStr": "", "SessionHexStr": "", "IsFullScreenBool": False,
                         "IsIgnoredBool": False}  # Template
        lDataItemDict["SessionKeyStr"] = lRDPSessionKeyStrItem  # Session key str
        lDataItemDict["SessionHexStr"] = lRDPConfiguration["SessionHex"]  # Session Hex
        lDataItemDict["IsFullScreenBool"] = True if lRDPSessionKeyStrItem == inGlobalDict["RobotRDPActive"][
            "FullScreenRDPSessionKeyStr"] else False  # Check  the full screen for rdp window
        lDataItemDict["IsIgnoredBool"] = lRDPConfiguration["SessionIsIgnoredBool"]  # Is ignored
        lResultJSON["RenderRDPList"].append(lDataItemDict)
    # Send message back to client
    message = json.dumps(lResultJSON)
    # Write content as utf-8 data
    #inResponseDict["Body"] = bytes(message, "utf8")
    return bytes(message, "utf8")
# UserAccess get rights hierarchy dict in json
def UserRoleHierarchyGet(inRequest,inGlobalDict):
    inResponseDict = inRequest.OpenRPAResponseDict
    # Create result JSON
    lResultDict = inRequest.OpenRPA["DefUserRoleHierarchyGet"]() # Get the User Role Hierarchy list
    # Send message back to client
    message = json.dumps(lResultDict)
    # Write content as utf-8 data
    inResponseDict["Body"] = bytes(message, "utf8")

def GetScreenshot(inRequest,inGlobalDict):
    # Get Screenshot
    def SaveScreenshot(inFilePath):
        # grab fullscreen
        # Save the entire virtual screen as a PNG
        lScreenshot = getScreenAsImage()
        lScreenshot.save('screenshot.png', format='png')
        # lScreenshot = ScreenshotSecondScreen.grab_screen()
        # save image file
        # lScreenshot.save('screenshot.png')
    # Сохранить файл на диск
    SaveScreenshot("Screenshot.png")
    lFileObject = open("Screenshot.png", "rb")
    # Write content as utf-8 data
    inRequest.OpenRPAResponseDict["Body"] = lFileObject.read()
    # Закрыть файловый объект
    lFileObject.close()
def SettingsUpdate(inGlobalConfiguration):
    import os
    import pyOpenRPA.Orchestrator
    lOrchestratorFolder = "\\".join(pyOpenRPA.Orchestrator.__file__.split("\\")[:-1])
    lURLList = \
        [ #List of available URLs with the orchestrator server
            #{
            #    "Method":"GET|POST",
            #    "URL": "/index", #URL of the request
            #    "MatchType": "", #"BeginWith|Contains|Equal|EqualCase",
            #    "ResponseFilePath": "", #Absolute or relative path
            #    "ResponseFolderPath": "", #Absolute or relative path
            #    "ResponseContentType": "", #HTTP Content-type
            #    "ResponseDefRequestGlobal": None #Function with str result
            #}
            #Orchestrator basic dependencies
            {"Method":"GET", "URL": "/", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.xhtml"), "ResponseContentType": "text/html"},
            {"Method":"GET", "URL": "/Index.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\Index.js"), "ResponseContentType": "text/javascript"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.css"), "ResponseContentType": "text/css"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/semantic.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\semantic.min.js"), "ResponseContentType": "application/javascript"},
            {"Method":"GET", "URL": "/3rdParty/jQuery/jquery-3.1.1.min.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\jQuery\\jquery-3.1.1.min.js"), "ResponseContentType": "application/javascript"},
            {"Method":"GET", "URL": "/3rdParty/Google/LatoItalic.css", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Google\\LatoItalic.css"), "ResponseContentType": "font/css"},
            {"Method":"GET", "URL": "/3rdParty/Semantic-UI-CSS-master/themes/default/assets/fonts/icons.woff2", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Semantic-UI-CSS-master\\themes\\default\\assets\\fonts\\icons.woff2"), "ResponseContentType": "font/woff2"},
            {"Method":"GET", "URL": "/favicon.ico", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "Web\\favicon.ico"), "ResponseContentType": "image/x-icon"},
            {"Method":"GET", "URL": "/3rdParty/Handlebars/handlebars-v4.1.2.js", "MatchType": "EqualCase", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\Handlebars\\handlebars-v4.1.2.js"), "ResponseContentType": "application/javascript"},
            {"Method": "GET", "URL": "/Monitor/ControlPanelDictGet", "MatchType": "Equal", "ResponseDefRequestGlobal": Monitor_ControlPanelDictGet_SessionCheckInit, "ResponseContentType": "application/json"},
            {"Method": "GET", "URL": "/GetScreenshot", "MatchType": "BeginWith", "ResponseDefRequestGlobal": GetScreenshot, "ResponseContentType": "image/png"},
            {"Method": "GET", "URL": "/pyOpenRPA_logo.png", "MatchType": "Equal", "ResponseFilePath": os.path.join(lOrchestratorFolder, "..\\Resources\\Web\\pyOpenRPA_logo.png"), "ResponseContentType": "image/png"},
            {"Method": "POST", "URL": "/Orchestrator/UserRoleHierarchyGet", "MatchType": "Equal","ResponseDefRequestGlobal": UserRoleHierarchyGet, "ResponseContentType": "application/json"}
    ]
    inGlobalConfiguration["Server"]["URLList"]=inGlobalConfiguration["Server"]["URLList"]+lURLList
    return inGlobalConfiguration