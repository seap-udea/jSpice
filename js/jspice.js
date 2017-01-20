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
//JSPICE CONFIGURATION
//######################################################################

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//GLOBAL VARIABLES
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
HEALTH_TIMEOUT=null;

//######################################################################
//MODULE PATTERN OF JSPICE
//######################################################################
var jspice=(function($){
    
    var jspice={
	version: '0.1',
	verbose_depth: 0
    };

    //////////////////////////////////////////////////////////////
    //JSPICE INITIALIZE
    //////////////////////////////////////////////////////////////
    jspice.init=function(parameters={}){

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

		//Type of session: nosession, dynamic, unique
		session_type:"dynamic",

		//Time between health signals in seconds
		session_timeout:1.0,

		//Verbose depth: 1: shallow, 2: medium, 3: depth
		verbose_depth:1
	    },parameters);

	//Create jSpice indicator
	jspice.log(["Parameters:",parameters],0,"init");
	var keys=Object.keys(parameters);
	for(var i=0;i<keys.length;i++) this[keys[i]]=parameters[keys[i]];
	jspice.log(["Basic properties:",this],2,"init");

	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//SESSION INFORMATION
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	var namecookie="sessionid_"+pageName();
	jspice.sessionid=readCookie(namecookie);
	if(!jspice.sessionid){
	    jspice.sessionid=randomString(20);
	    createCookie(namecookie,jspice.sessionid,1);
	    jspice.log("New session",1,"init");
	}else{
	    jspice.log("Session recovered",1,"init");
	}
	jspice.log("Session ID:"+jspice.sessionid,1,"init");
	$('#sessionid').html(jspice.sessionid)

	
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//JSPICE PRIVATE PROPERTIES
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	jspice.server_http="http://"+jspice.server_fqdn+"/jSpice"
	jspice.proxy_http="http://"+jspice.proxy_fqdn+"/jSpice"
	jspice.session_cgi=jspice.server_http+"/cgi-bin/jspice.session.cgi";
	jspice.proxy_cgi=jspice.proxy_http+"/cgi-bin/jspice.proxy.cgi";
	jspice.direct_cgi=jspice.proxy_http+"/cgi-bin/jspice.direct.cgi";
	
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//START SESSION
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//Get server configuration
	jspice.run({url:jspice.server_http+"/jspice.cfg",
		    type:'GET',
		    jsonpCallback:'jsonpCallback'})
	    .done(function(d){
		jspice.session_timeout=d.session_timeout;
		jspice.log("Session timeout:"+jspice.session_timeout,0,"init");
	    });

	var session_handler;
	switch(jspice.session_type){
	    case "dynamic":{
		jspice.log("Session dynamic");
		session_handler=jspice.startSession(jspice.sessionid,jspice.proxy,5502);
		break;
	    }
	    case "unique":{
		jspice.log("Session unique");
		session_handler=jspice.startSession("0","127.0.0.1",5500);
		break;
	    }
	    case "nosession":{
		jspice.log("No session");
		session_handler={done:function(func){func();}};
		break;
	    }
	}
		

	jspice.log(["Properties after initialization:",this],0,"init");
	return session_handler;
    };

    //////////////////////////////////////////////////////////////
    //BASIC METHODS
    //////////////////////////////////////////////////////////////
    jspice.log=function(text,depth=1,section="main"){
	if(depth>jspice.verbose_depth) return 0;
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
		    "["+section+"] "+message);
    };

    jspice.run=function(parameters={}){
	var parameters=$.extend(
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

    jspice.command=function(code="jspice=True"){
	code=stringCompact(code);
	jspice.log("Executing:"+code,3,"command");
	var parameters={
	    url:jspice.proxy_cgi,
	    data:{sessionid:jspice.sessionid,
		  server:jspice.server,
		  port:jspice.port,
		  code:code
		 },
	    type:"POST",
	    success:function(result){
		jspice.output=jspice.decodeMsg(result.response);
		jspice.log(["Command output:",jspice.output],3,"command");
	    },
	    error:function(){
		jspice.healthCheck(false);
	    }
	};
	handler=jspice.run(parameters);
	return handler;
    };

    jspice.command_direct=function(code="jspice=True"){
	code=stringCompact(code);
	jspice.log("Executing:"+code,3,"command");
	var parameters={
	    url:jspice.direct_cgi,
	    data:{sessionid:jspice.sessionid,
		  server:jspice.server,
		  port:jspice.port,
		  code:code
		 },
	    type:"POST",
	    success:function(result){
		jspice.output=jspice.decodeMsg(result.response);
		jspice.log(["Command output:",jspice.output],3,"command");
	    },
	};
	handler=jspice.run(parameters);
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
		       jspice.log("Session healthy",1,"health");
		       $(jspice.indicator).css('background','darkgreen');
		   })
		   .fail(function(d,t,e){
		       jspice.log("Session passed away",1,"health");
		       $(jspice.indicator).css('background','red');
		       if(HEALTH_TIMEOUT) clearTimeout(HEALTH_TIMEOUT);
		   });
	if(qrepeat){
	    var timeout=1000*jspice.session_timeout*60/4;
	    jspice.log("Timeout:"+timeout,2,"health");
	    HEALTH_TIMEOUT=setTimeout(jspice.healthCheck,timeout);
	}
    };

    jspice.startSession=function(sessionid=jspice.sessionid,proxy=jspice.proxy,port=5501){
	jspice.log("Starting session "+sessionid,1,"start");
	var handler=jspice.run({
	    url:jspice.session_cgi,
	    data:{sessionid:sessionid,
		  proxy:proxy,
		  port:port},
	    type:'POST',
	    success:function(d){
		jspice.port=d.port;
		jspice.log("Session port:"+jspice.port,0,"init");
	    }
	}).done(function(x,t,e){
	    jspice.log("Session "+sessionid+" started with proxy "+proxy,1,"start");
	    //Place indicator
	    jspice.indicator=document.createElement('div');
	    $(jspice.indicator).
		addClass('jsp jsp-indicator').
		html('Powered by <a href="https://github.com/seap-udea/jSpice" target="_blank">jSpice</a>').
		appendTo($("body"));
	    //Launch health checker
	    jspice.healthCheck();
	});
	return handler;
    };

    jspice.stopSession=function(){
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
		if(HEALTH_TIMEOUT) clearTimeout(HEALTH_TIMEOUT);
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
	jmsg=JSON.parse(msg);
	return jmsg;
    };

    jspice.getValue=function(data){
	obj=data.response;
    };

    jspice.UTCnow=function(){
	var dfecha=new Date();
	var mes=dfecha.getUTCMonth()+1;
	var fecha=mes+'/'+dfecha.getUTCDate()+'/'+dfecha.getUTCFullYear()+' '+dfecha.getUTCHours()+':'+dfecha.getUTCMinutes()+':'+dfecha.getUTCSeconds();
	return fecha;
    }

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
function pageName(){
    var pname=location.pathname.substring(location.pathname.lastIndexOf("/") + 1);
    return pname;
}

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

function stringCompact(msg){
    var msgcomp=msg;
    //msgcomp=msgcomp.replace(/\n/gm,"\\n")
    //msgcomp=msgcomp.replace(/\t/gm,"\\t")
    //msgcomp=msgcomp.replace(/\s+(?=([^"^']*"[^"^']*["'])*[^"^']*$)/gm,"")
    return msgcomp;
}

//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
//PYTHON SANDBOXING
//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function array(vector){return vector;}
var True=true
var False=false
