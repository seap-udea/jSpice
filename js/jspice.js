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
	$('#sessionid').html(jspice.sessionid)

	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//CONSTRUCTOR PARAMETERS
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	parameters=$.extend(
	    {
		//Default parameters
		server_fqdn:"localhost",
		server:"127.0.0.1",
		slave_fqdn:"localhost",
		slave:"127.0.0.1",
		sessiontype:"dynamic"
	    },parameters);
	jspice.log(["Parameters:",parameters],"init");
	var keys=Object.keys(parameters);
	for(var i=0;i<keys.length;i++) this[keys[i]]=parameters[keys[i]];
	jspice.log(["Basic properties:",this],"init");
	
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//JSPICE PRIVATE PROPERTIES
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	var _server_http="http://"+jspice.server_fqdn+"/jSpice"
	var _slave_http="http://"+jspice.slave_fqdn+"/jSpice"
	jspice.session_cgi=_server_http+"/cgi-bin/jspice.session.cgi";
	jspice.executor_cgi=_slave_http+"/cgi-bin/jspice.executor.cgi";
	
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//START SESSION
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	var _session_handler=jspice.run({
	    url:jspice.session_cgi,
	    data:{sessionid:jspice.sessionid,
		  slave:jspice.slave,
		  port:5501},
	    type:'POST',
	    success:function(d){
		jspice.port=d.port;
	    }
	});

	//Initialize
	_session_handler.done(function(x,t,e){

	    //Place indicator
	    jspice.indicator=document.createElement('div');
	    $(jspice.indicator).
		addClass('jsp jsp-indicator').
		html('Powered by jSpice').
		appendTo($("body"));

	    //jspice.healthCheck();
	    
	    //Launch health checker
	    jspice.run({
		url:jspice.executor_cgi,
		data:{sessionid:jspice.sessionid,
		      server:jspice.server,
		      port:jspice.port,
		      //code:"f=lambda x:np.exp(x)",
		      code:"y=f(4)"
		     },
		type:'POST'
	    }).done(function(d,t,e){
		var x=JSON.parse(d.response);
		jspice.log(x);
	    });
	});
	return _session_handler;

	/*
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//INITIALIZE
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	jspice.kernel=jspice.http+"/cgi-bin/jspice.launchkernel.cgi";
	jspice.client=jspice.http+"/cgi-bin/jspice.client.cgi";

	jspice.log("Server:"+jspice.server,"init");
	jspice.log("Slave:"+jspice.slave,"init");

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
    jspice.run=function(parameters={}){
	parameters=$.extend(
	    {
		url:location.host,
		data:{},
		type:'GET',
		dataType:'jsonp',
		headers:{'Access-Control-Allow-Origin': '*'},
	    },parameters);
	//jspice.log(["AJAX Parameters:",parameters]);
	var handler=$.ajax(parameters);
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
	    if(typeof(text)=='object') message=JSON.stringify(text,null,4);
	    else message=text;
	}
	var now=new Date();
	console.log("["+now.toLocaleString()+"] "+
		    "["+instance+"] "+
		    "["+section+"] "+message);
    };

    jspice.healthCheck=function(){
	jspice.run({
	    url:jspice.executor_cgi,
	    data:{sessionid:jspice.sessionid,
		  server:jspice.server,
		  port:jspice.port,
		  code:"jspice=True"
		 },
	    type:"POST"
	})
		   .done(function(d,t,e){
		       jspice.log("Session healthy");
		       $(jspice.indicator).css('background','blue');
		   })
		   .fail(function(d,t,e){
		       jspice.log("Session passed away");
		       $(jspice.indicator).css('background','red');
		   });
	//setTimeout(jspice.healthCheck,1000);
    }

    //////////////////////////////////////////////////////////////
    //UTIL
    //////////////////////////////////////////////////////////////
    function clearResponse(response){
	response=response.replace(/'/g,'"');
	response=response.replace(/<\w+>/g,'');
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
