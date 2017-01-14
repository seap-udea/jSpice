/*
#############################################################
#             /######            /##                        #
#            /##__  ##          |__/                        #
#        /##| ##  \__/  /######  /##  /#######  /######     #
#       |__/|  ######  /##__  ##| ## /##_____/ /##__  ##    #
#        /## \____  ##| ##  \ ##| ##| ##      | ########    #
#       | ## /##  \ ##| ##  | ##| ##| ##      | ##_____/    #
#       | ##|  ######/| #######/| ##|  #######|  #######    #
#       | ## \______/ | ##____/ |__/ \_______/ \_______/    #
#  /##  | ##          | ##                                  #
# |  ######/          | ##                                  #
#  \______/           |__/                                  #
#							    #
#                 Jorge I. Zuluaga (C) 2016		    #
#############################################################
Function: jSpice javascript library
#############################################################
*/

//######################################################################
//MODULE PATTERN OF JSPICE
//######################################################################
var jspice=(function($){
    
    var jspice={
	version: '0.1',
    };

    //////////////////////////////////////////////////////////////
    //JSPICE INITIALIZE
    //////////////////////////////////////////////////////////////
    jspice.init=function(parameters={}){

	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//SESSION INFORMATION
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	jspice.sessionid=readCookie("sessionid");
	if(!jspice.sessionid){
	    jspice.sessionid=randomString(20);
	    createCookie("sessionid",jspice.sessionid,1);
	    jspice.log("New session","init");
	}else{
	    jspice.log("Session recovered","init");
	}
	jspice.log("Session ID:"+jspice.sessionid,"init");

	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//CONSTRUCTOR PARAMETERS
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	parameters=$.extend(
	    {
		//Default parameters
		server:location.host,
		slave:location.host,
		kerneltype:"dynamic"
	    },parameters);
	jspice.log(["Parameters:",parameters],"init");
	var keys=Object.keys(parameters);
	for(var i=0;i<keys.length;i++) this[keys[i]]=parameters[keys[i]];
	jspice.log(["Basic properties:",this],"init");
	
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//JSPICE PRIVATE PROPERTIES
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	var _server_http="http://"+jspice.server+"/jSpice"
	var _slave_http="http://"+jspice.slave+"/jSpice"
	var _kernel_cgi=_server_http+"/cgi-bin/jspice.launchkernel.cgi";
	var _client_cgi=_server_http+"/cgi-bin/jspice.client.cgi";
	
	/*
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//INITIALIZE
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	jspice.kernel=jspice.http+"/cgi-bin/jspice.launchkernel.cgi";
	jspice.client=jspice.http+"/cgi-bin/jspice.client.cgi";

	jspice.log("Server:"+jspice.server,"init");
	jspice.log("Slave:"+jspice.slave,"init");

	jspice.indicator=document.createElement('div');
	$(jspice.indicator).
	    addClass('jsp jsp-indicator').
	    html('Powered by jSpice').
	    appendTo($("body"));

	jspice.initKernel();
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//INITIAL CHECKS
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//????????????????????????????????????????
	//Is there a port for jspice session?
	//????????????????????????????????????????
	jspice.portfile=jspice.http+'/sessions/'+jspice.sessionid+'/port'
	var filehandler=$.ajax({
	    url:jspice.portfile,
	    data:{},
	    type:"GET",
	    timeout:1000,
	    dataType:'jsonp',
	    headers:{'Access-Control-Allow-Origin': '*'},
	    jsonpCallback:'jsonpCallback'
	});
	//No, there is no port...
	filehandler.fail(function(x,t,e){
	    jspice.log("Port file not found. Executing new kernel.","filehandler fail");
	    //Then, start a new kernel...
	    jspice.kernelhandler=jspice.initKernel();
	    jspice.log(jspice,"init");
	});
	//Yes, there is a port...
	filehandler.done(function(d,t,e){
	    jspice.log("A port is available for jspice session.","filehandler done");

	    //Then, get the port
	    jspice.port=d.port;
	    jspice.log("Port for session: "+jspice.port,"filehandler done");

	    //????????????????????????????????????????
	    //Is the kernel still listening jspice port?
	    //????????????????????????????????????????
	    clienthandler=jspice.execCommand("jspice=True");

	    //Yes, the kernel is listening
	    clienthandler.done(function(d,t,e){
		jspice.log("Kernel is still listening in jspice port...","clienthandler done");
		jspice.log(jspice,"clienthandler done");
		jspice.isKernelAlive()
	    });

	    //No, the kernel is not listening anymore
	    clienthandler.fail(function(d,t,e){
		jspice.log("Kernel is not listening anymore...","clienthandler fail");
		
		//Then, start a new kernel...
		jspice.kernelhandler=jspice.initKernel();
		
		jspice.log(jspice.kernerlhandler,"clienthandler fail");
		
		jspice.kernerlhandler.fail(function(x,t,e){
		    jspice.log("Failed","kernelhandler fail");
		});

		jspice.log(jspice,"clienthandler fail");
		$(jspice.indicator).css('background','darkgreen');
	    });
	});
	*/
    };

    //////////////////////////////////////////////////////////////
    //BASIC METHODS
    //////////////////////////////////////////////////////////////
    jspice.initKernel=function(){
	handler=$.ajax({
	    url:jspice.kernel,
	    data:{sessionid:jspice.sessionid},
	    type:'POST',
	    dataType:'jsonp',
	    cache:false,
	    headers:{'Access-Control-Allow-Origin': '*'},
	});
	//jspice.isKernelAlive();
	handler.fail(function(x,t,e){
	    jspice.log(x);
	});
	handler.done(function(x,t,e){
	    jspice.log(x);
	});
	return handler;
    }

    jspice.execCommand=function(code){
	handler=$.ajax({
	    url:jspice.client,
	    data:{code:code,
		  sessionid:jspice.sessionid,
		  port:jspice.port},
	    type:"POST",
	    timeout:1000,
	    dataType:'jsonp',
	    headers:{'Access-Control-Allow-Origin': '*'},
	});
	return handler;
    };

    jspice.log=function(text,section="main",instance=jspice.sessionid){
	var message="";
	if(text instanceof Array){
	    for(var i=0;i<text.length;i++){
		var t=text[i];
		if(typeof(t)=='object') t=JSON.stringify(t,null,4);
		message+=t+" ";
	    }
	}else{
	    message=text;
	}
	var now=new Date();
	console.log("["+now.toLocaleString()+"] "+
		    "["+instance+"] "+
		    "["+section+"] "+message);
    };

    jspice.stopKernel=function(){
	jspice.execCommand("exit(0)");
	$(jspice.indicator).css('background','red');
    };
    jspice.startKernel=function(){
	handler=jspice.initKernel();
	setTimeout(jspice.isKernelAlive,1000);
    };
    jspice.isKernelAlive=function(){
	handler=jspice.execCommand("jspice=True");
	handler.fail(function(x,t,e){
	    jspice.log("Kernel is dead","isKernelAlive Fail");
	    $(jspice.indicator).css('background','red');
	});
	handler.done(function(x,t,e){
	    jspice.log("Kernel is alive in port "+jspice.port,"isKernelAlive Done");
	    $(jspice.indicator).css('background','darkgreen');
	    setTimeout(jspice.isKernelAlive,1000);
	});
    }

    //////////////////////////////////////////////////////////////
    //UTIL
    //////////////////////////////////////////////////////////////
    function clearResponse(response){
	response=response.replace(/'/g,'"');
	response=response.replace(/<stdout>/g,'');
	response=response.replace(/<stderr>/g,'');
	response=response.replace(/<[^<]+>/g,'""');
	response=response.replace(/None/g,'""');
	response=response.replace(/True/g,'true');
	response=response.replace(/False/g,'false');
	response=response.replace(/\n/g,' ');
	return response;
    }

    function updateKernel(response){
	response=clearResponse(response);
	jspice.log(response,"update");
	jspice.kernel=JSON.parse(response);
    }

    return jspice;
}($));

//######################################################################
//ADDITIONAL ROUTINES
//######################################################################
/*
  Source:
  https://www.daniweb.com/programming/web-development/threads/19283/how-to-save-session-values-in-javascript
*/
function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime()+(days*24*60*60*1000));
        var expires = "; expires="+date.toGMTString();
    }
    else var expires = "";
    document.cookie = name+"="+value+expires+"; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name,"",-1);
}

function randomString(num) {
    var s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    var random=Array(num).join().split(',').map(function(){ 
	return s.charAt(Math.floor(Math.random() * s.length)); 
    }).join('');
    return random;
}
