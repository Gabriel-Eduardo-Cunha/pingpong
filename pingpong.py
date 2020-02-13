from graphics import GraphWin, Rectangle, Point, color_rgb, Text
import random
import time

class PingPong(GraphWin):
    def __init__(self, gameMode = 'normal', numOfPlayers = 1 , popName = False, render = True,frameRate = 30):
        if render == False:
            self.render = False
        else:
            self.render = True
            GraphWin.__init__(self, 'PingPongGame', 800, 600)
            self.setBackground(color_rgb(0,0,0))
        self.gameMode = gameMode
        self.framesPassed = 0
        self.popName = popName
        self.racket = [Racket(self, x) for x in range(numOfPlayers)]
        self.racketsAlive = numOfPlayers
        self.frameRate = frameRate
        self.gameSpeed = 1
        self.gameEnd = False
        if self.render:
            self.createHud()
        self.start()

    def start(self):
        while self.gameEnd == False:
            self.frame()
    
    def frame(self):
        self.moveBall()
        self.racketMove()
        self.checkBallColision()
        self.updateSpeed()
        self.framesPassed += 1
        if self.render:
            time.sleep(1/self.frameRate)
    
    def createHud(self):
        score = self.getScores()
        self.scoreText = Text(Point(730, 20 + len(self.racket) * 10), score)
        self.scoreText.setTextColor(color_rgb(255,255,255))
        self.scoreText.draw(self)
        
        self.gameSpeedText = Text(Point(50, 20), 'Speed: ' + str(self.gameSpeed))
        self.gameSpeedText.setTextColor(color_rgb(255,255,255))
        self.gameSpeedText.draw(self)
        
    def updateSpeed(self):
        if self.framesPassed >= 60:
            self.framesPassed = 0
            self.gameSpeed += 0.1
            self.gameSpeed = round(self.gameSpeed, 1)
            self.lastSpeedUpdate = time.time()
        if self.render:
            self.gameSpeedText.setText('Speed: ' + str(self.gameSpeed))
    
    def getScores(self):
        score = 'Scores:\n'
        for i in range(len(self.racket)):
            score += 'P' + str(i + 1) + ': ' + str(self.racket[i].score) + '\n'
        return score

    
    def moveBall(self):
        for racket in self.racket:
            racket.ball.move(racket.ball.speedX * self.gameSpeed, racket.ball.speedY  * self.gameSpeed)
    
    def racketMove(self):
        for racket in self.racket:
            if self.gameMode == 'normal':
                key = self.checkKey()
            if self.gameMode == 'aitrain':
                key = racket.brain.guess([int(racket.ball.getCenter().getX()), int(racket.getCenter().getX())])
            if key == 'Left' and racket.getP1().getX() > 0:
                racket.move(-20, 0)
            if key == 'Right' and racket.getP2().getX() < 800:
                racket.move(20, 0)

    
    def checkBallColision(self):
        for racket in self.racket:
            if racket.alive == True:
                if racket.ball.getP1().getX() < racket.getP2().getX() and racket.ball.getP2().getX() > racket.getP1().getX():
                    if racket.ball.getP2().getY() >= racket.getP1().getY() and racket.ball.getP1().getY() < racket.getP2().getY():
                        racket.ball.speedX = random.randint(-10, 10)
                        racket.ball.speedY = random.randint(-10, -5)
                        racket.score += round(10 * self.gameSpeed, 0)
                        if self.render:
                            self.scoreText.setText(self.getScores())
                
                # Left Wall Colision
                if racket.ball.getP1().getX() <= 0:
                    racket.ball.speedX = abs(racket.ball.speedX)
                # Right Wall Colision
                if racket.ball.getP2().getX() >= 800:
                    racket.ball.speedX = -abs(racket.ball.speedX)
                # Top Celing Colision
                if racket.ball.getP1().getY() <= 0:
                    racket.ball.speedY = abs(racket.ball.speedY)
                # Bottom Floor Colision
                if racket.ball.getP1().getY() > 600:
                    racket.ball.undraw()
                    racket.alive = False
                    racket.undraw()
                    self.racketsAlive -= 1
                    if self.racketsAlive == 0:
                        self.gameOver()
    
    def gameOver(self):
        if self.render:
            self.close()
        highestScore = 0
        self.betterId = 0
        for id in range(len(self.racket)):
            if self.racket[id].score > highestScore:
                self.betterId = id
                highestScore = self.racket[id].score
        print('Highest Score: ' + str(highestScore))
        self.gameEnd = True
        
class Racket(Rectangle):
    def __init__(self, graphWin, id):
        Rectangle.__init__(self, Point(350, 570), Point( 450, 590))
        self.id = id
        self.color = color_rgb(random.randint(10,255),random.randint(10,255),random.randint(10,255))
        self.score = 0
        if graphWin.render:
            self.setFill(self.color)
            self.draw(graphWin)
        self.ball = Ball(self, graphWin)
        self.alive = True

        

class Ball(Rectangle):
    def __init__(self, racket, graphWin):
        Rectangle.__init__(self, Point(385, 285), Point(415, 315))
        if graphWin.render:
            self.setFill(racket.color)
            self.draw(graphWin)
        self.speedX = 0
        self.speedY = 5
        
