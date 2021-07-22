from socket import *
import sys
import re

from _thread import *
import threading

stringTweet = ""
clients = {}
database = {}
def client_handler(connectionSocket):
	connectionOnline = True
	while connectionOnline:
		clientReception = connectionSocket.recv(1024).decode()
		if clientReception[0:4] == "user":
			userFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "twee":
			tweeFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "gett":
			gettFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "getu":
			getuFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "subs":
		    subsFunction(connectionSocket, clientReception)
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
	serverSocket.listen(5)
	print('The server is ready to receive at port: "{0}"'.format(serverPort))
	while True:
		connectionSocket, address = serverSocket.accept()
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
def addToDatabase(connectionSocket, tweet, hashtag_list):
	global database
	global clients
	if clients[connectionSocket] not in database:
		database[clients[connectionSocket]] = [tweet], [hashtag_list]
	else:
		database[clients[connectionSocket]][0].append(tweet)
		database[clients[connectionSocket]][1].append(hashtag_list)
def getAllTweetsByUsername(username):
	global database
	global clients
	return database[username] #returns a tuple (tweet_list, hashtag_list)

def userFunction(connectionSocket, clientReception):
	newUsername = clientReception[4:]
	global clients
	if clients and newUsername in clients.values():
		loginFailed = "username illegal, connection refused."
		failFlag = "F"
		loginFailed = failFlag + loginFailed
		connectionSocket.send(loginFailed.encode())
	else:
		loginSuccess = "username legal, connection established."
		successFlag = "S"
		loginSuccess = successFlag + loginSuccess
		subbed_hashtags = []
		clients[connectionSocket] = newUsername, subbed_hashtags
		connectionSocket.send(loginSuccess.encode())
def tweeFunction(connectionSocket, clientReception):
	global database
	full_message = clientReception[4:]
	full_message_list = full_message.split("#")
	tweet = full_message_list[0]
	hashtag_list = full_message_list[1:]
	#for hashtag in hashtag_list: 
	#	hashtag = "#" + hashtag
	addToDatabase(connectionSocket, tweet, hashtag_list)
	print(database)

def gettFunction(connectionSocket, clientReception): #gettweets
	username = clientReception[4:]
	hashtag = ""
	message = ""
	tweet_list, hashtag_lists = getAllTweetsByUsername(username)
	print(tweet_list)
	for i in range(len(tweet_list)):
		hashtag_list = hashtag_lists[i]
		for j in range(len(hashtag_list)):
			hashtag += "#" + hashtag_list[j]
		message += username + ": \"" + tweet_list[i] + '\" ' + hashtag + '\n'
		hashtag = ""
	connectionSocket.send(message.encode())
	
def getuFunction(connectionSocket, clientReception):
	usernameString = ""
	global clients
	for username in clients.values():
		usernameString += username + " "
	connectionSocket.send(usernameString.encode())

def subsFunction(connectionSocket, clientReception):
    global clients
    hashtag = clientReception[4:]

    if (len(clients[connectionSocket][1]) == 3 or hashtag in clients[connectionSocket][1]):
        subFailed = "operation failed: sub <hashtag> failed, already exists or exceeds 3 limitation."
        subFailed = "F" + subFailed
        connectionSocket.send(subFailed.encode())
    else:
        clients[connectionSocket][1].append(hashtag)
        subSuccess = "successfully subscribed to {0}".format(hashtag)
        subSuccess = "S" + subSuccess
        connectionSocket.send(subSuccess.encode())



if __name__ == '__main__':
    main()