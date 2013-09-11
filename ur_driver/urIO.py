#!/usr/bin/env python
#import roslib; roslib.load_manifest('ur5_io')
import roslib
import rospy
import SocketServer

class EchoRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        print self.client_address, 'connected!'

    def handle(self):
	inData = 0
	endData = 0
	dataString = ""
	while True:

		# Empfangen
        	data = self.request.recv(1024)

		# Warten bis Datenstring S....E vollstaendig ist
		if inData == 1:
			i = data.find("E")
			if i != -1:
				dataString = dataString + data[:i]
				endData = 1
				inData = 0
			else:
				dataString = dataString + data
		
		# Daten verarbeiten
		if endData:
			dataString = dataString[0:len(dataString)-1]
			getURIO = dataString.split(',')
			#print getURIO
	
			# Daten in ROS-Param pushen
			rospy.set_param('urIO/DI0', getURIO[0])
			rospy.set_param('urIO/DI1', getURIO[1])
			rospy.set_param('urIO/DI2', getURIO[2])
			rospy.set_param('urIO/DI3', getURIO[3])
			rospy.set_param('urIO/DI4', getURIO[4])
			rospy.set_param('urIO/DI5', getURIO[5])
			rospy.set_param('urIO/DI6', getURIO[6])
			rospy.set_param('urIO/DI7', getURIO[7])
			rospy.set_param('urIO/AI0', getURIO[8])
			rospy.set_param('urIO/AI1', getURIO[9])
			

			# Srings und Zaehler zuruecksetzen
			dataString = ""
			inData = 0
			endData = 0

			#print rospy.get_param('urIO/DO1')

			# SENDEN
			self.request.send('( '+str(rospy.get_param('urIO/DO0'))+' , '+str(rospy.get_param('urIO/DO1'))+' , '+str(rospy.get_param('urIO/DO2'))+' , '+str(rospy.get_param('urIO/DO3'))+' , '+str(rospy.get_param('urIO/DO4'))+' , '+str(rospy.get_param('urIO/DO5'))+' , '+str(rospy.get_param('urIO/DO6'))+' , '+str(rospy.get_param('urIO/DO7'))+' , '+str(rospy.get_param('urIO/AO0'))+' , '+str(rospy.get_param('urIO/AO1'))+' , '+str(rospy.get_param('urIO/AO0_domain'))+' , '+str(rospy.get_param('urIO/AO1_domain'))+' , '+str(rospy.get_param('urIO/AI0_range'))+' , '+str(rospy.get_param('urIO/AI1_range'))+' )')
	

		# Warten bis Datenstring S....E vollstaendig ist
		if inData == 0:
			i = data.find("S")
			if i != -1:			
				dataString = data[i+1:]
				inData = 1

		
	print "UR-IO: Verbindung beendet!"	
	self.close()


class urIOserver(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)

def main():
	rospy.init_node('urIO')

	# Init-Ausgangswerte setzen	
	rospy.set_param('urIO/DO0', 0)
	rospy.set_param('urIO/DO1', 0)
	rospy.set_param('urIO/DO2', 0)
	rospy.set_param('urIO/DO3', 0)
	rospy.set_param('urIO/DO4', 0)
	rospy.set_param('urIO/DO5', 0)
	rospy.set_param('urIO/DO6', 0)
	rospy.set_param('urIO/DO7', 0)
	rospy.set_param('urIO/AO0', 0)
	rospy.set_param('urIO/AO1', 0)
	rospy.set_param('urIO/AO0_domain', 1)
	rospy.set_param('urIO/AO1_domain', 1)
	rospy.set_param('urIO/AI0_range', 2)
	rospy.set_param('urIO/AI1_range', 2)
	server = urIOserver(('', 50005), EchoRequestHandler)
	

	print "UR-IO: Bereit..."

	try:
		server.serve_forever()

	except KeyboardInterrupt:
		server.shutdown()
		print "UR-IO: Beendet!"

if __name__ == '__main__': main()
