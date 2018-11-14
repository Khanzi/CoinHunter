from socket import *
serverName = '192.168.56.1'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
sentence = ""
while sentence!="quit":
    maze = clientSocket.recv(1024)
    print(maze.decode())
    sentence =  input('Input CMD_(W,A,S,D) for Up, Left, Down, Right. To see score type SCORE:')
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    #print ('YOU MOVED!\n', modifiedSentence.decode(), "\n\n\n\n")
clientSocket.close()

