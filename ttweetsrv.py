from socket import *
import sys
import re

from _thread import *
import threading

stringTweet = ""
usernameTuple = ()

def client_handler(connectionSocket):
	connectionOnline = True
	while connectionOnline:
		clientReception = connectionSocket.recv(1024).decode()
		if clientReception[0:4] == "user":
			userFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "getu":
			getuFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "exit":
			connectionOnline = False
	exitString = "bye bye"
	connectionSocket.send(exitString.encode())
	connectionSocket.close() #TODO: remove user information from server

def main():
	if len(sys.argv) != 2:
		print("Error: Invalid Input. Wrong number of parameters")
		exit()

	serverPort = int(sys.argv[1])
	if serverPort < 13000 or serverPort > 14000:
		print("Error: Invalid Input. Wrong number of parameters")
		exit()

	serverSocket = socket(AF_INET, SOCK_STREAM)
	serverSocket.bind(("", serverPort))
	serverSocket.listen()
	print('The server is ready to receive at port: "{0}"'.format(serverPort))
	while True:
		connectionSocket, addr = serverSocket.accept()
		thread = threading.Thread(target=client_handler, args=(connectionSocket,))
		thread.start()
	
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
	
def userFunction(connectionSocket, clientReception):
	newUsername = clientReception[4:]
	global usernameTuple
	if newUsername in usernameTuple:
		loginFailed = "username illegal, connection refused."
		failFlag = "F"
		loginFailed = failFlag + loginFailed
		connectionSocket.send(loginFailed.encode())
	else:
		loginSuccess = "username legal, connection established."
		successFlag = "S"
		loginSuccess = successFlag + loginSuccess
		usernameTuple += (newUsername,)
		connectionSocket.send(loginSuccess.encode())

def getuFunction(connectionSocket, clientReception):
	usernameString = ""
	global usernameTuple
	for username in usernameTuple:
		usernameString += username + " "
	connectionSocket.send(usernameString.encode())


if __name__ == '__main__':
    main()