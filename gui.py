from tkinter import *
from tkinter import simpledialog,font
from feed import Feed
class GUIApp:
    pass
class EditableListBox(LabelFrame):
    def __init__(self,parent,name):
        super().__init__(parent,text=name,padx=10,pady=10)

        self.listbox = Listbox(self,selectmode='extended')

        self.button_frame = Frame(self)
        self.add_button = Button(self.button_frame,text='+',command=self.addThroughDialog)
        self.remove_button = Button(self.button_frame,text='-',command=self.removeItem)
        self.clear_button = Button(self.button_frame,text='x',command=self.clearItem)
        self.applyLayout()

    def addThroughDialog(self):
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
        self.add_button.pack(side='top')
        self.remove_button.pack(side='top')
        self.clear_button.pack(side='top')

    def getData(self):
        return(self.listbox.get(0,END))
class Font(LabelFrame):
    def __init__(self,parent,name):
        super().__init__(parent,text=name,padx=10,pady=10)
        self.parent = parent

        self.selected_font = StringVar()
        self.selected_style = StringVar()
        self.selected_size = IntVar()

        self.selected_font.set('Arial')
        self.selected_style.set('bold')
        self.selected_size.set(24)

        self.sample_label = Label(self,font=(self.selected_font.get(),self.selected_size.get(),self.selected_style.get()),text='Sample')
        # self.select_font_button = Button(self,text='Select Font ...',command=self.selectFont)
        # self.font_entry = Entry(self)
        # self.font_entry['textvariable']= selected_font
        size_list = (9,10,11,12,13,14,18,24,36,48,64,72,96,144,288)
        self.font_combo = OptionMenu(self,self.selected_font,*font.families(),command=self.refreshSample)
        self.style_combo = OptionMenu(self,self.selected_style,*(font.NORMAL,font.BOLD,font.ITALIC),command=self.refreshSample)
        self.size_combo = OptionMenu(self,self.selected_size,*size_list,command=self.refreshSample)
        
        self.applyLayout()
    def refreshSample(self,variable):
        self.sample_label.configure(font=(self.selected_font.get(),self.selected_size.get(),self.selected_style.get()))
    def selectFont(self):
        font_selector = FontSelector(self.parent)
         
    def applyLayout(self):
        self.pack(fill=X,padx=10,pady=10)
        self.sample_label.pack(side='left',fill=X,expand=True)
        # self.select_font_button.pack(side='right')
        # self.font_entry.pack()
        self.font_combo.pack(side='left')
        self.style_combo.pack(side='left')
        self.size_combo.pack(side='left')
class FontSelector(Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        self.font_frame = LabelFrame(self,text='Font')
        # self.font_label = Label(self.font_frame,text='Font')
        self.font_listbox = Listbox(self.font_frame,listvariable=StringVar(value=font.families()),height=5)
        
        self.style_frame = LabelFrame(self,text='Font Style')
        self.style_listbox = Listbox(self.style_frame,listvariable=StringVar(value=(font.NORMAL,font.BOLD,font.ITALIC)),height=5)
        size_list = (9,10,11)
        self.font_frame.pack(side='left',padx=10,pady=10)
        self.font_listbox.pack()

        self.style_frame.pack(side='left',padx=10,pady=10)
        self.style_listbox.pack()
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
    ticker_font = Font(root,'Ticker Font')
    root.mainloop()
if __name__ == '__main__':
    main()