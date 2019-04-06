import curses
import time
import random


startlength = 5
growlength =1 
speed = {'Easy':0.1,'Medium':0.06, 'Hard':0.04}
difficulty = 'Medium'
accelration = True
screen = curses.initscr() # initialise the screen
screen.keypad(1) #take input from keyboard
h,w= screen.getmaxyx() #the screen dimensions


def game():
  screen.clear()#clear the screen in the start
  curses.start_color() #black background
  curses.curs_set(0)# cursor visibility zero
  curses.noecho() #does not echo the keys pressed
  screen.border() # sets a border
  screen.nodelay(1)# so we dont have to wait for anything to happen
  head = [random.randrange(1,h-1),random.randrange(1,w-1)]
  body = [head[:]]*startlength
  
  gameover = False
  direction = 0 # 0: right, 1: down, 2: left, 3: up 
  q=0
  deadcell = body[-1][:]
  foodmade = False

  while not gameover:
    while not foodmade:
      y,x = random.randrange(1, h-1),random.randrange(1,w-1)
      if screen.inch(y,x) == ord(' '):
        screen.addch(y,x,ord('$'))
        foodmade = True

    if deadcell not in body:
      screen.addch(deadcell[0],deadcell[1],' ')
    
    action = screen.getch()
    if action == curses.KEY_UP and direction != 1:
      direction =3
    if action == curses.KEY_DOWN and direction != 3:
      direction =1
    if action == curses.KEY_LEFT and direction != 0:
      direction =2
    if action == curses.KEY_RIGHT and direction != 2:
      direction =0

    screen.addch(head[0],head[1], curses.ACS_CKBOARD)

    if direction == 0:
      head[1] += 1
    if direction == 2:
      head[1] -= 1
    if direction == 1:
      head[0] += 1
    if direction == 3:
      head[0] -= 1
        
    deadcell = body[-1][:]
    for z in range(len(body)-1,0,-1):
      body[z] = body[z-1][:]

    body[0] = head[:]
    #check for border
    if screen.inch(head[0],head[1]) != ord(' '):
      if screen.inch(head[0],head[1]) == ord('$'):
        foodmade = False

        for i in range(growlength):
          body.append(body[-1])

      else:
        gameover = True
    screen.refresh()
    if not accelration:
      time.sleep(speed[difficulty])
    else:
      time.sleep(15.*speed[difficulty]/len(body))

  screen.clear()
  screen.nodelay(0)
  message1 = "Game Over"
  message2 = 'Your Score is '+ str(int((len(body)-startlength)/growlength))
  message3 = 'Press Space to play again'
  message4 = 'Press Enter to quit'
  message5 = 'Press M to go back to the menu'
  screen.addstr(int(h/2-1),int((w-len(message1))/2),message1)
  screen.addstr(int(h/2),int((w-len(message2))/2),message2)
  screen.addstr(int(h/2+1),int((w-len(message3))/2),message3)
  screen.addstr(int(h/2+2),int((w-len(message4))/2),message4)
  screen.addstr(int(h/2+3),int((w-len(message5))/2),message5)

  screen.refresh()
  while q not in [32,10,77,109]:
    q = screen.getch()

  if q== 32:
    screen.clear()
    game()
  elif q == 10:
    curses.endwin()
  elif q in [77,109]:
    menu()

def menu():
  screen.nodelay(0)
  screen.clear()
  curses.noecho()
  curses.curs_set(0)# cursor visibility zero
  selection = -1
  option = 0
  while selection < 0:
    graphics = [0]*5
    graphics[option] = curses.A_REVERSE
    screen.addstr(int(0),int(w/2-3), 'Snake')
    screen.addstr(int(h/2-2),int(w/2-2),'Play',graphics[0])
    screen.addstr(int(h/2-1),int(w/2-6),'Instructions',graphics[1])
    screen.addstr(int(h/2),int(w/2-6),'Game Options',graphics[2])
    screen.addstr(int(h/2+1),int(w/2-5),'High Scores',graphics[3])
    screen.addstr(int(h/2+2),int(w/2-2),'Exit',graphics[4])
    screen.refresh()
    action = screen.getch()
    if action == curses.KEY_UP:
      option = (option-1) %5
    if action == curses.KEY_DOWN:
      option = (option+1) %5
    if action == ord('\n'):
      selection = option
  
  if selection == 0:
    game()
  elif selection ==1:
    instructions()
  elif selection ==2:
    gameoptions()

def instructions():
  screen.clear()
  screen.nodelay(0)
  lines = ['Use arrow keys to move','dont run into yourself or the snake',' ','Press any key to go back']
  
  z = 0
  for z in range(len(lines)):
    screen.addstr(int((h-len(lines))/2+z),int((w-len(lines[z]))/2),lines[z])
  
  screen.refresh()
  screen.getch()
  menu()

def gameoptions():
  global startlength,growlength,difficulty,accelration
  screen.clear()
  selection = -1
  option = 0

  while selection < 4:
    screen.clear()
    graphics = [0]*5
    graphics[option] = curses.A_REVERSE
    strings = ['Starting snake length: '+ str(startlength),'Snake Growth rate: '+str(growlength),'Difficulty: '+ str(difficulty),'Accelration: '+ str(accelration),'Exit']
    for z in range(len(strings)):
      screen.addstr(int((h-len(strings))/2+z),int((w-len(strings[z]))/2),strings[z],graphics[z])
    screen.refresh()
    action = screen.getch()

    if action == curses.KEY_UP:
      option = (option-1) %5
    if action == curses.KEY_DOWN:
      option = (option+1) %5
    if action == ord('\n'):
      selection = option
    if action == curses.KEY_RIGHT:

      if option ==0 and startlength <20:
        startlength +=1
      elif option ==1 and growlength <10:
        growlength +=1

    if action == curses.KEY_LEFT:

      if option ==0 and startlength >3:
        startlength -=1
      elif option ==1 and growlength >1:
        growlength -=1


    if selection == 3:
      accelration = not accelration
    if selection == 2:
      if difficulty =='Easy':
        difficulty = 'Medium'
      elif difficulty == 'Medium':
        difficulty = 'Hard'
      else:
        difficulty = 'Easy'
    if selection < 4:
      selection = -1

  menu()


menu()
curses.endwin()