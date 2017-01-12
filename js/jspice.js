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
	kernel:''
    };

    //////////////////////////////////////////////////////////////
    //UTIL
    //////////////////////////////////////////////////////////////
    function clearResponse(response){
	response=response.replace(/'/g,"\"");
	response=response.replace(/<stdout>/g,"");
	response=response.replace(/<stderr>/g,"");
	response=response.replace(/<[^<]+>/g,"\"\"");
	response=response.replace(/None/g,"\"\"");
	response=response.replace(/\n/g," ");
	return response;
    }

    function updateKernel(response){
	response=clearResponse(response);
	console.log("Complete answer:"+response);
	jspice.kernel=JSON.parse(response);
    }
    
    //////////////////////////////////////////////////////////////
    //JSPICE INITIALIZE
    //////////////////////////////////////////////////////////////
    jspice.init=function(url){

	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//SERVER URL
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	this.url=url;

	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//SESSIONID
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	this.SESSIONID=readCookie("SESSIONID");
	if(!this.SESSIONID){
	    this.SESSIONID=randomString(20);
	    createCookie("SESSIONID",this.SESSIONID,1);
	}

	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	//KERNEL INDICATOR
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	/*
	var indicator=document.createElement('div');
	$(indicator).
	    addClass('jsp jsp-indicator').
	    html('Powered by jSpice').
	    appendTo($("body"));

	//var submission=this.submit("now=spy.jutcnow()");
	var submission=this.submit("a=1;print a");
	//var submission=this.submit("now=spy.jutcnow()");
	submission.done(function(data){
	    $('.jsp-indicator').css('background','green');
	    updateKernel(data.response);
	    console.log(jspice.kernel.now);
	});
	*/
    };

    jspice.submit=function(code,success=function(){},error=function(){}){
	/*
	  If you want to recover values as JS object
	  var response=clearResponse(data.response);
	*/
	var submission=$.ajax({
	    type:'POST',
	    url:this.url+'/server/cgi-bin/jspice.client.cgi',
	    data:{code:code},
	    async:false,
	    dataType:'jsonp',
	    headers:{'Access-Control-Allow-Origin': '*'},
	});
	return submission;
    };

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

