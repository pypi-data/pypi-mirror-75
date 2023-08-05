import ctypes
import tkinter as tk
from tkinter import *
import random
import re
import PIL
from PIL import ImageTk,Image


'''import tkinter
from tkinter import *

s= Tk()



d=Button(s, text= "Hello World")
d.pack()


s.mainloop()'''




class ModTk(tk.Tk):
    
    

    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    


class ModFrame(tk.LabelFrame):
    
    global x,y,x1,y1
    x= 0
    y=0
    x1= 0
    y1=0
    global true
    global false
    true= False
    false= False
        
    def FrameContainsHor(self,args=[], bcolor="#313335", fcolor="#D3D3D3"):
        global x,y
        global true
        
        cc= ['yellow','orange','gray','purple']

        for color in cc:
            if color==bcolor or color==fcolor:
                cc.remove(color)
        r=random.choice(cc)
        
        for i in args:
            i.grid(row=y ,column= x , padx= 10 , pady = 20)
            
            i.configure(bg= bcolor, fg= fcolor)

            if i.winfo_class()=="Button":
                i.configure(activebackground=bcolor, activeforeground=r)
            '''
            elif i.winfo_class()=="Entry":
                i.configure(fg=r)
            '''
            x+=1
        true=True

    def AddRow(self, args=[], bcolor="#313335", fcolor="#D3D3D3"):
        global x,y
        global true


        if true:
            y=y+1
            cc= ['yellow','orange','gray','purple']
            x=0
            for color in cc:
                if color==bcolor or color==fcolor:
                    cc.remove(color)
            r=random.choice(cc)
            
            for i in args:

                i.grid(row=y ,column= x , padx= 10 , pady = 20)
                
                i.configure(bg= bcolor, fg= fcolor)

                if i.winfo_class()=="Button":
                    i.configure(activebackground=bcolor, activeforeground=r)
                '''
                elif i.winfo_class()=="Entry":
                    i.configure(fg=r)
                '''
                x+=1
        else:
            print("ModTkinter.EncounterProblem.CannotAddRow.Error#001")
            
         
        
    def FrameContainsVer(self,args=[], bcolor="#313335", fcolor="#D3D3D3"):
        global x1,y1
        cc1= ['yellow','orange','gray','purple']

        global false
        


        r1=random.choice(cc1)
        
        for i in args:
            i.grid(row=y1 ,column= x1 , padx= 10 , pady = 20)
            
            i.configure(bg= bcolor, fg= fcolor)

            if i.winfo_class()=="Button":
                i.configure(activebackground=bcolor, activeforeground=r1)
            '''
            elif i.winfo_class()=="Entry":
                i.configure(fg=r)
            '''
            y1+=1
        false=True    

    def AddColumn(self, args=[], bcolor="#313335", fcolor="#D3D3D3"):
        global x1,y1
        global false

        if false:
            x1=x1+1
            cc1= ['yellow','orange','gray','purple']
            y1=0
            for color in cc1:
                if color==bcolor or color==fcolor:
                    cc1.remove(color)
            r1=random.choice(cc1)
            
            for i in args:
                i.grid(row=y1 ,column= x1 , padx= 10 , pady = 20)
                
                i.configure(bg= bcolor, fg= fcolor)

                if i.winfo_class()=="Button":
                    i.configure(activebackground=bcolor, activeforeground=r1)
                '''
                elif i.winfo_class()=="Entry":
                    i.configure(fg=r)
                '''
                y1+=1
        else:
            print("ModTkinter.EncounterProblem.CannotAddRow.Error#001")
            

class ModButton(tk.Button):
    
    __lp= []


    def Class(self,bgg,Blass="Default"):
        global Img,Img1
        global Img2,Img3
        global Img4,Img5
        global Img6,Img7
        global Img8
        global img,img1
        global img2,img3
        global img4,img5
        global img6,img7
        global img8
        

        c= []


     
        
        aspd= self['text']

        gra= self['font']
        print(gra)
        try:
            gra=int(gra.split(" ")[1])

            y= gra+gra//2
            x= gra+gra//2
        except:
            #pass
            x= 12
            y= 12



        w=re.split("\n",aspd)

        i= len(w)
        #print(i)

        #x*= i
        y*= i

        for s in w:
            c.append(len(s))

        so= max(c)

        d= c.index(so)
            

        see= w[d]

        
       
        img= Image.open("ButDef.png")
        img= img.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)
        Img= ImageTk.PhotoImage(img)

        img1=Image.open("ButMaceWindu.png")
        img1= img1.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)
        Img1= ImageTk.PhotoImage(img1)

        img2= Image.open("ButYoda.png")
        img2= img2.resize((75+len(see)*x,57+(y*i)),Image.ANTIALIAS)
        Img2= ImageTk.PhotoImage(img2)

        img3= Image.open("ButInfo.png")       
        img3= img3.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)    
        Img3= ImageTk.PhotoImage(img3)

        img4=Image.open("ButAlert.png")    
        img4= img4.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)    
        Img4= ImageTk.PhotoImage(img4)

        img5=Image.open("ButBored.png")        
        img5= img5.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)    
        Img5= ImageTk.PhotoImage(img5)

        img6=Image.open("ButCyan.png")  
        img6= img6.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)    
        Img6= ImageTk.PhotoImage(img6)

        img7=Image.open("ButCartoonish.png")        
        img7= img7.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)    
        Img7= ImageTk.PhotoImage(img7)

        img8=Image.open("ButDask.png")  
        img8= img8.resize((80+len(see)*x,60+(y*i)),Image.ANTIALIAS)    
        Img8= ImageTk.PhotoImage(img8)

        f= bgg['background']

        if Blass=="Default":
            self.configure(image= Img,border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)            

     
            if self['foreground']!="white":
                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img)

        elif Blass=="Violet-Ver" :
            self.configure(image= Img1,border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)

            #print(l)
        
            if self['foreground']!="white":
                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)
                self.__lp.append(Img1)
                #print(l)
        

        elif Blass=="Success":

           self.configure(image= Img2,border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)
           if self['foreground']!="white":     

                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img2)
    
        elif Blass=="Info-Type":
            self.configure(image= Img3,border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)

     
            if self['foreground']!="white":
                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img3)
        


        elif Blass=="Alert":

           self.configure(image=Img4,border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)
           if self['foreground']!="white":     

                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img4)

        elif Blass=="Cliche":

           self.configure(image= Img5,border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)
           if self['foreground']!="white":     

                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img5)

        elif Blass=="Guardian":

           self.configure(image= Img6,border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)
           if self['foreground']!="white":     

                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img6)

        elif Blass=="Cartoon":

           self.configure(border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)
           if self['foreground']!="white":     

                self.configure(image= Img7,border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img7)

        elif Blass=="Dask-Type":

           self.configure(image= Img8,border=0,bg=f ,activebackground=f,activeforeground="black", text=self['text'], compound= CENTER)
           if self['foreground']!="white":     

                self.configure(border=0,bg=f ,activebackground=f,activeforeground="white", text=self['text'], compound= CENTER)


                self.__lp.append(Img8)

        print(self.__lp)
        print(len(self.__lp))




if __name__== '__main__':
    #ModTk()
    #ModFrame()

    print("Objects of package initialised")









