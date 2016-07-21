import Tkinter as tk
import tkFont

master = tk.Tk()

class color_enum:    
    black='#000000'
    white='#fff'
    grey='#d3d3d3'
    pink='#ff69b4'

color = color_enum()

class font_enum:
    ubuntumono14b=tkFont.Font(master,family='Ubuntu Mono',size=14, weight='bold')
    ubuntumono14i=tkFont.Font(master,family='Ubuntu Mono',size=14, weight='normal')
    
font = font_enum()

frame = tk.Frame(master)
frame.grid(row=2,column=1,sticky = tk.W)

def button(width,height):
    return(tk.Button(frame,
                       text="test",
                       width=width,
                       height=height,
                       background=color.pink,
                       foreground=color.black,
                       font=font.ubuntumono14b))
   
button(20,20).grid(row=1,column=1,sticky=tk.N)
button(20,20).grid(row=2,column=1,sticky=tk.N)
master.mainloop()