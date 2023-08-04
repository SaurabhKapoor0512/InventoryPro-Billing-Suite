from tkinter import*
from PIL import Image,ImageTk  #pip install pillow 
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile

class BillClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1360x700+0+0")
        self.root.title("InventoryPro Billing Suite  | Developed By SAURABH KAPOOR | M.R.S Technology, Varanasi")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #====Title====
        self.icon_title=PhotoImage(file="images/logo1.png")
        title=Label(self.root,text="InventoryPro Billing Suite",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#101c48",fg="white",anchor="w",padx=20).place(x=0,y=0,relwidth=1,height=70)

        #====button logout====
        btn_logout=Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1150,y=10,height=50,width=150)

        #=====Subtile and Clock=====
        self.lbl_clock=Label(self.root,text="Welcome to InventoryPro Billing Suite\t\t Date : DD-MM-YYYY\t\t Time : HH:MM:SS",font=("times new roman",15),bg="#4d636d",fg="white")
        self.lbl_clock.place(x=0,y=70,relwidth=1,height=30)

        #=========================================================PART1(ProductFrame)=============================================================================
        self.var_search=StringVar()

        #=================ProductFrame1=========================
        ProductFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame.place(x=10,y=110,width=410,height=550)

        pTitle=Label(ProductFrame,text="All Products",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        #=================ProductFrame2=========================
        ProductFrame2=Frame(ProductFrame,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        lbl_search=Label(ProductFrame2,text="    Search Product | By Name",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_name=Label(ProductFrame2,text="Product Name",font=("times new roman",15,"bold"),bg="white").place(x=1,y=45)
        
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=130,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=290,y=45,width=100,height=25)
        btn_show=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=290,y=10,width=100,height=25)

        #=================TreeViewFrame(ProductFrame3)=====================
        ProductFrame3=Frame(ProductFrame,bd=3,relief=RIDGE)
        ProductFrame3.place(x=2,y=140,width=398,height=375)


        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        #CaseSensitive Query (DATABASE)
        self.Product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Product_Table.xview)
        scrolly.config(command=self.Product_Table.yview)

        self.Product_Table.heading("pid",text="ProductID")
        self.Product_Table.heading("name",text="Name")
        self.Product_Table.heading("price",text="Price")
        self.Product_Table.heading("qty",text="Qty")
        self.Product_Table.heading("status",text="Status")
        self.Product_Table["show"]="headings"    #Show Only Our Headings

        self.Product_Table.column("pid",width=80)
        self.Product_Table.column("name",width=100)             
        self.Product_Table.column("price",width=80)
        self.Product_Table.column("qty",width=50)
        self.Product_Table.column("status",width=80)
        self.Product_Table.pack(fill=BOTH,expand=1)
        self.Product_Table.bind("<ButtonRelease-1>",self.get_Data)

        lbl_note=Label(ProductFrame,text="Note : Enter 0 Quantity to remove Product from Cart",font=("goudy old style",12,"bold"),anchor=W,bg="white",fg="red").pack(side=BOTTOM,fill=X) 

#=============================================================PART2(CustomerFrame)=====================================================================================================
        self.var_custname=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)

        cTitle=Label(CustomerFrame,text="Customer Deatils",font=("goudy old style",15),bg="#009688").pack(side=TOP,fill=X)

        lbl_name=Label(CustomerFrame,text="Name",font=("times new roman",15),bg="white").place(x=5,y=35)        
        txt_name=Entry(CustomerFrame,textvariable=self.var_custname,font=("times new roman",13),bg="lightyellow").place(x=78,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact",font=("times new roman",15),bg="white").place(x=270,y=35)        
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=350,y=35,width=160)
        #========================Calculator & Cart Frame=============================
        CalciCartFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        CalciCartFrame.place(x=420,y=190,width=530,height=360)
        #=============================CalculatorFrame=================================
        self.var_calInput=StringVar()
        CalciFrame=Frame(CalciCartFrame,bd=9,relief=RIDGE,bg="white")
        CalciFrame.place(x=5,y=10,width=268,height=340)

        txt_calInput=Entry(CalciFrame,textvariable=self.var_calInput,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,justify=RIGHT,state='readonly')
        txt_calInput.grid(row=0,columnspan=4)

        btn_7=Button(CalciFrame,text="7",command=lambda:self.get_input(7),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(CalciFrame,text="8",command=lambda:self.get_input(8),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(CalciFrame,text="9",command=lambda:self.get_input(9),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_plus=Button(CalciFrame,text="+",command=lambda:self.get_input('+'),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(CalciFrame,text="4",command=lambda:self.get_input(4),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(CalciFrame,text="5",command=lambda:self.get_input(5),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(CalciFrame,text="6",command=lambda:self.get_input(6),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(CalciFrame,text="-",command=lambda:self.get_input('-'),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)

        btn_1=Button(CalciFrame,text="1",command=lambda:self.get_input(1),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(CalciFrame,text="2",command=lambda:self.get_input(2),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(CalciFrame,text="3",command=lambda:self.get_input(3),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_mul=Button(CalciFrame,text="*",command=lambda:self.get_input('*'),font=('arial',15,'bold'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)

        btn_0=Button(CalciFrame,text="0",command=lambda:self.get_input(0),font=('arial',15,'bold'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(CalciFrame,text="C",font=('arial',15,'bold'),command=self.clear_calci,bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=1)
        btn_equal=Button(CalciFrame,text="=",command=self.perform_cal,font=('arial',15,'bold'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(CalciFrame,text="/",command=lambda:self.get_input('/'),font=('arial',15,'bold'),bd=5,width=4,pady=15,cursor="hand2").grid(row=4,column=3)
        
        
        #==============================CartFrame========================================
        CartFrame=Frame(CalciCartFrame,bd=3,relief=RIDGE)
        CartFrame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(CartFrame,text="Cart\tTotal Product : [0]",font=("goudy old style",15),bg="lightgrey")
        self.cartTitle.pack(side=TOP,fill=X)
        scrolly=Scrollbar(CartFrame,orient=VERTICAL)
        scrollx=Scrollbar(CartFrame,orient=HORIZONTAL)

        #CaseSensitive Query (DATABASE)
        self.CartTable=ttk.Treeview(CartFrame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid",text="P ID")
        self.CartTable.heading("name",text="Name")
        self.CartTable.heading("price",text="Price")
        self.CartTable.heading("qty",text="Qty")
        
        self.CartTable["show"]="headings"    #Show Only Our Headings

        self.CartTable.column("pid",width=40)
        self.CartTable.column("name",width=100)             
        self.CartTable.column("price",width=90)
        self.CartTable.column("qty",width=40)
        
        self.CartTable.pack(fill=BOTH,expand=1)

        self.CartTable.bind("<ButtonRelease-1>",self.get_Data_cart)

        #===========================CartButtons==================================
        self.var_pid=StringVar()
        self.var_prodname=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_stock=StringVar()

        CartButtons=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        CartButtons.place(x=420,y=550,width=530,height=110)

        lbl_p_name=Label(CartButtons,text="Product Name",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_name=Entry(CartButtons,textvariable=self.var_prodname,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_price=Label(CartButtons,text="Price per Qty.",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_price=Entry(CartButtons,textvariable=self.var_price,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lbl_p_qty=Label(CartButtons,text="Quantity",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_qty=Entry(CartButtons,textvariable=self.var_qty,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(CartButtons,text="In Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clearCart=Button(CartButtons,text="Clear",command=self.clear_Cart,font=("times new roman",15,"bold"),bg="lightgrey",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_AddCart=Button(CartButtons,text="ADD | UPDATE",command=self.add_update,font=("times new roman",15,"bold"),bg="darkorange",cursor="hand2").place(x=340,y=70,width=180,height=30)

#=====================================================PART3(Customer Billing Area)======================================================================
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billFrame.place(x=953,y=110,width=410,height=410)

        bTitle=Label(billFrame,text="Customer Billing Area",font=("goudy old style",20,"bold"),bg="green",fg="white").pack(side=TOP,fill=X)

        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        self.txt_billArea=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_billArea.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_billArea.yview)

#==================================================Billing Buttons============================================================
        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        billMenuFrame.place(x=953,y=520,width=410,height=140)

        self.lbl_amt=Label(billMenuFrame,text="Bill Amount\n[0]",bd=2,relief=RIDGE,font=('goudy old style',13,"bold"),bg="#3f51b5",fg="white")
        self.lbl_amt.place(x=2,y=5,width=120,height=70)

        self.lbl_dis=Label(billMenuFrame,text="Discount\n[5%]",bd=2,relief=RIDGE,font=('goudy old style',15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_dis.place(x=124,y=5,width=120,height=70)

        self.lbl_netPay=Label(billMenuFrame,text="Net Amount Pay\n[0]",bd=2,relief=RIDGE,font=('goudy old style',13,"bold"),bg="orange",fg="white")
        self.lbl_netPay.place(x=246,y=5,width=160,height=70)

        btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,bd=1,relief=RAISED,font=('goudy old style',15,"bold"),bg="lightgreen",cursor="hand2")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clearAll=Button(billMenuFrame,text="Clear All",command=self.clear_All,bd=1,relief=RAISED,font=('goudy old style',15,"bold"),bg="grey",cursor="hand2")
        btn_clearAll.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billMenuFrame,text="Generate Bill\n or Save Bill",command=self.generate_bill,bd=1,relief=RAISED,font=('goudy old style',15,"bold"),bg="#009688",cursor="hand2")
        btn_generate.place(x=246,y=80,width=160,height=50)

        #============================FOOTER======================================
        footer=Label(self.root,text="IMBS - InventoryPro Billing Suite | Developed By Team-SAURABH \nFor Any Technical Issue  Contact : 8687973793 or Email : 1901650140018@kit.ac.in",font=("times new roman",12),bg="#101c48",fg="white").pack(side=BOTTOM,fill=X)

        self.show()
        #self.bill_top()
        self.update_date_time()


#=======================================================All Functions========================================================================

    def get_input(self,num):
        xnum=self.var_calInput.get()+str(num)
        self.var_calInput.set(xnum)

    def clear_calci(self):
        self.var_calInput.set('')

    def perform_cal(self):
        result=self.var_calInput.get()
        self.var_calInput.set(eval(result))

    def show(self):
        con=sqlite3.connect(database=r'imbs.db')
        cur=con.cursor()
        try:
            cur.execute("Select pid,name,price,qty,status from product where status='Active'")
            rows=cur.fetchall()
            self.Product_Table.delete(*self.Product_Table.get_children())
            for row in rows:
                self.Product_Table.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def search(self):
        con=sqlite3.connect(database=r'imbs.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)
            else:
                cur.execute("select pid,name,price,qty,status from product where name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.Product_Table.delete(*self.Product_Table.get_children())
                    for row in rows:
                        self.Product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    
    def get_Data(self,ev):
        f=self.Product_Table.focus()
        content=(self.Product_Table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_prodname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_instock.config(text=f"In Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')
        
        

    def get_Data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']     

        #pid,name,price,qty,stock
        self.var_pid.set(row[0])
        self.var_prodname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])
        self.lbl_instock.config(text=f"In Stock [{str(row[4])}]")
        self.var_stock.set(row[4])

    def add_update(self):
        if self.var_pid.get()=='':
            messagebox.showerror("Error","Please Select Product from the list",parent=self.root)
        elif self.var_qty.get()=='':
            messagebox.showerror("Error","Quantity is Required",parent=self.root)
        elif int(self.var_qty.get())>int(self.var_stock.get()):
            messagebox.showerror("Error","Invalid Quantity",parent=self.root)
        else:
            #price_cal=float(int(self.var_qty.get())*float(self.var_price.get()))    
            price_cal=self.var_price.get()
            cart_data=[self.var_pid.get(),self.var_prodname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]            

            #====================UpdateCart=====================
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_pid.get()==row[0]:
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno("Confirm","Product Already Present\n Do you want to update | Remove from the Cart List",parent=self.root)
                if op==True:
                    if self.var_qty.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #self.cart_list[index_][2]=price_cal #price
                        self.cart_list[index_][3]=self.var_qty.get() #quantity
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            self.bill_amt=self.bill_amt+(float(row[2])*int(row[3]))

        self.discount=(self.bill_amt*5)/100
        self.net_pay=self.bill_amt-self.discount
        self.lbl_amt.config(text=f'Bill Amount\n[{str(self.bill_amt)}]')
        self.lbl_netPay.config(text=f'Net Pay(Rs.)\n[{str(self.net_pay)}]')
        self.cartTitle.config(text=f'Cart\tTotal Product : [{str(len(self.cart_list))}]')
    
    
    def show_cart(self):        
        try:  
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)

    def generate_bill(self):
        if self.var_custname.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Customers Details are Required",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Please Add Product to The Cart",parent=self.root)

        else:
            #========BillTop=========
            self.bill_top()
            #========BillMid=========
            self.bill_middle()
            #========BillBottom======
            self.bill_bottom()
    
            fp=open(f'Bills/{str(self.invoice)}.txt','w')
            fp.write(self.txt_billArea.get('1.0',END))
            fp.close()
            messagebox.showinfo("Saved","Bill has been Generated & Saved in Records ",parent=self.root)
            self.chk_print=1
            
    

    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tTeam-SAURABH(KIT)
\tPhone No. 8687973793, Kanpur-208001
{str("="*47)}
 Customer Name : {self.var_custname.get()}
 Ph No. : {self.var_contact.get()}
 Bill No. {str(self.invoice)}\t\t\tDate : {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Product Name\t\t\tQTY\tPrice
{str("="*47)}
        '''
        self.txt_billArea.delete('1.0',END)
        self.txt_billArea.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Bill Amount\t\t\t\tRs.{self.bill_amt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_billArea.insert(END,bill_bottom_temp)

    def bill_middle(self):
        con=sqlite3.connect(database=r'imbs.db')
        cur=con.cursor()
        try:
            
            for row in self.cart_list:
                #pid,name,price,qty,stock
                
                pid=row[0]
                name=row[1]
                qty=int(row[4])-int(row[3])

                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'

                price=float(row[2])*int(row[3])
                price=str(price)
                self.txt_billArea.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
                #==================Update Quantity in Product Table===============
                cur.execute('Update product set qty=?,status=? where pid=?',(
                    qty,
                    status,
                    pid

                ))
                con.commit()
            con.close()
            self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to : {str(ex)}",parent=self.root)


    def clear_Cart(self):
        self.var_pid.set("")
        self.var_prodname.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.lbl_instock.config(text=f"In Stock")
        self.var_stock.set("")

    def clear_All(self):
        del self.cart_list[:]
        self.var_custname.set('')
        self.var_contact.set('')
        self.txt_billArea.delete('1.0',END)       
        self.cartTitle.config(text=f'Cart \t Total Product : [0]')
        self.var_search.set('')
        self.chk_print=0
        self.clear_Cart()
        self.show()
        self.show_cart()

    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"Welcome to InventoryPro Billing Suite\t\t Date : {str(date_)}\t\t Time : {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)
        
    def print_bill(self):
        if self.chk_print==1:
            messagebox.showinfo("Print","Please wait while printing",parent=self.root)
            new_file=tempfile.mktemp('.txt')
            open(new_file,'w').write(self.txt_billArea.get('1.0',END))
            os.startfile(new_file,'print')

        else:
            messagebox.showerror("Error","Please Generate Bill, to Print the receipt",parent=self.root)

    def logout(self):
        self.root.destroy()
        os.system("python login.py")
            


if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()