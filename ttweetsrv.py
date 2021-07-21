from socket import *
import sys
import re

from _thread import *
import threading

thread_lock = threading.Lock()

def Main():
	if len(sys.argv) != 2:
		print("Error: Invalid Input. Wrong number of parameters")
		exit()

	serverPort = int(sys.argv[1])
	if serverPort < 13000 or serverPort > 14000:
		print("Error: Invalid Input. Wrong number of parameters")
		exit()

	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(("", serverPort))
	serverSocket.listen(1)
	print('The server is ready to receive at port: "{0}"'.format(serverPort))
	stringTweet = ""
	usernameTuple = ()
	while True:
		connectionSocket, addr = serverSocket.accept()
		thread_lock.acquire()
		clientReception = connectionSocket.recv(1024).decode()
		if clientReception[0:4] == "user":
			start_new_thread(userFunction, (connectionSocket, clientReception, usernameTuple))
		if clientReception[0:4] == "getu":
			start_new_thread(getuFunction, (connectionSocket, clientReception, usernameTuple))
		if clientReception[0:4] == "exit":
			start_new_thread(exitFunction, (connectionSocket, clientReception))
	
		#if clientReception[0:2] == "-u":
		#	success = "Tweet was successfully uploaded"
		#	connectionSocket.send(success.encode())
		#	stringTweet = clientReception[2:]

		#if clientReception[0:2] == "-d":
		#	if stringTweet == "":
		#		emptyStr = ""
		#		connectionSocket.send(emptyStr.encode())
		#	else:
		#		connectionSocket.send(stringTweet.encode())
		#connectionSocket.close()
	
def userFunction(connectionSocket, clientReception, usernameTuple):
	newUsername = clientReception[4:]
	if newUsername in usernameTuple:
		loginFailed = "username illegal, connection refused."
		failFlag = "F"
		loginFailed = failFlag + loginFailed
		connectionSocket.send(loginFailed.encode())
	else:
		loginSuccess = "username legal, connection established."
		successFlag = "S"
		loginSuccess = successFlag + loginSuccess
		connectionSocket.send(loginSuccess.encode())
		usernameTuple += (newUsername,)

def getuFunction(connectionSocket, clientReception, usernameTuple):
	usernameString = ""
	for username in usernameTuple:
		usernameString += username + " "
	connectionSocket.send(usernameString.encode())

def exitFunction(connectionSocket, clientReception):
	exitString = "bye bye"
	connectionSocket.send(exitString.encode())
	thread_lock.release()
	connectionSocket.close()

if __name__ == '__main__':
    Main()