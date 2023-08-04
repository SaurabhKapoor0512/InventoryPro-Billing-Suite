from tkinter import*
from PIL import Image,ImageTk  #pip install pillow 
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time

class IMBS:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1360x700+0+0")
        self.root.title("InventoryPro Billing Suite  | Developed By SAURABH KAPOOR | M.R.S Technology, Varanasi")
        self.root.config(bg="white")

        #====Title====
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="InventoryPro Billing Suite",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#101c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #====button logout====
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #=====Subtile and Clock=====
        self.lbl_clock=Label(self.root,text="Welcome to InventoryPro Billing Suite\t\t Date : DD-MM-YYYY\t\t Time : HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #======Left Menu=============
        self.MenuLogo=Image.open("images/menu_im.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        lbl_menulogo=Label(LeftMenu,image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP,fill=X)

        self.icon_side=PhotoImage(file="images/side.png")
        lbl_menu=Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009688").pack(side=TOP,fill=X)
        
        #=======Employee Button========
        btn_emp=Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        #=======Supplier Button========
        btn_sup=Button(LeftMenu,text="Supplier",command=self.supplier,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        #=======Category Button========
        btn_caty=Button(LeftMenu,text="Categories",command=self.category,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        #=======Product Button=========
        btn_prod=Button(LeftMenu,text="Products",command=self.product,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        #=======Sales Button===========
        btn_sales=Button(LeftMenu,text="Sales",command=self.sales,image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)
        #=======Exit Button============
        btn_exit=Button(LeftMenu,text="Exit",image=self.icon_side,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="white",bd=2,cursor="hand2").pack(side=TOP,fill=X)

        #========Content==============
        self.lbl_emp=Label(self.root,text="Total Employees\n[ 0 ]",bd=5,relief=RIDGE,bg="#33bbf9",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_emp.place(x=300,y=120,height=150,width=300)
        
        self.lbl_sup=Label(self.root,text="Total Suppliers\n[ 0 ]",bd=5,relief=RIDGE,bg="#ff5722",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sup.place(x=650,y=120,height=150,width=300)
        
        self.lbl_caty=Label(self.root,text="Total Category\n[ 0 ]",bd=5,relief=RIDGE,bg="#009688",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_caty.place(x=1000,y=120,height=150,width=300)

        self.lbl_prod=Label(self.root,text="Total Products\n[ 0 ]",bd=5,relief=RIDGE,bg="#607d8b",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_prod.place(x=300,y=300,height=150,width=300)

        self.lbl_sales=Label(self.root,text="Total Sales\n[ 0 ]",bd=5,relief=RIDGE,bg="#ffc107",fg="white",font=("goudy old style",20,"bold"))
        self.lbl_sales.place(x=650,y=300,height=150,width=300)

        #==================================================Footer==========================================================
        lbl_footer=Label(self.root,text="IMBS - InventoryPro Billing Suite | Developed By Team-SAURABH \nFor Any Technical Issue  Contact : 8687973793 or Email : saurabhkapoor@email.com",font=("times new roman",12),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)
        self.update_content()
#===============================================================================================================================================

    def employee(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=employeeClass(self.new_win)
    
    def supplier(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=supplierClass(self.new_win)
        
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=categoryClass(self.new_win)

    def product(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=productClass(self.new_win)

    def sales(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=salesClass(self.new_win)


    def update_content(self):
        con=sqlite3.connect(database=r'imbs.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product=cur.fetchall()
            self.lbl_prod.config(text=f'Total Products\n[ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_sup.config(text=f'Total Supplier\n[ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category=cur.fetchall()
            self.lbl_caty.config(text=f'Total Category\n[ {str(len(product))} ]')

            cur.execute("select * from employee")
            employee=cur.fetchall()
            self.lbl_emp.config(text=f'Total Employee\n[ {str(len(product))} ]')  

            bill=len(os.listdir('Bills'))
            self.lbl_sales.config(text=f'Total Sales\n[ {str(bill)} ]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"Welcome to InventoryPro Billing Suite\t\t Date : {str(date_)}\t\t Time : {str(time_)}")
            self.lbl_clock.after(200,self.update_content)     

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__=="__main__":
    root=Tk()
    obj=IMBS(root)
    root.mainloop()