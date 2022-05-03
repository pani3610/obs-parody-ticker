from tkinter import *
from tkinter import simpledialog

class GUIApp:
    pass
class EditableListBox(LabelFrame):
    def __init__(self,parent,name):
        super().__init__(parent,text=name,padx=10,pady=10)

        self.listbox = Listbox(self,selectmode='extended')

        self.button_frame = Frame(self)
        self.add_button = Button(self.button_frame,text='+',command=self.addFeedURL)
        self.remove_button = Button(self.button_frame,text='-',command=self.removeItem)
        self.clear_button = Button(self.button_frame,text='x',command=self.clearItem)

        self.applyLayout()

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

    def applyLayout(self):
        self.pack(fill=X,padx=10,pady=10)
        self.listbox.pack(side='left',fill=X,expand=True)
        self.button_frame.pack(side='right')
        # self.label.pack(side='left')
        self.add_button.pack(side='top')
        self.remove_button.pack(side='top')
        self.clear_button.pack(side='top')

    def getData(self):
        return(self.listbox.get(0,END))
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
    for i in range(3):
        feed_list.addItem('abcd')
        feed_list.addItem('sfsdf')
        feed_list.addItem('ffhslf')
    print(feed_list.getData())
    root.mainloop()
if __name__ == '__main__':
    main()