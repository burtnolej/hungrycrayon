import curses
import re

l = ['last','fast','past','pest','mess','ask','gas']

l2 = ["["+_l+"]" for _l in l]
    
str = " ".join(l2)


#myscreen = curses.initscr()
#myscreen.border(0)

p = re.compile('as')
matches = p.finditer(str)

startpos = re.compile('[')
matches = p.finditer(str)

endpos = re.compile(']')
matches = p.finditer(str)

for match in matches:
    print match.group(), match.span()

for i in range(len(l2)):
    print startpos[i],endpos[i]
               
#myscreen.addstr(3, 3, result)

#myscreen.refresh()
#myscreen.getch()

#curses.endwin()