#!/usr/bin/python2.7
import urwid

class ListItem(urwid.FlowWidget):
    def __init__(self,label):
        self._label = label
    def selectable(self):
        return True
    def rows(self, size, focus):
        w = self.display_widget(size, focus)
        return w.rows(size, focus)
    def render(self, size, focus):
        w = self.display_widget(size, focus)
        
        return w.render(size, focus)
    def display_widget(self, size, focus):
        (maxcol,) = size
        num_pudding = maxcol - len(self._label)
        return urwid.Text(self._label)
    def keypress(self, size, key):
        return key
        
palette = [
    ('header', 'white', 'black'),
    #('reveal focus', 'black', 'dark cyan', 'standout'),
    #('normal', 'black', 'dark cyan', 'standout','#000','#f55'),
    ('normal', 'white', 'black'),
    ('focus', 'black', 'white'),
    #('focus', 'black', 'dark cyan', 'standout','#000','#fff'),
    ]

content1 = urwid.ListBox(urwid.SimpleListWalker([
    urwid.AttrMap(ListItem("ListItem 1"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 2"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 3"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 4"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 5"),'normal','focus'),]))

def liste():
    return urwid.ListBox(urwid.SimpleListWalker([
    urwid.AttrMap(ListItem("ListItem 1"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 2"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 3"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 4"),'normal','focus'),
    urwid.AttrMap(ListItem("ListItem 5"),'normal','focus'),]))

listbox = urwid.Columns([liste(),liste(),liste(),liste()])

show_key = urwid.Text("", wrap='clip')
head = urwid.AttrMap(show_key, 'header')
top = urwid.Frame(listbox, head)

def show_all_input(input, raw):
    show_key.set_text("Pressed: " + " ".join([
        unicode(i) for i in input]))
    return input

def exit_on_cr(input):
    if input == 'enter':
        raise urwid.ExitMainLoop()

loop = urwid.MainLoop(top, palette,
    input_filter=show_all_input, unhandled_input=exit_on_cr)
loop.screen.set_terminal_properties(colors=16) #1,16,88,256
#loop.screen.set_terminal_properties(bright_is_bold=True)

loop.run()
