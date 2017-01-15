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

		//Fully qualified name of the jSpice server
		server_fqdn:"localhost",
		//IP of the jSpice server
		server:"127.0.0.1",

		//Fully qualified name of the jSpice proxy
		proxy_fqdn:"localhost",
		//IP of the jSpice proxy
		proxy:"127.0.0.1",

		//Type of session: dynamic, unique
		sessiontype:"dynamic",

		//Time between health signals in seconds
		health_time:60.0,
	    },parameters);

	//Create jSpice indicator
	jspice.log(["Parameters:",parameters],"init");
	var keys=Object.keys(parameters);
	for(var i=0;i<keys.length;i++) this[keys[i]]=parameters[keys[i]];
	jspice.log(["Basic properties:",this],"init");
	
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//JSPICE PRIVATE PROPERTIES
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	var _server_http="http://"+jspice.server_fqdn+"/jSpice"
	var _proxy_http="http://"+jspice.proxy_fqdn+"/jSpice"
	jspice.session_cgi=_server_http+"/cgi-bin/jspice.session.cgi";
	jspice.proxy_cgi=_proxy_http+"/cgi-bin/jspice.proxy.cgi";
	
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//START SESSION
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	_session_handler=jspice.startKernel();
	jspice.log(["Properties after initialization:",this],"init");
	return _session_handler;
    };

    //////////////////////////////////////////////////////////////
    //BASIC METHODS
    //////////////////////////////////////////////////////////////
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

    jspice.run=function(parameters={}){
	parameters=$.extend(
	    {
		url:jspice.proxy_cgi,
		data:{},
		type:'POST',
		dataType:'jsonp',
		headers:{'Access-Control-Allow-Origin': '*'},
	    },parameters);
	var handler=$.ajax(parameters);
	return handler;
    };

    jspice.healthCheck=function(qrepeat=true){
	jspice.run({
	    url:jspice.proxy_cgi,
	    data:{sessionid:jspice.sessionid,
		  server:jspice.server,
		  port:jspice.port,
		  code:"jspice=True"
		 },
	    type:"POST"
	})
		   .done(function(d,t,e){
		       jspice.log("Session healthy");
		       $(jspice.indicator).css('background','darkgreen');
		   })
		   .fail(function(d,t,e){
		       jspice.log("Session passed away");
		       $(jspice.indicator).css('background','red');
		   });
	if(qrepeat)
	    setTimeout(jspice.healthCheck,1000*jspice.health_time);
    };

    jspice.startKernel=function(){
	var _session_handler=jspice.run({
	    url:jspice.session_cgi,
	    data:{sessionid:jspice.sessionid,
		  proxy:jspice.proxy,
		  port:5501},
	    type:'POST',
	    success:function(d){
		jspice.port=d.port;
	    }
	}).done(function(x,t,e){
	    //Place indicator
	    jspice.indicator=document.createElement('div');
	    $(jspice.indicator).
		addClass('jsp jsp-indicator').
		html('Powered by jSpice').
		appendTo($("body"));
	    //Launch health checker
	    jspice.healthCheck();
	});
	return _session_handler;
    };

    jspice.stopKernel=function(){
	var parameters={
	    url:jspice.proxy_cgi,
	    data:{sessionid:jspice.sessionid,
		  server:jspice.server,
		  port:jspice.port,
		  code:"exit(0)"
		 },
	    type:"POST"
	};
	jspice.run(parameters)
	    .fail(function(){
		jspice.healthCheck(false);
	    });
    };
    
    //////////////////////////////////////////////////////////////
    //UTIL
    //////////////////////////////////////////////////////////////
    jspice.decodeMsg=function(msg){
 	msg=msg.replace(/"/g,'\\"');
	msg=msg.replace(/'/g,'"');
	msg=msg.replace(/\n/g,'');
	console.log(msg);
	jmsg=JSON.parse(msg);
	return jmsg;
    };

    return jspice;
}($));

//######################################################################
//ADDITIONAL ROUTINES
//######################################################################

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//COOKIES ROUTINES
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//OTHER ROUTINES
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function randomString(num) {
    var s = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    var random=Array(num).join().split(',').map(function(){ 
	return s.charAt(Math.floor(Math.random() * s.length)); 
    }).join('');
    return random;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//PYTHON SANDBOXING
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function array(vector){return vector;}
