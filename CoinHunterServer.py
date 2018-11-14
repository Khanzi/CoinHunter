
from socket import *
import threading
import time


maze = [['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'p', '#', '', '', '', '#', '', 'o', '#'],
        ['#', 'o', '#', 'o', '#', '', '#', '', '#', '#'],
        ['#', '', '#', '#', '#', '', '#', '', '', '#'],
        ['#', '', '', 'o', '', '', 'o', '', '', '#'],
        ['#', '', '#', '#', '#', '#', '', '', '', '#'],
        ['#', '', 'o', '', '', '#', '', '', '', '#'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']]

class serveThread (threading.Thread):
        def __init__(self, socket, addr):
         threading.Thread.__init__(self)
         self.socket = socket
         self.addr = addr
        def run(self):
         p = playerID(1,1)
         message = ""
         coins = 0
         while(message != "quit"):
                mazeStr = mazeS(maze)
                print("Sending the map!")
                self.socket.send(mazeStr.encode())
                message = self.socket.recv(1024).decode()
                print("Receiving input!")
                if(message == "CMD_W" and canIMove(p.xPos-1,p.yPos,maze)):
                    p.xPos -= 1
                    maze[p.xPos+1][p.yPos] = ''
                    coins = coins + int(coinCheck(p.xPos, p.yPos, maze))
                    wallCheck(p.xPos, p.yPos, maze)
                    print(p.xPos)
                elif(message == "CMD_A"and canIMove(p.xPos,p.yPos-1,maze)):
                    p.yPos -= 1
                    maze[p.xPos][p.yPos+1] = ''
                    coins = coins + int(coinCheck(p.xPos, p.yPos, maze))
                    wallCheck(p.xPos, p.yPos, maze)
                elif(message == "CMD_S"and canIMove(p.xPos+1,p.yPos,maze)):
                    p.xPos += 1
                    maze[p.xPos-1][p.yPos] = ''
                    coins = coins + int(coinCheck(p.xPos, p.yPos, maze))
                    wallCheck(p.xPos, p.yPos, maze)
                elif(message == "CMD_D"and canIMove(p.xPos,p.yPos+1,maze)):
                    p.yPos += 1
                    maze[p.xPos][p.yPos-1] = ''
                    coins = coins + int(coinCheck(p.xPos, p.yPos, maze))
                    wallCheck(p.xPos, p.yPos, maze)
                elif(message == "SCORE"):
                    print("Your score is ", coins)
                    score = "!!!YOUR SCORE IS " + str(coins) + "!!!" + "\n" + "\n"
                    self.socket.send(score.encode())
                else:
                    badmove = "!!!INVALID MOVE OR UNRECOGNIZED COMMAND!!! \n \n"
                    self.socket.send(badmove.encode())
                mazeStr = mazeS(maze)
                self.socket.send(mazeStr.encode())

                print("We received "+message);
                time.sleep(.1)
         self.socket.close()


serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
print ('The server is ready to receive!')
serverSocket.bind(('', serverPort))

myThreads = []




#Turning the maze into a string!
def mazeS(maze):
    return('\n'.join([''.join(['{:4}'.format(item) for item in row]) for row in maze]))

class playerID(object):
    xPos = 1
    yPos = 1

    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos
        self.coins = 0

def makePlayer(xPos, yPos):
    player = playerID(xPos,yPos)
    return player

def canIMove(xPos, yPos, maze):
    if(maze[xPos][yPos] == '#'):
        return(False)
    else:
        return(True)

def wallCheck(xPos, yPos, maze):
    if(maze[xPos][yPos] != '#'):
        maze[xPos][yPos] = 'p'
    else:
        xPos = 1
        yPos = 1

def coinCheck(xPos, yPos, maze):
    if(maze[xPos][yPos] == 'o'):
        return(1)
    else:
        return(0)



serverSocket.listen(10)
while True:
  connectionSocket, addr = serverSocket.accept()
  temp = serveThread(connectionSocket,addr)
  temp.start()

  print("\nSpawned Thread")
  myThreads.append(temp)
for t in myThreads: 
    t.join() 
