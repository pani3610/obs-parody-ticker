from tkinter import *
from tkinter import simpledialog,font
from tkinter import tix
from feed import Feed
class GUIApp:
    pass
class EditableListBox(LabelFrame):
    def __init__(self,parent,name):
        super().__init__(parent,text=name,padx=10,pady=10)

        self.listbox = Listbox(self,selectmode='extended',height=5)

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

        self.sample_label = Label(self,font=self.getData(),text='Sample')
        # self.select_font_button = Button(self,text='Select Font ...',command=self.selectFont)
        # self.font_entry = Entry(self)
        # self.font_entry['textvariable']= selected_font
        size_list = (9,10,11,12,13,14,18,24,36,48,64,72,96,144,288)
        self.font_combo = OptionMenu(self,self.selected_font,*font.families(),command=self.refreshSample)
        self.style_combo = OptionMenu(self,self.selected_style,*(font.NORMAL,font.BOLD,font.ITALIC),command=self.refreshSample)
        self.size_combo = OptionMenu(self,self.selected_size,*size_list,command=self.refreshSample)
        
        self.applyLayout()
    def refreshSample(self,variable):
        self.sample_label.configure(font=self.getData())

    # def selectFont(self):
    #     font_selector = FontSelector(self.parent)
         
    def applyLayout(self):
        self.pack(fill=X,padx=10,pady=10)
        self.sample_label.pack(side='left',fill=X,expand=True)
        # self.select_font_button.pack(side='right')
        # self.font_entry.pack()
        self.font_combo.pack(side='left')
        self.style_combo.pack(side='left')
        self.size_combo.pack(side='left')
    
    def getData(self):
        return((self.selected_font.get(),self.selected_size.get(),self.selected_style.get()))
# class FontSelector(Toplevel):
#     def __init__(self,parent):
#         super().__init__(parent)
#         self.font_frame = LabelFrame(self,text='Font')
#         # self.font_label = Label(self.font_frame,text='Font')
#         self.font_listbox = Listbox(self.font_frame,listvariable=StringVar(value=font.families()),height=5)
        
#         self.style_frame = LabelFrame(self,text='Font Style')
#         self.style_listbox = Listbox(self.style_frame,listvariable=StringVar(value=(font.NORMAL,font.BOLD,font.ITALIC)),height=5)
#         size_list = (9,10,11)
#         self.font_frame.pack(side='left',padx=10,pady=10)
#         self.font_listbox.pack()

#         self.style_frame.pack(side='left',padx=10,pady=10)
#         self.style_listbox.pack()
class TickBoxList(LabelFrame):
    def __init__(self,parent,name,item_list):
        super().__init__(parent,text=name,padx=10,pady=10)
        self.value = []
        for item in item_list:
            item_var = StringVar(value=item)
            self.value.append(item_var)
            checkbox = Checkbutton(self,variable=item_var,text=item,onvalue=item,offvalue='')
            checkbox.pack(side='left')
        self.remove_button = Button(self,text='-',command=self.getData)
        self.pack(fill=X,padx=10,pady=10)
        self.remove_button.pack()

    def getData(self):
        selected_items=list(filter(lambda item:item.get()!='',self.value))
        print([item.get() for item in selected_items])
class Slider(LabelFrame):
    def __init__(self,parent,name,minimum:int,maximum:int):
        super().__init__(parent,text=name,padx=10,pady=10)
        self.value = IntVar(self,value=(minimum+maximum)//2)
        self.slider = Scale(self,from_=minimum,to=maximum,
                            variable=self.value,
                            orient=HORIZONTAL,
                            length=200,
                            sliderlength=10,
                            width=5,
                            tickinterval=100,
                            showvalue=False)
        self.entry_box = Entry(self,width=3,validate="key",validatecommand=(self.register(self.ensureInt),'%P'),textvariable=self.value)
        self.applyLayout()
    def ensureInt(self,inp:str):
        if inp.isdigit():
            # print('digit')
            return(True)
        elif inp == '':
            # print('blank')
            return(True)
        else:
            print('invalid')
            return(False)

    def applyLayout(self):
        self.pack(fill=X,padx=10,pady=10)
        self.slider.pack(side='left',fill=X,expand=True)
        self.entry_box.pack(side='left')
    
    def getData(self):
        return(self.value)

class FloatEntry(LabelFrame):
    def __init__(self,parent,name,label):
        super().__init__(parent,text=name,padx=10,pady=10)
        self.value = IntVar()
        self.entry_box = Entry(self,width=3,validate="key",validatecommand=(self.register(self.ensureFloat),'%P'),textvariable=self.value)
        self.label = Label(self,text=label)
        self.applyLayout()
    def applyLayout(self):
        self.pack(padx=10,pady=10,side='left')
        self.entry_box.pack(side='left')
        self.label.pack(side='left')
    def ensureFloat(self,inp:str):
        try:
            value =float(inp)
            return(True)
        except ValueError:
            print('invalid')
            return(False)
    def getData(self):
        return(self.value.get())

class RadioList(LabelFrame):
    def __init__(self,parent,name,option_list):
        super().__init__(parent,text=name,padx=10,pady=10)
        self.value = StringVar(value=option_list[0])
        for item in option_list:
            checkbox = Radiobutton(self,variable=self.value,text=item,value=item,command=self.getData)
            checkbox.pack()
        self.pack(fill=X,padx=10,pady=10)

    def getData(self):
        print(self.value.get())
def main():
    root = Tk()
    # root.geometry("300x250")
    # frame = LabelFrame(root,text='Feed List')
    # frame.pack()
    scene_list = ['Scene 1','Coding']
    scene_checklist = TickBoxList(root,'Scene List',scene_list)
    feed_list = EditableListBox(root,'Feed List')
    for i in range(3):
        feed_list.addItem('abcd')
        feed_list.addItem('sfsdf')
        feed_list.addItem('ffhslf')
    ticker_font = Font(root,'Ticker Font')
    ticker_scroll_speed = Slider(root,'Text Scroll Speed',0,400)
    empty_time =FloatEntry(root,'Sleep time between feeds','seconds')
    text_direction= RadioList(root,'Text Direction',['Right to Left','Left to Right'])

    root.mainloop()
if __name__ == '__main__':
    main()