from tkinter import *

class GUIApp:
    pass
class EditableListBox():
    def __init__(self,parent):
        self.listbox = Listbox(parent)
        self.listbox.pack()
    def addItem(self,item):
        self.listbox.insert(END,item)
class FontSelector:
    pass

class TickBoxList:
    pass
def main():
    root = Tk()
    root.geometry("300x250")
    feed_list = EditableListBox(root)
    feed_list.addItem('abcd')
    root.mainloop()
if __name__ == '__main__':
    main()