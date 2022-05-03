from tkinter import *
from tkinter import simpledialog

class GUIApp:
    pass
class EditableListBox():
    def __init__(self,parent):
        self.label = Label(parent,text='Feed List')
        self.listbox = Listbox(parent,selectmode='extended')
        self.add_button = Button(parent,text='+',command=self.addFeedURL)
        self.remove_button = Button(parent,text='-',command=self.removeItem)
        self.clear_button = Button(parent,text='x',command=self.clearItem)
        self.listbox.pack()
        self.label.pack(side='left')
        self.add_button.pack(side='right')
        self.remove_button.pack(side='right')
        self.clear_button.pack(side='right')
    def addFeedURL(self):
        response = simpledialog.askstring('','Enter URL')
        self.addItem(response)
    def addItem(self,item):
        self.listbox.insert(END,item)
    def removeItem(self):
        selected = self.listbox.curselection()
        if selected == ():
            self.listbox.delete(END)
        else:
            for index in selected[::-1]:
                self.listbox.delete(index)
    def clearItem(self):
        self.listbox.delete(0,END)
class FontSelector:
    pass

class TickBoxList:
    pass
def main():
    root = Tk()
    root.geometry("300x250")
    feed_list = EditableListBox(root)
    feed_list.addItem('abcd')
    feed_list.addItem('sfsdf')
    feed_list.addItem('ffhslf')
    root.mainloop()
if __name__ == '__main__':
    main()