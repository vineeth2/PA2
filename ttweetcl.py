from socket import *
import sys
import re

def main():
    if len(sys.argv) != 4:
        print("error: args should contain <ServerIP> <ServerPort> <Username>")
        exit()

    serverIP = str(sys.argv[1])
    serverName = str(sys.argv[1])

    if not re.match(r"^[0-9]*$", sys.argv[2]):
        print("error: server port invalid, connection refused.")
        exit()
    serverPort = int(sys.argv[2]) #13500
    if serverPort < 13000 or serverPort > 14000:
        print("error: server port invalid, connection refused.")
        exit()

    username = "user" + sys.argv[3]
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        
        clientSocket.settimeout(5)
        clientSocket.connect((serverName, serverPort))
    except:
        print("error: server ip invalid, connection refused.")
        exit()  
    login(clientSocket, username)
    
    #message = sys.argv[1]
    #if (sys.argv[1] == "-u" and len(sys.argv[4]) > 150):
    #    print("message length illegal, connection refused.")
    #    exit()
    #
    #if (sys.argv[1] == "-u" and len(sys.argv[4]) <= 150):
    #    message = message + sys.argv[4]
    #    uploadSys(serverName, serverPort, message)
    #
    #else:
    #    downloadSys(serverName, serverPort, message)


def login(clientSocket, username):  
    clientSocket.send(username.encode())
    usernameResponse = clientSocket.recv(1024).decode()
    printUsernameResponse = usernameResponse[1:]
    print("{0}".format(printUsernameResponse))
    if (usernameResponse[0] == "F"):
        exit()
    userInput(clientSocket)

def userInput(clientSocket):
    userInputString = input()
    userInputList = userInputString.split()
    if userInputList[0] == "tweet":
        uploadSys(clientSocket, userInputString) #Input string here for later split
    elif userInputList[0] == "subscribe":
        subscribeSys(clientSocket, userInputList)
    elif userInputList[0] == "unsubscribe":
        unsubscribeSys(clientSocket, userInputList)
    elif userInputList[0] == "timeline":
        timelineSys(clientSocket, userInputList)
    elif userInputList[0] == "getusers":
        usersSys(clientSocket, userInputList)
    elif userInputList[0] == "gettweets":
        tweetsSys(clientSocket, userInputList)
    elif userInputList[0] == "exit":
        exitSys(clientSocket, userInputList)
    else:
        print("client command not found.")
        userInput(clientSocket)

def uploadSys(clientSocket, userInputList):
    userInputList = userInputList.split('"')
    if len(userInputList) != 3:
        print("length not correct")
        userInput(clientSocket)
    tweet = userInputList[1]
    hashtag = userInputList[2].strip() #Removes whitespace due to split
    if len(tweet) > 150 or len(tweet) < 1 or tweet == None: #TODO fix empty edge case
        if len(tweet) > 150:
            print("message length illegal, connection refused.")
        if len(tweet) < 1 or tweet == None:
            print("message format illegal.")
        userInput(clientSocket)
    if hashtag[0] != '#':
        print("hashtag illegal format, connection refused.")
        userInput(clientSocket)
    hashtag_list = hashtag.split('#')
    if len(hashtag_list) > 6:
        print("operation failed: sub <hashtag> failed, already exists or exceeds 3 limitation")
        userInput(clientSocket)
    for htag in hashtag_list[1:]:
        if len(htag) > 14:
            print("hashtag illegal format, connection refused.")
            userInput(clientSocket)
        if not re.match('^[a-zA-Z0-9_]+$', htag):
            print("hashtag illegal format, connection refused.")
            userInput(clientSocket)
    message = "twee" + tweet + hashtag
    clientSocket.send(message.encode())
    userInput(clientSocket)

#def downloadSys(serverName, serverPort, message):
#    try:
#        clientSocket = socket(AF_INET, SOCK_STREAM)
#        clientSocket.settimeout(5)
#        clientSocket.connect((serverName, serverPort))
#        sentence = message
#        clientSocket.send(sentence.encode())
#        newSentence = clientSocket.recv(1024)
#        print('Output: "{0}"'.format(newSentence.decode()))
#        clientSocket.close()
#    except:
#        print("error: server ip invalid, connection refused.")
#        exit()

def usersSys(clientSocket, userInputList):
    getUsersSentence = "getu"
    clientSocket.send(getUsersSentence.encode())
    usernames = clientSocket.recv(1024).decode()
    usernameList = usernames.split()
    for username in usernameList:
        print(username)
    userInput(clientSocket)
    
def tweetsSys(clientSocket, userInputList):
    if (len(userInputList) != 2):
        print("length illegal, connection refused.")
        userInput(clientSocket)
    username = userInputList[1]
    message = "gett" + username
    clientSocket.send(message.encode())
    serverResponse = clientSocket.recv(2048).decode()
    print(serverResponse)
    userInput(clientSocket)

def subscribeSys(clientSocket, userInputList):
    if (len(userInputList) != 2):
        print("length illegal, connection refused.")
        userInput(clientSocket)

    hashtag = userInputList[1]
    if (hashtag == null or hashtag.length < 2):
        print("hashtag illegal format, connection refused.")    # checks if hashtag CANNOT be properly formatted.
        userInput(clientSocket)
    if (hashtag[0] != "#"):
        print("hashtag illegal format, connection refused.")    # checks if hashtag not preceded by "#"
        userInput(clientSocket)
    if len(hashtag[1:]) > 14:
        print("hashtag illegal format, connection refused.")    # checks if hashtag length is too long
        userInput(clientSocket)
    if not re.match('^[a-zA-Z0-9_]+$', hashtag[1:]):
        print("hashtag illegal format, connection refused.")    # checks if hashtag consists of letters and numbers
        userInput(clientSocket)
    message = "subs" + hashtag[1:]
    clientSocket.send(message.encode())
    userInput(clientSocket)

def exitSys(clientSocket, userInputList):
    exitSentence = "exit"
    clientSocket.send(exitSentence.encode())
    serverResponse = clientSocket.recv(1024).decode()
    print(serverResponse)

if __name__ == "__main__":
    main()