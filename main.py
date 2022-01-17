from curses import wrapper , textpad
import curses
import random
score = 0


def endScreen(stdscr):
    global score
    stdscr.nodelay(False)
    curses.beep()
    stdscr.erase()
    lry , lrx = stdscr.getmaxyx()
    text = f'''
   _________    _____   ____     _______  __ ___________ 
  / ___\__  \  /     \_/ __ \   /  _ \  \/ // __ \_  __ \\
 / /_/  > __ \|  Y Y  \  ___/  (  <_> )   /\  ___/|  | \/
 \___  (____  /__|_|  /\___  >  \____/ \_/  \___  >__|   
/_____/     \/      \/     \/                   \/       
                
                        SCORE: {score}

    '''
    subscr = stdscr.subwin((lry-8)//2, (lrx-56)//2)
    subscr.addstr(0,0,text, curses.color_pair(1))
    stdscr.refresh()
    curses.napms(2000)
    stdscr.getkey()



def getFood(lry , lrx , snake):
    return random.choice([(x,y) for x in range(3 , lrx-3) for y in range(3 , lry-3) if (x,y) not in snake])


def getSnake(lry , lrx , direction , snake , extend):
    if not snake:
        x , y = random.randint(4,lrx-6) , random.randint(4 ,lry-4)
        snake.extend([(x ,y) , (x+1 , y) , (x+2 , y)])
        return snake
    else:
        x , y = snake[-1]
        if not extend:
            snake.pop(0)
        if direction == curses.KEY_RIGHT:
            snake.append((x+1,y))
        if direction == curses.KEY_LEFT:
            snake.append((x-1,y))
        if direction == curses.KEY_UP:
            snake.append((x,y-1))
        if direction == curses.KEY_DOWN:
            snake.append((x,y+1))
        x_head , y_head = snake[-1]
        if x_head >= lrx-2 or y_head >= lry-2 or x_head <= 2 or y_head <= 2 or (x_head , y_head) in snake[:-1]:
            return "END"
        return snake

def main(stdscr):
    curses.resize_term(30,120)
    curses.init_pair(1, 6 , 0)
    curses.init_pair(2, 3 , 0)
    curses.init_pair(3, 2 , 0)
    global score
    snake , direction , food , extend = []  , curses.KEY_RIGHT , () , False
    while True:
        stdscr.erase()
        lry , lrx = stdscr.getmaxyx()
        stdscr.addstr(1, (lrx- 6)//2,f"SCORE:{score}", curses.A_BOLD)
        textpad.rectangle(stdscr , 2, 2 , lry-2, lrx-2)
        curses.curs_set(False)
        stdscr.nodelay(True)
        choice = stdscr.getch()

        valid = [choice == curses.KEY_RIGHT and direction != curses.KEY_LEFT, 
                 choice == curses.KEY_DOWN and direction != curses.KEY_UP,
                 choice == curses.KEY_LEFT and direction != curses.KEY_RIGHT,
                 choice == curses.KEY_UP and direction != curses.KEY_DOWN] 

        if any(valid):
            direction = choice

        if not food:
            food = getFood(lry , lrx , snake)
        stdscr.addstr(food[1] ,food[0]  , "@" , curses.color_pair(1))

        snake = getSnake(lry ,lrx ,  direction , snake , extend)
        if snake == "END":
            return endScreen(stdscr)
        for x , y in snake:
            stdscr.addstr(y,x ,"O" , curses.color_pair(2))
        stdscr.addstr(y,x ,"%" , curses.color_pair(3))
        extend = False

        if (x,y) == food:
            food = None
            score += 1
            extend = True


        stdscr.refresh() 
        curses.napms(50)

wrapper(main)


