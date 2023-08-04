from tkinter import*
from PIL import Image,ImageTk  #pip install pillow 
from tkinter import ttk,messagebox
import sqlite3
import os

class salesClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("InventoryPro Billing Suite  | Developed By SAURABH KAPOOR | M.R.S Technology, Varanasi")
        self.root.config(bg="white")
        self.root.focus_force()
        self.bill_list=[]

        self.var_invoice=StringVar()
        #================Title===================
        
        lbl_title=Label(self.root,text="View Customer Bill",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        lbl_invoice=Label(self.root,text="Invoice No.",font=("Times New Roman",15),bg="white").place(x=50,y=100)
        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("Times New Roman",15),bg="lightyellow").place(x=160,y=100,width=180,height=28)
        #===============Buttons==================

        btn_search=Button(self.root,text="Search",command=self.search,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_clear=Button(self.root,text="Clear",command=self.clear,font=("times new roman",15,"bold"),bg="lightgrey",cursor="hand2").place(x=490,y=100,width=120,height=28)

        #====================Bill List======================
        sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
        sales_Frame.place(x=50,y=140,width=200,height=330)

        scrolly=Scrollbar(sales_Frame,orient=VERTICAL)

        self.sales_list=Listbox(sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)

        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.sales_list.yview)
        self.sales_list.pack(fill=BOTH,expand=1)
        self.sales_list.bind("<ButtonRelease-1>",self.get_Data)
        #=====================BillArea=======================

        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=410,height=330)
        #==================Bill Title=========================

        lbl_title2=Label(bill_Frame,text="Customer Bill Area",font=("goudy old style",20),bg="orange",).pack(side=TOP,fill=X)
        
        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.billarea=Text(bill_Frame,bg="lightyellow",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.billarea.yview)
        self.billarea.pack(fill=BOTH,expand=1)

        #=============Image==============
        self.bill_pic=Image.open("images/cat2.jpg")
        self.bill_pic=self.bill_pic.resize((450,300),Image.ANTIALIAS)
        self.bill_pic=ImageTk.PhotoImage(self.bill_pic)

        lbl_image=Label(self.root,image=self.bill_pic,bd=0)
        lbl_image.place(x=700,y=130)

        self.show()
#=======================================================================================================================
    def show(self):
        del self.bill_list[:]
        self.sales_list.delete(0,END)
        for i in os.listdir('Bills'):
            if i.split('.')[-1]=='txt':
                self.sales_list.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_Data(self,ev):   #ev passes to solve event error
        index_=self.sales_list.curselection()
        file_name=self.sales_list.get(index_)
        print(file_name)
        self.billarea.delete('1.0',END)
        fp=open(f'Bills/{file_name}','r')
        for i in fp:
            self.billarea.insert(END,i)
        fp.close()

    def search(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Invoice No. should be required",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                messagebox.showinfo("Success","Invoice Found")
                fp=open(f'Bills/{self.var_invoice.get()}.txt','r')
                self.billarea.delete('1.0',END)
                for i in fp:
                    self.billarea.insert(END,i)
                fp.close()

            else:
                messagebox.showerror("Error","Invlaid Invoice No.",parent=self.root)

    def clear(self):
        self.show()
        self.billarea.delete('1.0',END)

        
if __name__=="__main__":
    root=Tk()
    obj=salesClass(root)
    root.mainloop()