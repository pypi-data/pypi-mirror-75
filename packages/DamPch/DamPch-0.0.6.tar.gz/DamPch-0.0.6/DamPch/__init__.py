

import tkinter
from tkinter import *
import hdpitkinter
from hdpitkinter import*
import re

class PCH:
    
    grp=[]


    def __init__(self):
        print("Placeholder and Binding classes initialised")
    
    def none(self):
        pass


    
    def dampch( root,  placeholder="This is a place holder",kbind=None, bfg="gray", afg= "black", afont= "Consolas", bfont="Consolas"):
        
        b=bfg
        a=afg

        def Po(self):
            
            if root.winfo_class()=='Entry' and root.get()== placeholder:
                root.config(foreground= afg , font=bfont )

                root.delete(0,END)
                root.bind("<Key>", kbind)

            elif root.winfo_class()=='Listbox'  :
                root.config(foreground= afg , font=bfont )
                root.delete(0,END)
            elif root.winfo_class()=='Text' and root.get('1.0', 'end'+'-1c')== placeholder:
                root.config(foreground= afg , font=bfont )
                root.delete('1.0',END)
            elif root.winfo_class()=='Message':
                root.config(foreground= afg , font=bfont )
                root.delete(0,END)

        def P1():
            d= root.get()

            
            if root.winfo_class()=='Entry' and d=="" :
                PCH.dampch(root, placeholder,kbind, bfg, afg, afont, bfont)


                
        def Po1(self):
            
            if root.winfo_class()=='Entry' and root.get()=="":
                
                PCH.dampch(root,  placeholder,kbind, bfg, afg, afont, bfont)


        def Po2(self):
            
            if root.get('1.0','end'+'-1c')== '':

                PCH.dampch(root,  placeholder,kbind, bfg, afg, afont, bfont)

        def Po3(self):
            
            if root.get(ANCHOR)== '':

                PCH.dampch(root,  placeholder,kbind, bfg, afg, afont, bfont)



            
        if root.winfo_class()=='Entry':
            
            root.config(foreground= bfg, font= afont)
            root.insert(1, str(placeholder))
            root.bind("<Button-1>", Po)
            root.bind("<Key>", Po)
            root.bind("<Leave>", Po1)
            
            

        elif root.winfo_class()=='Text':
            
            root.config(foreground= bfg, font= afont)        
            root.insert('1.0', str(placeholder))
      
            root.bind("<Button-1>", Po)
            root.bind("<Key>", Po)
            root.bind("<Leave>", Po2)

        elif root.winfo_class()=='Listbox':

            root.config(foreground= bfg, font= afont)        
            root.insert(1, str(placeholder))
      
            root.bind("<Button-1>", Po)
            root.bind("<Leave>", Po3)

    def dampsw(root,  placeholder="password", bfg="gray", afg= "black", afont= "Consolas 9", bfont="Consolas 9"):


        def Po11(self):
            if root.winfo_class()=='Entry' and root.get()=="" :
                PCH.dampsw(root,  placeholder, bfg, afg, afont, bfont)

        def Po112(self):

            if root.get()== placeholder:
                root.config(foreground= afg , font=bfont, show="*")

                root.delete(0,END)
      


        grp=[]
        root.configure(foreground= bfg, font= afont, show="")
        root.insert(1, str(placeholder))
        root.bind("<Button-1>", Po112)        
        root.bind("<Leave>", Po11)
        root.bind("<Key>", Po112)
        PCH.grp= grp

    def ShowPassWord(root):
        return root.get()

    def DelPassWord(root):
        return root.delete(0,END)



    def AuthName(root,placeholder="@gmail.com", bfg="gray", afg= "black", afont= "Consolas 9", bfont="Consolas 9"):

        def GPo(self):

            if root.winfo_class()=='Entry' and root.get()== placeholder:
                root.config(foreground= afg , font=bfont )

                root.delete(0,END)

        def GPo1(self):
            
            if root.winfo_class()=='Entry' and root.get()=="":
                
                PCH.AuthName(root,  placeholder, bfg, afg, afont, bfont)

        def GPo2(self):

            if not re.search(placeholder, root.get()):
                root.insert(END, placeholder)

            
        if root.winfo_class()=='Entry':
            
            root.config(foreground= bfg, font= afont)
            root.insert(1, str(placeholder))
            root.bind("<Button-1>", GPo)
            root.bind("<Key>", GPo)
            root.bind("<Leave>", GPo1)
            root.bind("<Tab>", GPo2)


    def AddSuggestion(root,route,op=['option-1','option-2','option-3'],pph="options",xx= 400,yy=400 ,cfg= "black", cfont= "Consolas 9",cbg="white"):
        global rootsug
        global sugg
        global ddfc

        def gg(self):
            global rootsug
            global sugg
            global ddfc

            try:
                rootsug.destroy()
                sugg.destroy()
                ddfc.destroy()
            except:
                print("Nothing to Destroy")
                      
        def Sigo(self):
            global rootsug
            global sugg
            global ddfc

            i =sugg.get(ANCHOR)

            root.delete(0,END)
            
            root.insert(1,str(i))

            try:
                sugg.destroy()
                rootsug.destroy()
                ddfc.destroy()

            except:
                
                print("Nothing to Destroy")
        



        def aGPo(self):

            if root.winfo_class()=='Entry' and root.get()== pph:
                root.configure(fg= cfg)

                root.delete(0,END)

        def aGPo1(self):
            
            if root.winfo_class()=='Entry' and root.get()=="":
                
                PCH.AddSuggestion(root, route, op ,pph, xx, yy, cfg, cfont, cbg)

        def bGPo(self):
            global rootsug
            global sugg
            global ddfc


            try:
                rootsug.destroy()
                sugg.destroy()

            except:
                print("Nothing to get destory")

                
            if root.winfo_class()=='Entry' and root.get()== pph:
                

                root.delete(0,END)

            root.configure(fg= cfg)
            rootsug = LabelFrame(route, border= 0)
            rootsug.place(x= xx , y = yy)
            sugg= Listbox(rootsug, border= 0, height=5)
            sugg.pack(fill= BOTH, side= 'left')
            sugg.bind("<Double-Button-1>",Sigo)
            ddfc= Scrollbar(rootsug)
            ddfc.pack(fill= Y, side= 'right')
            ddfc.configure(command= sugg.yview)
            sugg.configure(yscrollcommand= ddfc.set)
            sugg.bind("<Leave>", gg)
            
            for i_t_e_m in op:

                sugg.insert(END, str(i_t_e_m))
                
            #print([self.char])
            if self.char == "\x08" or self.char == "":

                try:
                    sugg.destroy()
                    rootsug.destroy()
                except:
                    print("Nothing to Destroy")

                


            
        def Tabbi(self):
            pass



        if root.winfo_class()=='Entry':
            root.config(foreground= "gray")
            root.insert(1,pph)

            
            
            root.bind("<Button-1>", aGPo)
            root.bind("<Key>", bGPo)
            root.bind("<Double-Button-1>", bGPo)
            root.bind("<Leave>", aGPo1)
            #route.bind("<Button-1>", gg)
            
            root.bind("<Tab>", Tabbi)            
        

        
    def AddSugCustom(root,route,op=['option-1','option-2','option-3'],pph="options",xx= 400,yy=400 ,cfg= "black", cfont= "Consolas 9",cbg="white",lbg='white',lfg='black'):
        
        global rootsug1
        global sugg1
        global ddfc1

        def gg1(self):
            global rootsug11
            global sugg1
            global ddfc1

            try:
                rootsug1.destroy()
                sugg1.destroy()
                ddfc1.destroy()
            except:
                print("Nothing to Destroy")
                      
        def Sigo1(self):
            global rootsug1
            global sugg1
            global ddfc1

            i =sugg1.get(ANCHOR)

            root.delete(0,END)
            
            root.insert(1,str(i))

            try:
                sugg1.destroy()
                rootsug1.destroy()
                ddfc1.destroy()

            except:
                
                print("Nothing to Destroy")
        



        def aGPo1(self):

            if root.winfo_class()=='Entry' and root.get()== pph:
                root.configure(fg= cfg)

                root.delete(0,END)

        def aGPo11(self):
            
            if root.winfo_class()=='Entry' and root.get()=="":
                
                PCH.AddSugCustom(root, route, op ,pph, xx, yy, cfg, cfont, cbg, lbg, lfg)

        def bGPo1(self):
            global rootsug1
            global sugg1
            global ddfc1


            try:
                rootsug1.destroy()
                sugg1.destroy()

            except:
                print("Nothing to get destory")

                
            if root.winfo_class()=='Entry' and root.get()== pph:
                

                root.delete(0,END)

            root.configure(fg= cfg)
            rootsug1 = Frame(route, border= 0)
            rootsug1.place(x= xx , y = yy)
            sugg1= Listbox(rootsug1, border= 0, height=5, bg= lbg, fg= lfg)
            sugg1.pack(fill= BOTH, side= 'left')
            sugg1.bind("<Double-Button-1>",Sigo1)
            ddfc1= Scrollbar(rootsug1)
            ddfc1.pack(fill= Y, side= 'right')
            ddfc1.configure(command= sugg1.yview)
            sugg1.configure(yscrollcommand= ddfc1.set)
            sugg1.bind("<Leave>", gg1)
            
            for i_t_e_m in op:

                sugg1.insert(END, str(i_t_e_m))
                
            #print([self.char])
            if self.char == "\x08" or self.char == "":

                try:
                    sugg1.destroy()
                    rootsug1.destroy()
                except:
                    print("Nothing to Destroy")

                


            
        def Tabbi1(self):
            pass



        if root.winfo_class()=='Entry':
            root.config(foreground= "gray")
            root.insert(1,pph)

            
            
            root.bind("<Button-1>", aGPo1)
            root.bind("<Key>", bGPo1)
            root.bind("<Double-Button-1>", bGPo1)
            root.bind("<Leave>", aGPo11)
            #route.bind("<Button-1>", gg)
            
            root.bind("<Tab>", Tabbi1)            
                
        

if __name__=='__main__':

    PCH()





       


