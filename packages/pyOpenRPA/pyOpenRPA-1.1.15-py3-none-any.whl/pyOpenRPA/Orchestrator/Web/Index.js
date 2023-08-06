var mGlobal={}
window.onload=function() {
    //document.cookie = "SessionGUIDStr=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    //Render existing data
    //mGlobal.Monitor.fControlPanelRefresh_TechnicalRender()
}
$(document).ready(function() {
      document.cookie = "SessionGUIDStr=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
      console.log("Cookie is deleted")
      // fix main menu to page on passing
      $('.main.menu').visibility({
        type: 'fixed'
      });
      $('.overlay').visibility({
        type: 'fixed',
        offset: 80
      });

      // lazy load images
      $('.image').visibility({
        type: 'image',
        transition: 'vertical flip in',
        duration: 500
      });

      // show dropdown on hover
      $('.main.menu  .ui.dropdown').dropdown({
        on: 'hover'
      });
    function clone(obj) {
        var copy;

        // Handle the 3 simple types, and null or undefined
        if (null == obj || "object" != typeof obj) return obj;

        // Handle Date
        if (obj instanceof Date) {
            copy = new Date();
            copy.setTime(obj.getTime());
            return copy;
        }

        // Handle Array
        if (obj instanceof Array) {
            copy = [];
            for (var i = 0, len = obj.length; i < len; i++) {
                copy[i] = clone(obj[i]);
            }
            return copy;
        }

        // Handle Object
        if (obj instanceof Object) {
            copy = {};
            for (var attr in obj) {
                if (obj.hasOwnProperty(attr)) copy[attr] = clone(obj[attr]);
            }
            return copy;
        }
        throw new Error("Unable to copy obj! Its type isn't supported.");
    }
    //For data storage key
    mGlobal["DataStorage"] = {}
    // Clear the session cookie

    String.prototype.replaceAll = function(search, replace){
        return this.split(search).join(replace);
    }
    mGlobal.GeneralGenerateHTMLCodeHandlebars=function(inInnerTemplateSelector,inData) {
        lHTMLTemplate=$(inInnerTemplateSelector)[0].innerHTML
        //console.log(lHTMLTemplate)
        //Компиляция
        var template = Handlebars.compile(lHTMLTemplate);
        //Вставка данных
        var lHTMLResult = template(inData);
        return lHTMLResult
    }
    mGlobal.GeneralGenerateHTMLCode=function(inTemplateHTMLSelector,inItemDictionary,inKeywordPrefix="::",inKeywordPostfix="::") {
        ///Получить заготовку
        lTemplateHTMLCode=$(inTemplateHTMLSelector)[0].outerHTML
        ///Определить ключь экранирования специальных ключевых слов
        ///Выполнить циклические замены, если там есть пожходящие ключи
        lResultHTMLCode=lTemplateHTMLCode
        for(var lKey in inItemDictionary) {
            lHTMLKey=inKeywordPrefix+lKey+inKeywordPostfix;
            lResultHTMLCode=lResultHTMLCode.replaceAll(lHTMLKey,inItemDictionary[lKey])
        }
        ///Вернуть результат
        return lResultHTMLCode
    }
    //////////////////////////
    /////Info JS module
    //////////////////////////
    mGlobal.Info={};

    mGlobal.Info.TableActivityLogScheduleListRefresh=function() {

    }
    //////////////////////////
    /////Controller JS module
    //////////////////////////
    mGlobal.Controller={};

    mGlobal.Controller.CMDRunText=function(inCMDText) {
        ///Подготовить конфигурацию
        lData = [
            {"Type":"CMDStart", "Command": inCMDText}
        ]
        ///Обнулить таблицу
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3){},
            dataType: "text"
        });
    }
    mGlobal.Controller.CMDRun=function() {
        ///Обнулить таблицу
        lCMDCode=$(".openrpa-controller-cmd-run-input")[0].value
        ///Подготовить конфигурацию
        lData = [
            {"Type":"CMDStart", "Command": lCMDCode }
        ]
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                ///Отправить запрос на формирование таблицы
                //lHTMLCode=console.log("CMDRun result: "+lResponseJSON[0].result)
            },
            dataType: "text"
        });
    }
    mGlobal.Controller.CMDRunGUILogout=function() {
        ///Обнулить таблицу
        lCMDCode="for /f \"skip=1 tokens=2\" %s in ('query user %USERNAME%') do (tscon  \\dest:console)"
        //lCMDCode = lCMDCode.replace(/\\n/g, "\\n")
        //                  .replace(/\\'/g, "\\'")
        //                  .replace(/\\"/g, '\\"')
        //                  .replace(/\\&/g, "\\&")
        //                  .replace(/\\r/g, "\\r")
        //                  .replace(/\\t/g, "\\t")
        //                  .replace(/\\b/g, "\\b")
        //                  .replace(/\\f/g, "\\f")
        //				  .replace('"', "\\\"");
        ///Подготовить конфигурацию
        lData = [
            {"Type":"CMDStart", "Command": lCMDCode }
        ]
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                ///Отправить запрос на формирование таблицы
                //lHTMLCode=console.log("CMDRun result: "+lResponseJSON[0].result)
            },
            dataType: "text"
        });
    }
    ///Restart PC
    mGlobal.Controller.PCRestart = function () {
        mGlobal.Controller.CMDRunText("shutdown -r")
    }
    ///Orchestrator save session
    mGlobal.Controller.OrchestratorSessionSave=function() {
        ///Подготовить конфигурацию
        lData = [
            {"Type":"OrchestratorSessionSave"}
        ]
        $.ajax({
          type: "POST",
          url: 'Utils/Processor',
          data: JSON.stringify(lData),
          success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
            },
          dataType: "text"
        });
    }
    ///Перезагрузить Orchestrator
    mGlobal.Controller.OrchestratorRestart=function() {
        ///Подготовить конфигурацию
        lData = [
            {"Type":"OrchestratorRestart"}
        ]
        $.ajax({
          type: "POST",
          url: 'Utils/Processor',
          data: JSON.stringify(lData),
          success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
            },
          dataType: "text"
        });
    }
    mGlobal.Controller.OrchestratorGITPullRestart = function() {
        mGlobal.Controller.OrchestratorSessionSave() //Save current RDP list session
        mGlobal.Controller.CMDRunText("timeout 3 & taskkill /f /im OpenRPA_Orchestrator.exe & timeout 2 & cd "+mGlobal.WorkingDirectoryPathStr+" & git reset --hard & git pull & pyOpenRPA.Orchestrator_x64_administrator_startup.cmd");
    }
    //////////////////////////
    /////Monitor JS module
    //////////////////////////
    mGlobal.Monitor={};
    mGlobal.Monitor.ScreenshotModal={};
    mGlobal.Monitor.GenerateUniqueID=function(inPrefix="tempUID=") {
        return inPrefix+Math.round(Math.random()*1000)+"-"+Math.round(Math.random()*10000)+"-"+Math.round(Math.random()*1000)
    }
    //inHostURI: http://localhost:8081
    mGlobal.Monitor.ScreenshotModal.Show=function(inHostURI="	") {
        $('.ui.modal.daemon-screenshot').modal('show');

        //Функция обновления картинки
        lScreenshotUpdate=function() {
            lScreenshotSrc=inHostURI+"/GetScreenshot?"+mGlobal.Monitor.GenerateUniqueID()
            $(".daemon-screenshot img").attr('src', lScreenshotSrc);
        }

        mGlobal.Monitor.ScreenshotModal.timerId=setInterval(lScreenshotUpdate,1500)
    }
    mGlobal.Monitor.ScreenshotModal.Close=function() {
        clearInterval(mGlobal.Monitor.ScreenshotModal.timerId);
    }
    ///Monitor
    mGlobal.Monitor.DaemonList={}
    mGlobal.Monitor.DaemonList.fRefreshTable=function() {
        ///Загрузка данных
        $.ajax({
          type: "GET",
          url: 'Monitor/JSONDaemonListGet',
          data: '',
          success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                ///Сформировать HTML код новой таблицы
                lHTMLCode=mGlobal.GeneralGenerateHTMLCodeHandlebars(".openrpa-hidden-monitor-table-general",lResponseJSON)
                ///Очистить дерево
                //mGlobal.ElementTree.fClear();
                ///Прогрузить новую таблицу
                $(".openrpa-monitor").html(lHTMLCode)
            },
          dataType: "text"
        });
    }
    ////////////////////////////////
    ///////Control panel
    ///////////////////////////////
    ///Refresh control panel
    function sleep(ms) {
        ms += new Date().getTime();
        while (new Date() < ms){}
    }
    function uuidv4() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    mGlobal.SessionGUIDStr = uuidv4() // Generate uuid4 of the session
    //console.log(uuidv4());
    mGlobal.RobotRDPActive = {}
    mGlobal.Monitor.fControlPanelRefresh_TechnicalRender = function()
    {
        lResponseJSON = mGlobal.Monitor.mDatasetLast
        if (lResponseJSON!= null) {
            ///Escape onclick
            /// RenderRobotList
            lResponseJSON["RenderRobotList"].forEach(
                function(lItem){
                    if ('FooterButtonX2List' in lItem) {
                        /// FooterButtonX2List
                        lItem["FooterButtonX2List"].forEach(
                            function(lItem2){
                                if ('OnClick' in lItem) {
                                    lOnClickEscaped = lItem["OnClick"];
                                    lOnClickEscaped = lOnClickEscaped.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
                                    lItem["OnClick"] = lOnClickEscaped;
                                }
                            }
                        );
                        /// FooterButtonX1List
                        lItem["FooterButtonX1List"].forEach(
                            function(lItem2){
                                if ('OnClick' in lItem) {
                                    lOnClickEscaped = lItem["OnClick"];
                                    lOnClickEscaped = lOnClickEscaped.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
                                    lItem["OnClick"] = lOnClickEscaped;
                                }
                            }
                        );
                    }
                }
            );
            //////////////////////////////////////////////////////////
            ///Сформировать HTML код новой таблицы - контрольная панель
            lHTMLCode=mGlobal.GeneralGenerateHTMLCodeHandlebars(".openrpa-hidden-control-panel",lResponseJSON)
            //Присвоить ответ в mGlobal.Monitor.mResponseList
            mGlobal.Monitor.mResponseList = lResponseJSON
            ///Set result in mGlobal.DataStorage
            lResponseJSON["RenderRobotList"].forEach(
                function(lItem){
                    if ('DataStorageKey' in lItem) {
                        mGlobal["DataStorage"][lItem['DataStorageKey']]=lItem
                    }
                }
            )
            ///Прогрузить новую таблицу
            $(".openrpa-control-panel").html(lHTMLCode)
            ////////////////////////////////////////////////////
            ///Сформировать HTML код новой таблицы - список RDP
            lHTMLCode=mGlobal.GeneralGenerateHTMLCodeHandlebars(".openrpa-hidden-robotrdpactive-control-panel",lResponseJSON)
            //Присвоить ответ в mGlobal.RobotRDPActive.mResponseList
            mGlobal.RobotRDPActive.mResponseList = lResponseJSON
            ///Прогрузить новую таблицу
            $(".openrpa-robotrdpactive-control-panel").html(lHTMLCode)
            ///Очистить дерево
            //mGlobal.ElementTree.fClear();
        }
    }
    mGlobal.Monitor.mDatasetLast = null
    mGlobal.Monitor.fControlPanelRefresh=function() {
        try {
            //var XHR = new XMLHttpRequest();
            //XHR.setRequestHeader("Cookies",document.cookie)
            ///Загрузка данных
            //console.log("Request is sent")
            //console.log(document.cookie)
            $.ajax({
                type: "GET",
                headers: {"SessionGUIDStr":mGlobal.SessionGUIDStr},
                url: 'Monitor/ControlPanelDictGet',
                data: '',
                //cache: false,
                //xhr: XHR,
                success: function(lData,l2,l3) {
                    try {
                        var lResponseJSON=JSON.parse(lData)
                        mGlobal.Monitor.mDatasetLast = lResponseJSON
                        mGlobal.Monitor.fControlPanelRefresh_TechnicalRender()
                    }
                    catch(error) {
                    }
                    mGlobal.Monitor.fControlPanelRefresh() // recursive
                },
                dataType: "text",
                error: function(jqXHR, textStatus, errorThrown ) {
                    sleep(3000)
                    mGlobal.Monitor.fControlPanelRefresh() // recursive
                }
            });
        }
        catch(error) {
            sleep(3000)
            mGlobal.Monitor.fControlPanelRefresh() // recursive
        }
        //mGlobal.Monitor.fControlPanelRefresh() // recursive
    }
    mGlobal.Monitor.fControlPanelRefresh()
    mGlobal.Test=function() {
        ///Обнулить таблицу
        lData = [
            {
                "Type":"GlobalDictKeyListValueSet",
                "key_list":["Storage","Robot_R01"],
                "value":{
                    "RunDateTimeString":"Test1",
                    "StepCurrentName":"Test2",
                    "StepCurrentDuration":"Test3"
                }
            }
        ]
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                //console.log(lData)
            },
            dataType: "text"
        });
    }
    ///////////////////////////////
    ///Processor functions
    ///////////////////////////////
    mGlobal.Processor = {}
    mGlobal.Processor.ServerValueAppend = function(inKeyList,inValue) {
        lData = [
            {
                "Type":"GlobalDictKeyListValueAppend",
                "KeyList": inKeyList,
                "Value": inValue
            }
        ]
        ///Обнулить таблицу
        $('.ui.modal.basic .content').html("");
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                ///TODO Show error if exist error
            },
            dataType: "text"
        });
    }
    mGlobal.Processor.ServerValueSet = function(inKeyList,inValue) {
        lData = [
            {
                "Type":"GlobalDictKeyListValueSet",
                "KeyList": inKeyList,
                "Value": inValue
            }
        ]
        ///Обнулить таблицу
        $('.ui.modal.basic .content').html("");
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                ///TODO Show error if exist error
            },
            dataType: "text"
        });
    }
    mGlobal.Processor.ServerValueOperatorPlus = function(inKeyList,inValue) {
        lData = [
            {
                "Type":"GlobalDictKeyListValueOperator+",
                "KeyList": inKeyList,
                "Value": inValue
            }
        ]
        ///Обнулить таблицу
        $('.ui.modal.basic .content').html("");
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                ///TODO Show error if exist error
            },
            dataType: "text"
        });
    }
    mGlobal.Processor.Send = function(inData) {
        lData = inData
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                ///TODO Show error if exist error
            },
            dataType: "text"
        });
    }
    mGlobal.Server= {}
    mGlobal.Server.JSONGet=function(inMethod, inURL, inDataJSON, inCallback)
    {
        $.ajax({
            type: inMethod,
            url: inURL,
            data: JSON.stringify(inDataJSON),
            success:
            function(lData,l2,l3)
            {
                var lResponseJSON=JSON.parse(lData)
                inCallback(lResponseJSON)
            },
            dataType: "text"
        });
    }

    /////////////////
    ///Modal
    ///////////////////
    mGlobal.Modal={}
    /////////////////////////////////////////////////////
    mGlobal.Modal.TableFilter={}
    mGlobal.Modal.TableFilter.Show=function(inJSON) {
        //{
        //	"Title":"",
        //	"Headers":["Header1","Header2"],
        //	"Rows": [["Cell1","Cell2"],["Cell2-1","Cell2-2"]],
        //	"FilterOnKeyUp": "<JS Code>" //Fill here in function
        //}
        //Set js handler to Search field
        inJSON["FilterOnKeyUp"]="mGlobal.Modal.TableFilter.FilterUpdate(this.value);"
        ///Set value
        mGlobal.Modal.TableFilter.mDataJSON = inJSON
        //Render HTML
        lHTMLCode=mGlobal.GeneralGenerateHTMLCodeHandlebars(".openrpa-handlebar-template-table-filter",inJSON);
        ///Установить HTML код
        $('.ui.modal.basic .content').html(lHTMLCode);
        $('.ui.modal.basic').modal('show');
        //DO widest modal for table with scroll x
        $("div.ui.basic.modal.transition.visible.active.scrolling")[0].style["width"]="1300px"
        $("div.ui.basic.modal.transition.visible.active.scrolling")[0].style["overflow"]="scroll"
    }
    //Service function
    mGlobal.Modal.TableFilter.FilterUpdate=function(inFilterValue) {
        //Get JSON, apply filter, clone data
        lDataJSON = clone(mGlobal.Modal.TableFilter.mDataJSON)
        delete lDataJSON["Rows"]
        lDataJSON["Rows"]=[]
        //Filter code [any occurence in the row is ok for push! ]
        mGlobal.Modal.TableFilter.mDataJSON["Rows"].forEach(
            function(inElement) {
                lFlagElementAppend = false
                inElement.forEach(
                    function(inElement2) {
                        if (String(inElement2).includes(inFilterValue)) {
                            lFlagElementAppend = true
                        }
                    }
                )
                if (lFlagElementAppend) {
                    lDataJSON["Rows"].push(inElement)
                }
            }
        )
        //Clear Filter Title property (fixed in html)
        delete lDataJSON["FilterOnKeyUp"]
        delete lDataJSON["Title"]
        //Search the table element [replace only table html]
        lElement = $('.ui.modals.active .content table.table')[0]
        lElementParentElement = lElement.parentNode
        lElement.parentNode.removeChild(lElement);
        //Render HTML
        lHTMLCode=mGlobal.GeneralGenerateHTMLCodeHandlebars(".openrpa-handlebar-template-table-filter",lDataJSON);
        ///Установить HTML код
        lElementParentElement.insertAdjacentHTML("beforeend",lHTMLCode);
    }
    /////////////////////////////////////////////////////////////
    mGlobal.Modal.ListFilter={}
    mGlobal.Modal.ListFilter.Show=function(inJSON) {
        //{
        //	"Title":"",
        //	"List":[{"Header":"","Description":""}],
        //	"FilterOnKeyUp": "<JS Code>" //Fill here in function
        //}
        //Set js handler to Search field
        inJSON["FilterOnKeyUp"]="mGlobal.Modal.ListFilter.FilterUpdate(this.value);"
        ///Set value
        mGlobal.Modal.ListFilter.mDataJSON = inJSON
        //Render HTML
        lHTMLCode=mGlobal.GeneralGenerateHTMLCodeHandlebars(".openrpa-handlebar-template-list-filter",inJSON);
        ///Установить HTML код
        $('.ui.modal.basic .content').html(lHTMLCode);
        $('.ui.modal.basic').modal('show');
    }
    //Service function
    mGlobal.Modal.ListFilter.FilterUpdate=function(inFilterValue) {
        //Get JSON, apply filter, clone data
        lDataJSON = clone(mGlobal.Modal.ListFilter.mDataJSON)
        delete lDataJSON["List"]
        lDataJSON["List"]=[]
        //Filter code [any occurence in the row is ok for push! ]
        mGlobal.Modal.ListFilter.mDataJSON["List"].forEach(
            function(inElement) {
                lFlagElementAppend = false
                if (String(inElement["Header"]).includes(inFilterValue)) {
                    lFlagElementAppend = true
                }
                if (String(inElement["Description"]).includes(inFilterValue)) {
                    lFlagElementAppend = true
                }
                if (lFlagElementAppend) {
                    lDataJSON["List"].push(inElement)
                }
            }
        )
        //Clear Filter Title property (fixed in html)
        delete lDataJSON["FilterOnKeyUp"]
        delete lDataJSON["Title"]
        //Search the table element [replace only table html]
        lElement = $('.ui.modals.active .content div.ui.inverted.segment')[0]
        lElementParentElement = lElement.parentNode
        lElement.parentNode.removeChild(lElement);
        //Render HTML
        lHTMLCode=mGlobal.GeneralGenerateHTMLCodeHandlebars(".openrpa-handlebar-template-list-filter",lDataJSON);
        ///Установить HTML код
        lElementParentElement.insertAdjacentHTML("beforeend",lHTMLCode);
    }
    mGlobal.UserRoleHierarchyDict = null // Put here the user role hierarchy
    // UAC Ask
    mGlobal.UserRoleAsk=function(inList) {
        var lResult = true; // Init flag
        var lRoleHierarchyDict = mGlobal.UserRoleHierarchyDict; // get the Hierarchy
        // Try to get value from key list
        var lKeyValue = lRoleHierarchyDict; // Init the base
        var lListLength = inList.length;
        for (var i = 0; i<lListLength; i++) {
            var lItem = inList[i]; // get the item
            if (typeof lKeyValue == "object") {
                if (lItem in lKeyValue) { // Has key
                    lKeyValue = lKeyValue[lItem]; // Get the value and go to the next loop iteration
                } else { // Else branch - true or false
                    if (Object.keys(lKeyValue).length > 0) { // false - if Dict has some elements
                        lResult = false; // Set the False Flag
                    } else {
                        lResult = true; // Set the true flag
                    }
                    break; // Stop the loop
                }
            } else { // Has element with no detalization - return true
                lResult = true; // Set the flag
                break; // Close the loop
            }
        }
        return lResult; // Return the result
    }
    // Check user roles and update the Orchestrator UI
    mGlobal.UserRoleUpdate=function() {
        $.ajax({
            type: "POST",
            url: 'Orchestrator/UserRoleHierarchyGet',
            data: "",
            success:
            function(lData,l2,l3)
            {
                var lUACAsk = mGlobal.UserRoleAsk // Alias
                var lResponseDict=JSON.parse(lData)
                mGlobal.UserRoleHierarchyDict = lResponseDict // set the user role hierarchy
                //Turn on the Lookmachine screenshot button
                if (lUACAsk(["Orchestrator","Controls","LookMachineScreenshots"])) {
                    $(".openrpa-control-lookmachinescreenshot").show() //Show button
                }
                //Turn on the restart orchestrator button
                if (lUACAsk(["Orchestrator","Controls","RestartOrchestrator"])) {
                    $(".openrpa-control-restartorchestrator").show() //Show button
                }
                //Turn on the rdp session list
                if (lUACAsk(["Orchestrator","RDPActive","ListRead"])) {
                    $(".openrpa-rdpactive-title").show() //Show section
                    $(".openrpa-robotrdpactive-control-panel-general").show() //Show section
                }
                //Turn on the restart PC button
                if (lUACAsk(["Orchestrator","Controls","RestartPC"])) {
                    $(".openrpa-control-restartpc").show() //Show button
                }
                //Turn on the git update + restart orchestrator
                if (lUACAsk(["Orchestrator","Controls","GITRestartOrchestrator"])) {
                    $(".openrpa-control-gitrestartorchestrator").show() //Show button
                }
            },
            dataType: "text"
        });
    }
    mGlobal.UserRoleUpdate() // Cal the update User Roles function
    // Orchestrator model
    mGlobal.WorkingDirectoryPathStr = null
    mGlobal.OrchestratorModelUpdate=function() {
        lData = [
            {
               "Type": "GlobalDictKeyListValueGet",
               "KeyList": ["Server","WorkingDirectoryPathStr"]
            }
        ]
        $.ajax({
            type: "POST",
            url: 'Utils/Processor',
            data: JSON.stringify(lData),
            success:
            function(lData,l2,l3)
            {
                var lUACAsk = mGlobal.UserRoleAsk // Alias
                var lResponseList=JSON.parse(lData)
                mGlobal.WorkingDirectoryPathStr = lResponseList[0]["Result"]
            },
            dataType: "text"
        });
    }
    mGlobal.OrchestratorModelUpdate() // Cal the update orchestrator model
});