from tkinter import *
from tkinter import simpledialog

class GUIApp:
    pass
class EditableListBox(LabelFrame):
    def __init__(self,parent,name):
        super().__init__(parent,text=name,padx=10,pady=10)
        # self.label = Label(parent,text='Feed List')
        self.listbox = Listbox(self,selectmode='extended',width=30)
        print(self.listbox.configure().keys())
        self.add_button = Button(self,text='+',command=self.addFeedURL)
        self.remove_button = Button(self,text='-',command=self.removeItem)
        self.clear_button = Button(self,text='x',command=self.clearItem)
        self.pack(fill=X,padx=10,pady=10)
        self.listbox.pack()
        # self.label.pack(side='left')
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

    def packAll(self):
        pass


class FontSelector:
    pass

class TickBoxList:
    pass
def main():
    root = Tk()
    # root.geometry("300x250")
    # frame = LabelFrame(root,text='Feed List')
    # frame.pack()
    feed_list = EditableListBox(root,'Feed List')
    for i in range(5):
        feed_list.addItem('abcd')
        feed_list.addItem('sfsdf')
        feed_list.addItem('ffhslf')
    root.mainloop()
if __name__ == '__main__':
    main()