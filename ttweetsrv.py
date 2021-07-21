from socket import *
import sys
import re

from _thread import *
import threading

stringTweet = ""
usernameDictionary = dict()

def client_handler(connectionSocket, address):
	connectionOnline = True
	while connectionOnline:
		clientReception = connectionSocket.recv(1024).decode()
		if clientReception[0:4] == "user":
			userFunction(connectionSocket, clientReception, address)
		if clientReception[0:4] == "getu":
			getuFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "exit":
			connectionOnline = False
	exitString = "bye bye"
	connectionSocket.send(exitString.encode())
	global usernameDictionary
	del(usernameDictionary[address])
	connectionSocket.close()

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
		connectionSocket, address = serverSocket.accept()
		thread = threading.Thread(target=client_handler, args=(connectionSocket, address))
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
	
def userFunction(connectionSocket, clientReception, address):
	newUsername = clientReception[4:]
	global usernameDictionary
	usernameList = []
	for username, hashtags, tweets in usernameDictionary.values():
		usernameList.append(username)
	if newUsername in usernameList:
		loginFailed = "username illegal, connection refused."
		failFlag = "F"
		loginFailed = failFlag + loginFailed
		connectionSocket.send(loginFailed.encode())
	else:
		loginSuccess = "username legal, connection established."
		successFlag = "S"
		loginSuccess = successFlag + loginSuccess
		usernameDictionary[address] = (newUsername, [], []) #Item[0] = username, Item[1] = subscribed Hashtags, Item[2] = tweets sent by user
		connectionSocket.send(loginSuccess.encode())

def getuFunction(connectionSocket, clientReception):
	usernameString = ""
	global usernameDictionary
	usernameList = []
	for username, hashtags, tweets in usernameDictionary.values():
		usernameList.append(username)
	for username in usernameList:
		usernameString += username + " "
	connectionSocket.send(usernameString.encode())


if __name__ == '__main__':
    main()