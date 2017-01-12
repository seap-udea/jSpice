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

/*
  Module pattern
*/
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
	//KERNEL INDICATOR
	//%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
