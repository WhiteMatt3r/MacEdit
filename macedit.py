#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os, fcntl, socket, struct, signal, platform, netifaces
from sys import exit, argv, executable
from time import sleep
from random import randint

def clear():
	print(chr(27) + "[2J")

def header():
	print """
.88b  d88.  .d8b.   .o88b. d88888b d8888b. d888888b d888888b 
88'YbdP`88 d8' `8b d8P  Y8 88'     88  `8D   `88'   `~~88~~' 
88  88  88 88ooo88 8P      88ooooo 88   88    88       88    
88  88  88 88~~~88 8b      88~~~~~ 88   88    88       88    
88  88  88 88   88 Y8b  d8 88.     88  .8D   .88.      88    
YP  YP  YP YP   YP  `Y88P' Y88888P Y8888D' Y888888P    YP  
                                          By: WhiteMatt3r
	"""

def setMAC(mac, interface):
	os.system("ip link set dev " + interface + " down && ip link set dev " + interface + " address " + mac + " && ip link set dev " + interface + " up")
	return "MAC address set to " + mac + " on " + interface

def craftSH(interface):
	return "Not yet implemented"

def Randomize(interface):
	mac = [randint(0x00, 0x7f), randint(0x00, 0x7f), randint(0x00, 0x7f), randint(0x00, 0x7f), randint(0x00, 0xff), randint(0x00, 0xff)] 
	new_mac = ':'.join(map(lambda x: "%02x" % x, mac))
	return setMAC(new_mac, interface)

def ValidMAC(interface):
	sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	mac_p1 = ':'.join(['%02x' % ord(char) for char in fcntl.ioctl(sck.fileno(), 0x8927,  struct.pack('256s', interface[:15]))[18:21]]) + ":"
	mac_p2 = [randint(0x00, 0x7f), randint(0x00, 0xff), randint(0x00, 0xff)] 
	new_mac = mac_p1 + ':'.join(map(lambda x: "%02x" % x, mac_p2))
	return setMAC(new_mac, interface)

def CustomMAC(interface):
	new_mac = raw_input("MAC Address: ")
	while len(new_mac) <= 0 or len(new_mac) > 17 or len(new_mac) < 17:
		new_mac = raw_input("MAC Address: ")
	return setMAC(new_mac, interface)

def Boot(interface):
	return craftSH(interface)

options = {
	'1': Randomize,
	'2': ValidMAC,
	'3': CustomMAC,
	'4': Boot
}

def sighandle(signal,frame):
	if signal == 2:
		exit("Shutting down...\n")

if __name__ == "__main__":

	if os.geteuid() != 0:
		print "This script must be run as root. Sudoing..."
		args = ['sudo', executable] + argv + [os.environ]
		os.execlpe('sudo', *args)

	signal.signal(signal.SIGINT, sighandle)
	clear()
	header()

	print "Enumerating interfaces...\n"

	iface_list = netifaces.interfaces()

	sleep(1)

	if len(iface_list) > 0:
		x = 0
		for i in iface_list:
			print str(x) + ") " + i
			x+=1
		print ""
	else:
		exit("No interfaces found!")

	iface_sel = raw_input("Please enter a choice: ")
	while len(iface_sel) <= 0:
		iface_sel = raw_input("Please enter a choice: ")

	try:
		iface = iface_list[int(iface_sel)]
	except IndexError:
		exit("Please try again and enter a choice within range!")

	clear()

	header()

	print """
1) Randomize MAC address
2) Create valid MAC address
3) Enter a custom MAC address
4) Change this MAC address on boot
	"""

	option_sel = raw_input("Please enter a choice: ")
	while len(option_sel) <= 0:
		option_sel = raw_input("Please enter a choice: ")

	try:
		option = options[option_sel]
	except KeyError:
		exit("Please try again and enter a choice within range!")

	print option(iface)