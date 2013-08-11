#Copyright 2010 Gagan Deep Singh(Quest World)
#Licensed under the Apache License, Version 2.0 (the "License"); 
#you may not use this file except in compliance with the License. 
#You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0 
#Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License. 



#To use this app, just press up arrow key to start your first call making(give the phone number and the number of times)
#To force reset in case it starts giving errors, press down arrow key
#Use the RED colored END key to terminate it in between the miss call process is going on
#Thats it, what else do you expect from a miss call software???(do write to us, may be we'll implement)

import telephone,appuifw,key_codes,e32,globalui,keycapture

def newphonestate (stateInformation):
	global msg
	newState = stateInformation[0]
	if newState == telephone.EStatusUnknown: s_unknown()
	elif newState == telephone.EStatusIdle: s_idle()
	elif newState == telephone.EStatusDialling:s_dialing()
	elif newState == telephone.EStatusRinging: s_ringing(stateInformation[1])
	elif newState == telephone.EStatusAnswering: s_answering()
	elif newState == telephone.EStatusConnecting: s_connecting()
	elif newState == telephone.EStatusConnected: s_connected()
	elif newState == telephone.EStatusReconnectPending: s_reconnectPending()
	elif newState == telephone.EStatusDisconnecting: s_disconnecting()
	elif newState == telephone.EStatusHold: s_hold()
	elif newState == telephone.EStatusTransferring: s_transferring()
	elif newState == telephone.EStatusTransferAlerting: s_transferAlerting()
	print "The phone has changed states."
	print "   ",msg


# Begin defining call states	
def s_unknown():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg = "The new state is unknown"

def s_idle():
	global msg,state
	state="idle"
	call()
	msg = "The phone is idle"

def s_dialing():
	global msg,state
	state="unknown"
	msg = "The Phone is dialing"

def s_ringing(in_num):
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg = "The new phone is ringing, call is from %s " % in_num

def s_answering():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg = "A call is being answered"

def s_connecting():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg = "A call is connecting"

def s_connected():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg="A call has been connected"

def s_reconnectPending():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg="The channel has been lost and a reconnect is being attempted"

def s_disconnecting():
	global msg,state
	state="dc"
	telephone.hang_up()
	msg="A call is being disconnected"

def s_hold():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg="A call is being placed on hold"

def s_transferring():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg = "A call is being transferred"

def s_transferringAlerting():
	global msg,state
	state="unknown"
	telephone.hang_up()
	msg = "The phone is alerting the remote phone about a transferred call"
# end of definition of call states



def call():
	global n,num,i,m,state
	if n>0:
		n=n-1
		globalui.global_note(u"Missed Calls Done:"+str(m-n))
		telephone.dial(num)
	else:
		ch=globalui.global_query(u"Want to Give more missed calls to:\n"+str(num)+u" ?")
		if ch:
			n=m+1
			call()

def query():
	global num,n,m,end,state
	if state!="idle":
		telephone.hang_up()
	num=appuifw.query(u"Enter Number","text",u"+91")
	n=appuifw.query(u"How Many Times?","number")
	if num:
		if n:
			n=n-1
			m=n
			telephone.dial(num)

def quit():
	global state
	app_lock.signal()
	if state!="idle":
		telephone.hang_up()
	capturer.stop()

def stop(anti_freeze=None):
	global n,state
	if anti_freeze!=None:
		telephone.hang_up()
	n=0

def key_capture(key):
	global end
	globalui.global_note(u"Miss calls termination detected")
	end=1
	stop(1)

end=0
state="idle"
capturer = keycapture.KeyCapturer(key_capture)
capturer.keys = (key_codes.EKeyNo,)
capturer.start()

i=appuifw.InfoPopup()

telephone.call_state(newphonestate)
canvas=appuifw.Canvas()
appuifw.app.body=canvas
canvas.bind(key_codes.EKeyUpArrow,query)
canvas.bind(key_codes.EKeyDownArrow,stop)
appuifw.app.title=u"Miss Call Dabster by Gagan"

appuifw.app.exit_key_handler=quit
app_lock=e32.Ao_lock()

#telephone.dial(num)

app_lock.wait()