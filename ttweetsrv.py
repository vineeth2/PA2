from socket import *
import sys
import re

from _thread import *
import threading

stringTweet = ""
clients = {}
database = {}
timelineDatabase = {}
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
		if clientReception[0:4] == "unsu":
		    unsuFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "time":
			timelineFunction(connectionSocket, clientReception)
		if clientReception[0:4] == "exit":
			connectionOnline = False
	exitString = "bye bye"
	connectionSocket.send(exitString.encode())
	del(clients[connectionSocket])
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
	usernameKey, subbed_hashtags = clients[connectionSocket]
	if usernameKey not in database.keys():
		database[usernameKey] = [tweet], [hashtag_list]
	else:
		database[usernameKey][0].append(tweet)
		database[usernameKey][1].append(hashtag_list)

def getAllTweetsByUsername(username):
	global database
	global clients
	return database[username] #returns a tuple (tweet_list, hashtag_list)

def findSubscribedHashtags(connectionSocket, incoming_hashtags):
	global clients
	socket_dictionary = {}
	socket_list = list(clients.keys())
	user_list, hashtag_lists = zip(*clients.values())
	for i in range(len(socket_list)):
		hashtag_list = hashtag_lists[i]
		for hashtag in hashtag_list:
			if hashtag in incoming_hashtags or hashtag == "ALL":
				socket_dictionary[socket_list[i]] = user_list[i]
	return socket_dictionary

def broadcast(connectionSocket, socket_dictionary, tweet):
	global timelineDatabase
	for sock in socket_dictionary.keys():
		if sock == connectionSocket:
			continue
		if sock in timelineDatabase.keys():
			timelineDatabase[sock].append(tweet)
		else:
			timelineDatabase[sock] = [tweet]


def userFunction(connectionSocket, clientReception):
	newUsername = clientReception[4:]
	global clients
	if clients:
		usernameEqualFlag = 0
		for username, hashtag_list in clients.values():
			if newUsername == username:
				usernameEqualFlag = 1
		if usernameEqualFlag:
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
	t, h = tuple(full_message.split('#', 1))
	username, _ = clients[connectionSocket]
	formated_tweet = username + ': "' + t + '" ' + "#" + h
	addToDatabase(connectionSocket, tweet, hashtag_list)
	broadcast(connectionSocket, 
	findSubscribedHashtags(connectionSocket, hashtag_list), formated_tweet)
	#print(database)

def gettFunction(connectionSocket, clientReception): #gettweets
	username = clientReception[4:]
	hashtag = ""
	message = ""
	tweet_list, hashtag_lists = getAllTweetsByUsername(username)
	#print(tweet_list)
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
	for username, hastag_list in clients.values():
		usernameString += username + " "
	connectionSocket.send(usernameString.encode())

def subsFunction(connectionSocket, clientReception):
    global clients
    hashtag = clientReception[4:]

    returnMessage = ""
    if (len(clients[connectionSocket][1]) == 3 or hashtag in clients[connectionSocket][1]):
        returnMessage = "operation failed: sub <hashtag> failed, already exists or exceeds 3 limitation."
    else:
        clients[connectionSocket][1].append(hashtag)
        returnMessage = "operation success"

    #print(clients)

    connectionSocket.send(returnMessage.encode())

def unsuFunction(connectionSocket, clientReception):
    global clients
    hashtag = clientReception[4:]

    returnMessage = "no"
    if (hashtag == "ALL"):
        clients[connectionSocket][1].clear()    # if hashtag is #ALL, unsub from all hashtags in list
        returnMessage = "operation success"
    elif (hashtag in clients[connectionSocket][1]):
        clients[connectionSocket][1].remove(hashtag)    # only remove hashtag if it exists.
        returnMessage = "operation success"

    connectionSocket.send(returnMessage.encode())

def timelineFunction(connectionSocket, clientReception):
	global timelineDatabase
	message = ""
	if connectionSocket not in timelineDatabase.keys():
		message = "User has not had anything on their timeline."
	else:
		for tweet in timelineDatabase[connectionSocket]:
			if tweet == timelineDatabase[connectionSocket][-1]:
				message += tweet
			else:
				message += tweet + "\n"
	connectionSocket.send(message.encode())


if __name__ == '__main__':
    main()