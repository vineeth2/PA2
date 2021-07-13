from socket import *
import sys
import re

def main():
    if len(sys.argv) < 4:
        print("Error, invalid number of parameters")
        exit()

    serverIP = str(sys.argv[2])
    serverName = str(sys.argv[2])

    if not re.match(r"^[0-9]*$", sys.argv[3]):
        print("Error, invalid Server Port")
        exit()
    serverPort = int(sys.argv[3]) #13500
    if serverPort < 13000 or serverPort > 14000:
        print("Error, invalid Server Port")
        exit()

    if sys.argv[1] == "-u" and len(sys.argv) != 5:
        print("Error, invalid number of parameters for upload mode")
        exit()   

    if (sys.argv[1] == "-d" and len(sys.argv) != 4):
        print("Error, invalid number of parameters for download mode")
        exit() 
    
    message = sys.argv[1]
    if (sys.argv[1] == "-u" and len(sys.argv[4]) > 150):
        print("Error: Message Cannot be greater than 150 characters")
        exit()

    if (sys.argv[1] == "-u" and len(sys.argv[4]) <= 150):
        message = message + sys.argv[4]
        uploadSys(serverName, serverPort, message)

    else:
        downloadSys(serverName, serverPort, message)


    

def uploadSys(serverName, serverPort, message):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        
        clientSocket.settimeout(5)
        clientSocket.connect((serverName, serverPort))
        sentence = message
        
        clientSocket.send(sentence.encode())
        newSentence = clientSocket.recv(1024)
        print("{0}".format(newSentence.decode()))
        clientSocket.close()
    except:
        print("Error Message: Server Not Found")
        exit()

def downloadSys(serverName, serverPort, message):
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.settimeout(5)
        clientSocket.connect((serverName, serverPort))
        sentence = message
        clientSocket.send(sentence.encode())
        newSentence = clientSocket.recv(1024)
        print('Output: "{0}"'.format(newSentence.decode()))
        clientSocket.close()
    except:
        print("Error Message: Server Not Found")
        exit()

if __name__ == "__main__":
    main()