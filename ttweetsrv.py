from socket import *
import sys
import re

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
	clientReception = connectionSocket.recv(1024).decode()
	if clientReception[0:4] == "user":
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
	if clientReception[0:4] == "getu":
		usernameString = ""
		for username in usernameTuple:
			usernameString += username + " "
		connectionSocket.send(usernameString.encode())
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
	
