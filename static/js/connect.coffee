connect = ()->
	#console.log "Trying to connect"
	ws = new WebSocket "ws://#{window.location.host}/websocket/"
	ws.onopen = ()->
		ws.send "Hello,world"
		$("#wsstatus").css "color","green"
		console.log "WsOnline"

	ws.onclose =  ()->
		$("#wsstatus").css "color","red"
		setTimeout "connect()",1000

	ws.onerror = (error)->
		console.log error

	eventfunc={}

	ws.onmessage = (e)->
		mes= e.data
		mes = eval "(" + mes + ")"
		if mes.event of eventfunc
			eventfunc[mes.event] JSON.stringify(mes.data)

	addevent = (event,func)->
		eventfunc[event] = func

	this.addevent = addevent
	this.eventfunc = eventfunc

	addevent "debug",(mes)->
		console.log mes
		ws.send "Alright"

	addevent "gamedata",(mes)->
		$("#loc").html mes

	addevent "serverconn",(mes)->
		if mes.toString() == "\"true\""
			$("#status").html "Connected"
			$("#status").css "color","green"
		else
			$("#status").html "Not Connected"
			$("#status").css "color","red"


	addevent ""

this.connect = connect
connect()