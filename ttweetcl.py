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
        uploadSys(clientSocket, userInputList)
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

#def uploadSys(userInputList):
#    if len(userInputList) == 3:
#        sentence = message
#        clientSocket.send(sentence.encode())

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

if __name__ == "__main__":
    main()