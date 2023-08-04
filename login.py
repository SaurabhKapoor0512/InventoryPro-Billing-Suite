from tkinter import*
from PIL import Image,ImageTk  #pip install pillow
from tkinter import messagebox
import sqlite3
import os

class Login_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1360x700+0+0")
        self.root.title("Login System  | Developed By SAURABH KAPOOR | M.R.S Technology, Varanasi")
        self.root.config(bg="#fafafa")

#===========================ImportImages=======================
        self.phone_img=ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_phone_img=Label(self.root,image=self.phone_img,bd=0).place(x=200,y=50)
#===========================LoginFrame=========================
        self.emp_id=StringVar()
        self.password=StringVar()

        self.LoginFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        self.LoginFrame.place(x=670,y=90,width=350,height=460)

        title=Label(self.LoginFrame,text="Login System",font=("Elephant",30,'bold'),bg="white").place(x=0,y=30,relwidth=1)

        username=Label(self.LoginFrame,text="Employee ID",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_username=Entry(self.LoginFrame,textvariable=self.emp_id,font=("times new roman",15),bg="#ECECEC").place(x=50,y=140,width=250)

        password=Label(self.LoginFrame,text="Password",font=("Andalus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_password=Entry(self.LoginFrame,textvariable=self.password,show="*",font=("times new roman",15),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_Login=Button(self.LoginFrame,text="Log In",command=self.login,font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00B0F0",fg="White",cursor="hand2").place(x=50,y=300,width=250,height=35)

        hr=Label(self.LoginFrame,bg="Lightgrey").place(x=50,y=370,width=250,height=2)
        or_=Label(self.LoginFrame,text="OR",font=("times new Roman",15,"bold"),fg="Lightgrey",bg="white").place(x=150,y=355)

        btn_forget_pass=Button(self.LoginFrame,text="Forget Password ?",command=self.forget_password,font=("Times New Roman",13),bg="white",fg="#00759E",cursor="hand2",bd=0,activebackground="white",activeforeground="#00759E").place(x=100,y=390)


        #===================Frame2=====================
        RegistrationFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        RegistrationFrame.place(x=670,y=570,width=350,height=60)

        signUp=Label(RegistrationFrame,text="Final Year Project on Python",font=("Times new roman",15),bg="white").place(x=0,y=20,relwidth=1)
        
        
        #=================Header and Footer==================================
        #header=Label(self.root,text="InventoryPro Billing Suite (IMBS)",font=("goudy old style",20,'bold'),bg="white").pack(side=TOP,fill=X)
        #footer=Label(self.root,text="Developed By Saurabh Kapoor | For Technical Issue, Contact us on : 8687973793 or Email on : 1901650140018@kit.ac.in",fg="white",font=("times new roman",13,'bold'),bg="green").pack(side=BOTTOM,fill=X)
        
#===================================Animations=================================

        self.im1=ImageTk.PhotoImage(file="images/im1.png")
        self.im2=ImageTk.PhotoImage(file="images/im2.png")
        self.im3=ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_img=Label(self.root,bg="white")
        self.lbl_change_img.place(x=367,y=153,width=240,height=428)
        self.animate()
    
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_img.config(image=self.im)
        self.lbl_change_img.after(2000,self.animate)
    
    
    
    
    def login(self):
        con=sqlite3.connect(database=r'imbs.db')
        cur=con.cursor()
        try:
            if self.emp_id.get()=='' or self.password.get()=='':
                messagebox.showerror('Error','All Fields are required',parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? AND pass=?",(self.emp_id.get(),self.password.get()))
                user=cur.fetchone()
                if user==None:
                   messagebox.showerror('Error','Invalid Username/Password',parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
                   
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def forget_password(self):
        con=sqlite3.connect(database=r'imbs.db')
        cur=con.cursor()
        try:
            if self.emp_id.get()=='':
                messagebox.showerror('Error','Employee must be required',parent=self.root)
            else:
                cur.execute("select email from employee where eid=?",(self.emp_id.get(),))
                email=cur.fetchone()
                if email==None:
                   messagebox.showerror('Error','Invalid Employee Id, Try Again',parent=self.root)
                else:
                    #=========ForgetWindow=================
                    self.var_otp=StringVar()
                    self.new_pass=StringVar()
                    self.confirm_new_pass=StringVar()
                    #call send_email_fn()
                    self.forget_window=Toplevel(self.root)
                    self.forget_window.title("RESET PASSWORD")
                    self.forget_window.geometry('400x350+500+100')
                    self.forget_window.focus_force()

                    title=Label(self.forget_window,text="Reset Password",font=('goudy old style',15,'bold'),bg="#3f51b3",fg="white").pack(side=TOP,fill=X)
                    
                    lbl_reset=Label(self.forget_window,text="Enter OTP Sent on Registered Email",font=('times new roman',15)).place(x=20,y=60)
                    txt_reset=Entry(self.forget_window,textvariable=self.var_otp,font=('times new roman',15),bg="lightyellow").place(x=20,y=100,width=250,height=30)

                    self.btn_otp=Button(self.forget_window,text="Confirm",font=('times new roman',15),bg="lightblue",cursor="hand2")
                    self.btn_otp.place(x=280,y=100,width=100,height=30)

                    lbl_newPass=Label(self.forget_window,text="New Password",font=('times new roman',15)).place(x=20,y=160)
                    txt_newPass=Entry(self.forget_window,textvariable=self.new_pass,font=('times new roman',15),bg="lightyellow").place(x=20,y=190,width=250,height=30)

                    lbl_confirmPass=Label(self.forget_window,text="Confirm New Password",font=('times new roman',15)).place(x=20,y=225)
                    txt_confirmPass=Entry(self.forget_window,textvariable=self.confirm_new_pass,font=('times new roman',15),bg="lightyellow").place(x=20,y=255,width=250,height=30)

                    self.btn_update=Button(self.forget_window,text="Submit",font=('times new roman',15),state=DISABLED,bg="lightblue",cursor="hand2")
                    self.btn_update.place(x=150,y=300,width=100,height=30)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)
          

root=Tk()
obj=Login_System(root)
root.mainloop()