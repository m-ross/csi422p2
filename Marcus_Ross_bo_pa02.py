from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

windowWidth = 500.0
windowHeight = 500.0

# triangle vertices
xA = 80.0
yA = 80.0
xB = 350.0
yB = 90.0
xC = 380.0
yC = 380.0

global alpha
global beta
global gamma

# initialised to unusable values to ensure white is the first color rendered
alpha = -1
beta = -1
gamma = -1

def initGL():
	glClearColor(0.0, 0.0, 0.0, 1.0)
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0.0, windowWidth, 0.0, windowHeight)

def lineFunc(x0, y0, x1, y1, x, y): # gives the output at (x, y) of an implicit function of a line from point (x0, y0) to (x1, y1)
	number = (y0 - y1) * x + (x1 - x0) * y + x0 * y1 - x1 * y0
	return number

def calcAlpha():
	global alpha
	global beta
	global gamma
	beta = lineFunc(xA, yA, xC, yC, xMouse, yMouse) / lineFunc(xA, yA, xC, yC, xB, yB) # beta = f_ac(x, y) / f_ac(xB, yB)
	gamma = lineFunc(xA, yA, xB, yB, xMouse, yMouse) / lineFunc(xA, yA, xB, yB, xC, yC) # gamma = f_ab(x, y) / f_ab(xC, yC)
	alpha = 1 - beta - gamma

def pickColor():
	if (alpha < 0 or alpha > 1 or beta < 0 or beta > 1 or gamma < 0 or gamma > 1):
		glColor3f(1.0, 1.0, 1.0) # use white if any of alpha, beta, or gamma are negative or >1
	else:
		glColor3f(alpha, beta, gamma) # otherwise, color = (alpha * red, beta * green, gamma * blue)
	# this is intentionally different from your example in that the color is not retained after the mouse leaves the triangle

def mouse(x, y):
	global xMouse
	global yMouse
	xMouse = x
	yMouse = windowHeight - y # get cursor position relative to bottom left instead
	calcAlpha() # get alpha, beta, and gamma
	drawTriangle() # redraw the triangle to effect the new color

def drawTriangle():
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	pickColor()

	glBegin(GL_TRIANGLES)
	glVertex2f(xA, yA)
	glVertex2f(xB, yB)
	glVertex2f(xC, yC)
	glEnd()

	glFlush()

def main():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
	glutInitWindowSize(int(windowWidth), int(windowHeight))
	glutInitWindowPosition(100, 100)
	glutCreateWindow("ICSI 422 Program 2 by Marcus Ross")
	initGL()

	glutPassiveMotionFunc(mouse)
	drawTriangle()

	glutMainLoop()

if __name__ == "__main__":
	main()