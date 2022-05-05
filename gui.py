import tkinter as tk
from tkinter import simpledialog,font
from extrafunctions import *
class GUIApp(tk.Tk):
    def __init__(self,name):
        super().__init__()
        super().title(name)
    def addWidget(self,widget):
        pass
    def getNamedChildren(self):
        custom_widgets = {key:value for key,value in self.children.items() if not key.startswith('!')}
        return(custom_widgets)

    def exportData(self,filename='gui-data.json'):
        gui_data ={}
        for widget_name,widget_obj in self.getNamedChildren().items():
            gui_data[widget_name] = widget_obj.getData()

        convertObjectToJson(gui_data,filename)
        


class CustomWidget(tk.LabelFrame):
    def __init__(self,parent,name,**kw):
        super().__init__(parent,text=name,padx=10,pady=10,name=name.lower().replace(' ','_'),**kw)
        self.value = dict()

    def getData(self):
        return(self.value.get())
    
    def printData(self):
        print(self.getData())

class EditableListBox(CustomWidget):
    def __init__(self,parent,name,**kw):
        super().__init__(parent,name,**kw)
        self.value= tk.StringVar()
        self.listbox = tk.Listbox(self,selectmode='extended',height=5,listvariable=self.value)

        self.button_frame = tk.Frame(self)
        self.add_button = tk.Button(self.button_frame,text='+',command=self.addThroughDialog)
        self.remove_button = tk.Button(self.button_frame,text='-',command=self.removeItem)
        self.clear_button = tk.Button(self.button_frame,text='x',command=self.clearItem)
        self.applyLayout()

    def addThroughDialog(self):
        response = simpledialog.askstring('','Enter URL')
        self.addItem(response)
        
    def addItem(self,item):
        self.listbox.insert(tk.END,item)

    def removeItem(self):
        selected = self.listbox.curselection()
        if selected == ():
            self.listbox.delete(tk.END)
        else:
            for index in selected[::-1]:
                self.listbox.delete(index)

    def clearItem(self):
        self.listbox.delete(0,tk.END)

    def applyLayout(self):
        self.pack(fill=tk.X,padx=10,pady=10)
        self.listbox.pack(side='left',fill=tk.X,expand=True)
        self.button_frame.pack(side='right')
        self.add_button.pack(side='top')
        self.remove_button.pack(side='top')
        self.clear_button.pack(side='top')
    def getData(self):
        string_list = self.value.get()[1:-1]
        string_list = string_list.replace('\'','')
        final_list = string_list.split(', ')

        return(final_list)
class Font(CustomWidget):
    def __init__(self,parent,name,**kw):
        super().__init__(parent,name,**kw)
        self.parent = parent

        self.selected_font = tk.StringVar()
        self.selected_style = tk.StringVar()
        self.selected_size = tk.IntVar()

        self.selected_font.set('Arial')
        self.selected_style.set('bold')
        self.selected_size.set(24)

        self.sample_label = tk.Label(self,font=self.getData(),text='Sample')
        # self.select_font_button = tk.Button(self,text='Select Font ...',command=self.selectFont)
        # self.font_entry = tk.Entry(self)
        # self.font_entry['textvariable']= selected_font
        size_list = (9,10,11,12,13,14,18,24,36,48,64,72,96,144,288)
        self.font_combo = tk.OptionMenu(self,self.selected_font,*font.families(),command=self.refreshSample)
        self.style_combo = tk.OptionMenu(self,self.selected_style,*(font.NORMAL,font.BOLD,font.ITALIC),command=self.refreshSample)
        self.size_combo = tk.OptionMenu(self,self.selected_size,*size_list,command=self.refreshSample)
        
        self.applyLayout()
    def refreshSample(self,variable):
        self.sample_label.configure(font=self.getData())

    # def selectFont(self):
    #     font_selector = FontSelector(self.parent)
         
    def applyLayout(self):
        self.pack(fill=tk.X,padx=10,pady=10)
        self.sample_label.pack(side='left',fill=tk.X,expand=True)
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
#         self.font_frame = tk.LabelFrame(self,text='Font')
#         # self.font_label = tk.Label(self.font_frame,text='Font')
#         self.font_listbox = tk.Listbox(self.font_frame,listvariable=tk.StringVar(value=font.families()),height=5)
        
#         self.style_frame = tk.LabelFrame(self,text='Font Style')
#         self.style_listbox = tk.Listbox(self.style_frame,listvariable=tk.StringVar(value=(font.NORMAL,font.BOLD,font.ITALIC)),height=5)
#         size_list = (9,10,11)
#         self.font_frame.pack(side='left',padx=10,pady=10)
#         self.font_listbox.pack()

#         self.style_frame.pack(side='left',padx=10,pady=10)
#         self.style_listbox.pack()
class TickBoxList(CustomWidget):
    def __init__(self,parent,name,item_list,**kw):
        super().__init__(parent,name,**kw)
        self.value = []
        for item in item_list:
            item_var = tk.StringVar(value=item)
            self.value.append(item_var)
            checkbox = tk.Checkbutton(self,variable=item_var,text=item,onvalue=item,offvalue='')
            checkbox.pack(side='left')
        self.remove_button = tk.Button(self,text='-',command=self.printData)
        self.pack(fill=tk.X,padx=10,pady=10)
        self.remove_button.pack()

    def getData(self):
        selected_items=list(filter(lambda item:item.get()!='',self.value))
        return([item.get() for item in selected_items])
class Slider(CustomWidget):
    def __init__(self,parent,name,minimum:int,maximum:int,**kw):
        super().__init__(parent,name,**kw)
        self.value = tk.IntVar(self,value=(minimum+maximum)//2)
        self.slider = tk.Scale(self,from_=minimum,to=maximum,
                            variable=self.value,
                            orient=tk.HORIZONTAL,
                            length=200,
                            sliderlength=10,
                            width=5,
                            tickinterval=100,
                            showvalue=False)
        self.entry_box = tk.Entry(self,width=3,validate="key",validatecommand=(self.register(self.ensureInt),'%P'),textvariable=self.value)
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
        self.pack(fill=tk.X,padx=10,pady=10)
        self.slider.pack(side='left',fill=tk.X,expand=True)
        self.entry_box.pack(side='left')
class FloatEntry(CustomWidget):
    def __init__(self,parent,name,label,**kw):
        super().__init__(parent,name,**kw)
        self.value = tk.IntVar()
        self.entry_box = tk.Entry(self,width=3,validate="key",validatecommand=(self.register(self.ensureFloat),'%P'),textvariable=self.value)
        self.label = tk.Label(self,text=label)
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
class RadioList(CustomWidget):
    def __init__(self,parent,name,option_list,**kw):
        super().__init__(parent,name,**kw)
        self.value = tk.StringVar(value=option_list[0])
        for item in option_list:
            checkbox = tk.Radiobutton(self,variable=self.value,text=item,value=item,command=self.getData)
            checkbox.pack()
        self.pack(fill=tk.X,padx=10,pady=10,side='left')


class ToggleButton(tk.Button):
    def __init__(self,parent,on_text,off_text,on_command,off_command,**kw):
        self.off_text = off_text
        self.on_text = on_text
        self.on_command = on_command
        self.off_command = off_command
        self.value = tk.StringVar(value=self.off_text)
        super().__init__(parent,textvariable=self.value,command=self.toggle,**kw)
    def toggle(self):
        if (self.value.get()==self.off_text):
            self.value.set(self.on_text)
            self.off_command()
        elif (self.value.get()==self.on_text):
            self.value.set(self.off_text)
            self.on_command()

def main():
    root = GUIApp('OBS Ticker')
    def on():
        print('on')
    def off():
        print('off')
    ToggleButton(root,'ON','OFF',on,off) 


    # scene_list = ['Scene 1','Coding']
    # scene_checklist = TickBoxList(root,'Scene Checklist',scene_list)
    # feed_list = EditableListBox(root,'Feed List')
    # for i in range(3):
    #     feed_list.addItem('abcd')
    #     feed_list.addItem('sfsdf')
    #     feed_list.addItem('ffhslf')
    # ticker_font = Font(root,'Ticker Font')
    # ticker_scroll_speed = Slider(root,'Text Scroll Speed',0,400)
    # empty_time =FloatEntry(root,'Sleep time between feeds','seconds')
    # text_direction= RadioList(root,'Text Direction',['Right to Left','Left to Right'])
    # start_button = tk.Button(root,text='Start▶️')
    # stop_button = tk.Button(root,text='Stop')
    # reset_button = tk.Button(root,text='Reset')
    # start_button.pack(side='top')
    # stop_button.pack(side='top')
    # reset_button.pack(side='top')
    # print(start_button.configure().keys())
    # # print(root.__dict__)
    # for widget_name,widget_obj in root.getNamedChildren().items():
    #     print(f'{widget_name} : {widget_obj.getData()}')
    root.mainloop()
if __name__ == '__main__':
    main()