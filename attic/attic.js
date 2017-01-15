		jspice.run({
		    url:jspice.executor_cgi,
		    data:{sessionid:jspice.sessionid,
			  server:jspice.server,
			  port:jspice.port,
			  //code:"f=lambda x:np.exp(x)",
			  //code:"y=np.array([1,2,3])"
			  //code:"z=f(4)"
			  //code:"w=2*v"
			  code:"w=np.zeros((3,3))"
			 },
		    type:'POST'
		}).done(function(d,t,e){
		    console.log(d.response);
		    var x=jspice.decodeMsg(d.response);
		    var y=eval(x.y);
		    var w=eval(x.w);
		    jspice.log(x);
		    jspice.log(y);
		    jspice.log(w[0]);
		});
