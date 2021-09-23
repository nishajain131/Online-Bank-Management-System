from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image,ImageTk
import re
import decimal
from decimal import *
import mysql.connector

global root
global regex
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
root = Tk()
root.minsize(1600,1100)
root.maxsize(1688,1126)

class register:
    def __init__(self,root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("1920x1700+0+0")
        
        #bg image

        self.bg=ImageTk.PhotoImage(file='images/bgg.jpg')
        bg = Label(self.root,image=self.bg).place(x=0,y=0,relwidth=1,relheight=1)
        
        #---------------------------------------------------registeration frame-----------------------------------------------------------------------------#
        global frame1
        frame1 = Frame(self.root,bg="white")
        frame1.place(x=550,y=200,width=800,height=650)

        title = Label(frame1,text = "SIGN UP",font=('times new roman',20,'bold'),bg='white',fg='green').place(x=300,y=40)

        f_name = Label(frame1,text = "FIRST NAME",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=50,y=100)
        self.txt_fname = Entry(frame1,font=("times new roman",15),bg = "white") 
        self.txt_fname.place(x=50,y=130,width = 300,height=30) 
       

        l_name = Label(frame1,text = "LAST NAME",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=370,y=100)
        self.txt_lname = Entry(frame1,font=("times new roman",15),bg = "white")
        self.txt_lname.place(x=370,y=130,width = 300,height=30)

        mail = Label(frame1,text = "EMAIL",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=50,y=160)
        self.txt_mail = Entry(frame1,font=("times new roman",15),bg = "white") 
        self.txt_mail.place(x=50,y=190,width = 300,height=30)

        p_num = Label(frame1,text = "PHONE NUMBER",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=370,y=160)
        self.txt_pnum = Entry(frame1,font=("times new roman",15),bg = "white") 
        self.txt_pnum.place(x=370,y=190,width = 300,height=30) 


        address = Label(frame1,text = "ADDRESS",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=50,y=230)
        self.txt_address = Entry(frame1,font=("times new roman",15),bg = "white")
        self.txt_address.place(x=50,y=260,width = 640,height=80)


        dob = Label(frame1,text = "AGE IN YEARS",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=50,y=360)
        self.txt_dob = Entry(frame1,font=("times new roman",15),bg = "white")
        self.txt_dob.place(x=50,y=390,width = 300,height=30)
        



        gender = Label(frame1,text = "GENDER",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=370,y=360)
        self.cmb_gender = ttk.Combobox(frame1,font=("times new roman",15),state='readonly',justify = CENTER)
        self.cmb_gender['values'] = ("select","Male","Female","Other")
        self.cmb_gender.place(x=370,y=390,width = 300,height=30)
        self.cmb_gender.current(0)

        password = Label(frame1,text = "PASSWORD",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=50,y=430)
        self.txt_password = Entry(frame1,font=("times new roman",15),bg = "white",show='*') 
        self.txt_password.place(x=50,y=460,width = 300,height=30) 

        confirm = Label(frame1,text = "CONFIRM PASSWORD",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=370,y=430)
        self.txt_confirm = Entry(frame1,font=("times new roman",15),show='*',bg = "white")
        self.txt_confirm.place(x=370,y=460,width=300,height=30)

        self.chk_var = IntVar()
        chk = Checkbutton(frame1,text = "I agree to the terms and conditions",font=('times new roman',20,'bold'),variable = self.chk_var,onvalue = 1,offvalue = 0,bg='white',fg='black').place(x=50,y=520)
        
        rbutton = Button(frame1,text="REGISTER",width=15,bg ="green",fg="white",font=('times new roman',15,'bold'),cursor = "hand2", command= self.registerData).place(x=50,y=580) 
        lbutton = Button(frame1,text="LOGIN",width=15,bg ="green",fg="white",font=('times new roman',15,'bold'),cursor = "hand2", command= self.login).place(x=300,y=580) 
        exit_button = Button(frame1,text="CANCEL",width=15,bg ="green",fg="white",font=('times new roman',15,'bold'),cursor = "hand2",command=root.quit).place(x=550,y=580)

    #-----------------------------Check if the data in the registration form is valid------------------------------------------------------------------------#        
    def registerData(self):

        if self.txt_fname.get() == " " or  self.txt_mail.get() == " " or self.txt_pnum.get() == " " or self.txt_address.get() == " " or self.txt_dob.get() == " " or self.cmb_gender.get() == "select" or self.txt_password.get() == " "  or self.txt_confirm.get() == " ":
            messagebox.showerror("Error","All fields are mandatory",parent=self.root)
        elif not re.search(regex,self.txt_mail.get()):
            messagebox.showerror("Error","Enter valid mail",parent = self.root)
        elif len(self.txt_password.get()) < 5:
            messagebox.showerror("Error",'Enter strong password',parent=self.root)
        elif self.txt_password.get() != self.txt_confirm.get():
            messagebox.showerror("Error","Enter correct password",parent = self.root)
        elif self.txt_fname.get().isalpha() == False :
            messagebox.showerror('Error','Enter valid name',parent=root)
        elif self.chk_var.get() == 0:
            messagebox.showerror("Error","Please agree our terms and conditions",parent=self.root)
        elif len(self.txt_pnum.get()) < 10 or self.txt_pnum.get().isnumeric() == False:
            messagebox.showerror("Error","Enter valid number",parent = self.root)
        else:

            try:
                con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')

                cur = con.cursor()
                cur.execute("select * from customer where mail=%s or pnum=%s",(self.txt_mail.get(),self.txt_pnum.get()))
                row = cur.fetchone()
                
                if row == None:
                    cur.execute("insert into customer(fname,lname,mail,pnum,address,age,gender,cpassword) values(%s,%s,%s,%s,%s,%s,%s,%s)",(self.txt_fname.get(),self.txt_lname.get(),self.txt_mail.get(),self.txt_pnum.get(),self.txt_address.get(),self.txt_dob.get(),self.cmb_gender.get(),self.txt_password.get()))
                    con.commit()
                    cur.execute("select cid from customer where mail='"+ self.txt_mail.get()+"'" )
                    rows = cur.fetchone()
                    con.close()
                    messagebox.showinfo("Success","Registered successfully\n Your id is "+ str(rows[0]),parent=self.root)
                else:
                    messagebox.showerror('Error','User already exists',parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Error due to : {str(es)}",parent = self.root)



    #---------------------------------------------Login window for admin and user-------------------------------------------------------------------#
    def login(self):
        
        global log
        log = Tk()
        
        self.log = log
        self.log.title("Login")
        self.log.geometry('500x300+550+350')
        self.log.minsize(500,300)
        self.log.maxsize(500,300)

        global frame2
        frame2 = Frame(self.log,bg='light blue')
        frame2.place(x=0,y=0,width=500,height=300)
        title2 = Label(frame2,text = "SELECT  YOUR  DESIGNATION",font=('times new roman',20,'bold'),padx = 30,pady=20,bg='light blue',fg='green').grid(row=1,column=1)
        t = Label(frame2,text="",bg='light blue').grid(row=2,column=1)
        t2 = Label(frame2,text="",bg='light blue').grid(row=3,column=1)
       
        user = Button(frame2,text = 'User Login',command=self.userLog,cursor = 'hand2',font= ("times new roman",15,'bold'),bg='white',fg='black').grid(row=4,column=1)
        t3 = Label(frame2,text="",bg='light blue').grid(row=5,column=1)
        t4 = Label(frame2,text="",bg='light blue').grid(row=6,column=1)
        admin = Button(frame2,text = 'Admin Login',command=self.adminLog,cursor='hand2',font= ("times new roman",15,'bold'),bg='white',fg='black').grid(row=7,column=1)
    

    #-------------------------------------------------------------User login window---------------------------------------------------------------#
    def userLog(self):
        global log    
        global frame2
        frame2.place_forget()
        
        frame3 = Frame(self.log,bg='white')
        frame3.place(x=0,y=0,width=500,height=350)

        self.l_Mail = Label(frame3,text = "EMAIL ADDRESS",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=20,y=0)
        self.ent_mail = Entry(frame3,font=('times new roman',15),bg='white',width=30)
        self.ent_mail.place(x=20,y=50)

            
        self.l_password = Label(frame3,text = "PASSWORD",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=20,y=100)
        self.ent_password = Entry(frame3,font=('times new roman',15),show='*',bg='white',width=30)
        self.ent_password.place(x=20,y=150)
        self.l_button = Button(frame3,text="LOGIN",width=25,bg ="green",fg="white",font=('times new roman',15,'bold'),command=self.checkuserLogin,cursor = "hand2").place(x=20,y=220)
        
    #-------------------------------------------------------------Admin login window--------------------------------------------------------------------#   
    def adminLog(self):
        global log    
        global frame2
        frame2.place_forget()
        
        frame4 = Frame(self.log,bg='white')
        frame4.place(x=0,y=0,width=500,height=350)

        self.al_Mail = Label(frame4,text = "EMAIL ADDRESS",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=20,y=0)
        self.aent_mail = Entry(frame4,font=('times new roman',15),bg='white',width=30)
        self.aent_mail.place(x=20,y=50)

            
        self.al_password = Label(frame4,text = "PASSWORD",font=('times new roman',15,'bold'),bg='white',fg='black').place(x=20,y=100)
        self.aent_password = Entry(frame4,font=('times new roman',15),bg='white',width=30,show='*')
        self.aent_password.place(x=20,y=150)
    
        self.al_button = Button(frame4,text="LOGIN",width=25,bg ="green",fg="white",font=('times new roman',15,'bold'),command=self.checkLogin,cursor = "hand2").place(x=20,y=220) 
       
        

    #--------------------------------Check if the data in the admin login form is valid------------------------------------------------------------------------#

    def checkLogin(self): 

        ###### admin features #######
        def admin_features():
            my_notebook = ttk.Notebook(root)
            my_notebook.pack(fill = 'both',expand=1)
            
            ttk.Style().configure('TNotebook.Tab',background='black',foreground = 'white',padding=[68,35],font=('times new roman',20,'bold'),width=22)
 ###==========================================================================================================================#################################
  
            viewtab = Frame(my_notebook,bg='light green')
            viewtab.grid(row=0,column=0)
            my_notebook.add(viewtab,text='View')

            def view():
                con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                cur = con.cursor()
                cur.execute('select accno,cid,acctype from cusAccount')
                rows = cur.fetchall()

                for row in rows:
                    
                    tree.insert('',END,values=row)
                con.close()


            con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
            cur = con.cursor()

            tree = ttk.Treeview(viewtab,column=('accno','cid','acctype'),show='headings')

            tree.column('#1',anchor=CENTER)
            tree.heading('#1',text='Account Number')

            tree.column('#2',anchor=CENTER)
            tree.heading('#2',text='Customer Id')

            tree.column('#3',anchor=CENTER)
            tree.heading('#3',text='Account Type')

            tree.place(x=400,y=200,width=1000,height=450)

            myButton = Button(viewtab,text='View',font=('Aerial',15,'bold'),command=view,width=10,bg='red',fg='white')
            myButton.place(x=600,y=520)
            con.close()

###==============================================================================================================================#######
            #---------------------------------------------add branch tab-----------------------------------------------------------------------#

            add_tab = Frame(my_notebook,bg='light green')
            add_tab.grid(row=0,column=1)
            my_notebook.add(add_tab,text='Home')

            #----------------------------------------check if details are filled in branch tab----------------------------------------#
            
            def add():
            
                if add_cmb.get() == '' or add_ent.get() == '' :
                    messagebox.showerror('Error','Enter all the fields',parent=root) 
                
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')

                        cur = con.cursor()
                        cur.execute("select bname from branch where bname='"+add_cmb.get()+"'" )
                        row = cur.fetchone()
                     
                        if row != None:
                            messagebox.showerror('Error','Branch name already exists',parent=root)
                        else:

                            cur.execute("insert into branch(bname,baddress) values(%s,%s)",(add_cmb.get(),add_ent.get()))
                            con.commit() 
                            con.close()   
                            messagebox.showinfo('Success','Branch added successfully',parent=root)
                               
                        
                    except Exception as es:
                        messagebox.showerror('Error',f"Error due to : {str(es)}",parent=root)
                    
            def delete():
                try:
                    if del_ent.get() == 'select' or del_add.get() == '':
                        messagebox.showerror('Error','Enter all the fields',parent=root)
                    else:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        id = del_add.get().casefold()
                        name  = del_ent.get().casefold()
                        cur.execute("select * from branch where bid=%s and bname=%s",(id,name))
                        row = cur.fetchone()
                        
                        if row == None:
                            messagebox.showerror('Error','Branch does not exist',parent=root)
                        else:
                            cur.execute('delete from branch where bid=%s and bname=%s',(id,name))
                            con.commit()
                            con.close()
                            messagebox.showinfo('Success','Branch deleted successfully',parent=root)
                except Exception as es:
                    messagebox.showerror('Error',f'Error due to : {str(es)}',parent =root)

            def updatebr():
                try:
                    if oldid.get() == '':
                        messagebox.showerror('Error','Enter branch id to be updated',parent=root) 
                    else:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select bid from branch where bid='"+oldid.get()+"'")
                        row=cur.fetchone()
                        if row == None:
                            messagebox.showerror('Error','Branch does not exists',parent=root)
                        else:
                            if new_ent.get()!='':
                                cur.execute('update branch set bname=%s where bid=%s',(new_ent.get(),oldid.get()))
                                con.commit()

                            if newcity_ent.get()!='':
                                cur.execute('update branch set baddress=%s where bid=%s',(newcity_ent.get(),oldid.get()))
                                con.commit()
                                con.close()
                        messagebox.showinfo('Success','Updated Successfuy',parent=root)

                except Exception as es:
                    messagebox.showerror('Error',f'Error due to: {str(es)}',parent=root)

            d = Label(add_tab,text='',bg='light green',width=60,height=10).grid(row=0,column=0)
            delbr = Label(add_tab,text='Enter Branch Name',font=('times new roman',20,'bold'),bg='light green',fg='black').grid(row=1,column=0)
            a7 = Label(add_tab,text='',bg='light green').grid(row=2,column=0)
            del_ent = Entry(add_tab,font=("times new roman",15),width=30)
        
            del_ent.grid(row=3,column=0)
            a = Label(add_tab,text='',bg='light green').grid(row=4,column=0)
            deladdress = Label(add_tab,text='Enter Branch Id',font=('times new roman',20,'bold'),bg='light green',height=2).grid(row=5,column=0)  
            r = Label(add_tab,text='',bg='light green').grid(row=6,column=0)
            del_add = Entry(add_tab,width=30,font=('times new roman',20))
            del_add.grid(row=7,column=0)
            n = Label(add_tab,text='',bg='light green').grid(row=8,column=0)

            delete_button = Button(add_tab,text='Delete Branch',font = ('times new roman',20,'bold'),width=20,bg='red',fg='white',cursor='hand2',command = delete)
            delete_button.grid(row=9,column=0)

            a7 = Label(add_tab,text='',width=70,bg='light green').grid(row=0,column=1)  
            depos = Label(add_tab,text='Enter Branch Name',font=('times new roman',20,'bold'),bg='light green',fg='black').grid(row=1,column=1)
            a8 = Label(add_tab,text='',bg='light green').grid(row=2,column=1)
            add_cmb = Entry(add_tab,font=("times new roman",15),width=30)
            
            add_cmb.grid(row=3,column=1)
            a = Label(add_tab,text='',bg='light green').grid(row=4,column=1)
            accadd = Label(add_tab,text='Enter Branch City',font=('times new roman',20,'bold'),bg='light green',height=2).grid(row=5,column=1) 
            r = Label(add_tab,text='',bg='light green').grid(row=6,column=1)
            add_ent = Entry(add_tab,width=30,font=('times new roman',20))
            add_ent.grid(row=7,column=1)
            n = Label(add_tab,text='',bg='light green').grid(row=8,column=1)

            add_button = Button(add_tab,text='Add Branch',font = ('times new roman',20,'bold'),width=20,bg='red',fg='white',cursor='hand2',command = add)
            add_button.grid(row=9,column=1)


            newbr = Label(add_tab,text='Enter New Branch Name',font=('times new roman',20,'bold'),bg='light green',fg='black').grid(row=1,column=3)
            a7 = Label(add_tab,text='',bg='light green').grid(row=2,column=3)
            new_ent = Entry(add_tab,font=("times new roman",15),width=30)
            new_ent.grid(row=3,column=3)
            a = Label(add_tab,text='',bg='light green').grid(row=4,column=3)
            newaddress = Label(add_tab,text='Enter Branch City',font=('times new roman',20,'bold'),bg='light green',height=2).grid(row=5,column=3)
            r = Label(add_tab,text='',bg='light green').grid(row=6,column=3)
            newcity_ent = Entry(add_tab,width=30,font=('times new roman',20))
            newcity_ent.grid(row=7,column=3)

            a = Label(add_tab,text='',bg='light green').grid(row=8,column=3)
            idl = Label(add_tab,text='Enter Branch Id To Update',font=('times new roman',20,'bold'),bg='light green',height=2).grid(row=9,column=3)
            r = Label(add_tab,text='',bg='light green').grid(row=10,column=3)
            oldid = Entry(add_tab,width=30,font=('times new roman',20))
            oldid.grid(row=11,column=3)
            n = Label(add_tab,text='',bg='light green').grid(row=12,column=1)

            update_button = Button(add_tab,text='Update Branch',font = ('times new roman',20,'bold'),width=20,bg='red',fg='white',cursor='hand2',command = updatebr)
            update_button.grid(row=13,column=3)

            
           #-------------------------------------------------delete account tab------------------------------------------------------------------#

            delete_tab = Frame(my_notebook,bg='light green')
            delete_tab.grid(row=0,column=2)
            my_notebook.add(delete_tab,text='Delete Account')

            #----------------------------------------check if account no. is empty in delete account tab----------------------------------------#
            
            def checkdeleteinfo():
                if deleteentry.get() == '' or deletetypeentry.get() == 'select':
                    messagebox.showerror('Error','Enter all the fields',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select accno,acctype from cusAccount where accno=%s and acctype=%s",(deleteentry.get(),deletetypeentry.get()))
                        row = cur.fetchone()
                        
                        if row == None:
                            messagebox.showerror('Error',f'Account does not exists',parent=root)
                        else:
                            cur.execute("delete from cusAccount where accno=%s and acctype=%s",(deleteentry.get(),deletetypeentry.get()))
                            con.commit()
                            con.close()
                            messagebox.showinfo('Success','Account deleted successfully',parent=root)


                    except Exception as es:
                        messagebox.showerror('Error',f'Error due to : {str(es)}',parent=root)
                

            empty3 = Label(delete_tab,text='',bg='light green',width=85,height=5).grid(row=0,column=0)

            deletelabel = Label(delete_tab,text='Enter Account Number',font=('times new roman',20,'bold'),bg='light green',height=6).grid(row=1,column=1)
            deleteentry = Entry(delete_tab,width=30,font=('times new roman',20))
            deleteentry.grid(row=2,column=1)

            emp = Label(delete_tab,text='',bg='light green').grid(row=3,column=1)

            deletetylabel = Label(delete_tab,text='Enter Account Type',font=('times new roman',20,'bold'),bg='light green',height=6).grid(row=4,column=1)
            deletetypeentry = ttk.Combobox(delete_tab,font=("times new roman",20),state='readonly',justify = CENTER,width=30)
            deletetypeentry['values'] = ("select","Savings account","Current account")
            deletetypeentry.grid(row=5,column=1)
            deletetypeentry.current(0)
            
            empty4 = Label(delete_tab,text='',bg='light green').grid(row=6,column=1)

            deletebutton = Button(delete_tab,text='Delete',width=20,fg='white',bg='red',cursor='hand2',font=('times new roman',20,'bold'),command=checkdeleteinfo).grid(row=7,column=1)
            
            #--------------------------------------------------update tab-----------------------------------------------------------------#

            update_tab = Frame(my_notebook,bg = 'light green')
            update_tab.grid(row=0,column=3)
            my_notebook.add(update_tab,text='Update Account')


            #----------------------------------------insert details of update tab to database---------------------------------------#
            
            def updateInfo():
                try:
                    if cident.get() == '':
                        messagebox.showerror('Error','Enter id',parent = root)

                    else :
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select cid from customer where cid='"+cident.get()+"'")
                        row= cur.fetchone()
                        if row == None:
                            messagebox.showerror('Error','Invalid User id',parent=root)
                        else:
                            if fnameent.get() != '':
                                cur.execute('update customer set fname=%s where cid=%s',(fnameent.get(),cident.get()))
                                con.commit()
                                
                            if lnameent.get() != '':
                                cur.execute('update customer set lname=%s where cid=%s',(lnameent.get(),cident.get()))
                                con.commit()
                                
                            if addent.get() != '':
                                cur.execute('update customer set address=%s where cid=%s',(addent.get(),cident.get()))
                                con.commit()
                                
                            if nument.get() != '':
                                cur.execute('update customer set pnum=%s where cid=%s',(nument.get(),cident.get()))
                                con.commit()
                                
                            if mailent.get() != '':
                                cur.execute('update customer set mail=%s where cid=%s',(mailent.get(),cident.get()))
                                con.commit()
                                                        
                            if passent.get() != '':
                                cur.execute('update customer set cpassword=%s where cid=%s',(passent.get(),cident.get()))
                                con.commit()
                            messagebox.showinfo('Success','Updated successfully',parent=root)
                            con.close()
                        
                except Exception as es:
                    messagebox.showerror('Error',f'Error due to +{str(es)}',parent=root)

            
            def checkuseracc():
                if caccount_ent.get() == '':
                    messagebox.showerror('Error','Enter account number',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select accno,acctype,balance from cusAccount where accno='"+caccount_ent.get()+"'")
                        row=cur.fetchone()
                        con.close()
                        if row == None:
                            messagebox.showerror('Error','User does not exists',parent=root)
                        else:
                            newroot3 = Tk()
                            newroot3.minsize(500,200)
                            newroot3.maxsize(500,200)
                            newroot3.geometry('500x200+650+590')
                            newroot3.title('Account Info')
                            for i in row:
                                lb = Listbox(newroot3,font=('aerial',15),bd=5,width=50,justify=CENTER)
                                lb.insert(1,'User account no. is '+ str(row[0]))
                                lb.insert(2,'User account type is '+ str(row[1]))
                                lb.insert(3,'User balance is '+ str(row[2]))
                                lb.pack()
                                break
                            newroot3.mainloop()
                    except Exception as es:
                        messagebox.showerror('Error',f'Error due to: {str(es)}',parent=root)


            empty5 = Label(update_tab,text='',bg='light green',width=40,height=2).grid(row=0,column=0)

            sanctionlabel = Label(update_tab,text='Enter Following Details To Update User Info',font=('Aerial',25,'bold'),height=2,bg='light green').grid(row=1,column=1)
            
            cidlabel = Label(update_tab,text='Enter current id of the user',font=('times new roman',20,'bold'),height=2,bg='light green').grid(row=3,column=1)
            cident = Entry(update_tab,font=('times new roman',15))
            cident.grid(row=3,column=2)


            fnamelabel = Label(update_tab,text='Enter New first name',font=('times new roman',20,'bold'),height=2,bg='light green').grid(row=4,column=1)
            fnameent = Entry(update_tab,font=('times new roman',15))
            fnameent.grid(row=4,column=2)


            lnamelabel = Label(update_tab,text='Enter New last name',font=('times new roman',20,'bold'),height=2,bg='light green').grid(row=5,column=1)
            lnameent = Entry(update_tab,font=('times new roman',15))
            lnameent.grid(row=5,column=2)

          
            addlabel = Label(update_tab,text='Enter New Address',font=('times new roman',20,'bold'),height=2,bg='light green').grid(row=6,column=1)
            addent = Entry(update_tab,font=('times new roman',15))
            addent.grid(row=6,column=2)


            numlabel = Label(update_tab,text='Enter New Number',font=('times new roman',20,'bold'),height=2,bg='light green').grid(row=7,column=1)
            nument = Entry(update_tab,font=('times new roman',15))
            nument.grid(row=7,column=2)


            maillabel = Label(update_tab,text='Enter New Mail',font=('times new roman',20,'bold'),height=2,bg='light green').grid(row=8,column=1)
            mailent = Entry(update_tab,font=('times new roman',15))
            mailent.grid(row=8,column=2)

            passlabel = Label(update_tab,text='Enter New Password',font=('times new roman',20,'bold'),height=2,bg='light green').grid(row=9,column=1)
            passent = Entry(update_tab,font=('times new roman',15))
            passent.grid(row=9,column=2)

            updatebutton = Button(update_tab,text='Update',width=20,fg='white',bg='red',cursor='hand2',font=('times new roman',20,'bold'),command=updateInfo).grid(row=10,column=1)
            ttk.Separator(update_tab).place(x=0,y=650,relwidth=1)

            n1 = Label(update_tab,text='',font=('Aerial',20,'bold'),bg='light green',height=2).grid(row=11,column=1)
            
            detail = Label(update_tab,text='View details',font=('Aerial',20,'bold'),height=2,bg='light green').grid(row=12,column=1)
            idno = Label(update_tab,text='Enter account number',font=('Aerial',20,'bold'),bg='light green',height=2).grid(row=13,column=0)
            caccount_ent = Entry(update_tab,font=('Aerial',20))
            caccount_ent.grid(row=13,column=1)
            
            
            infobutton = Button(update_tab,text='View Info',fg='white',width=20,bg='red',cursor='hand2',font=('times new roman',20,'bold'),command=checkuseracc).grid(row=13,column=2)
            
            #-----------------------------------------------------admin logout tab------------------------------------------------------------------------#

            logout_tab = Frame(my_notebook,bg='light green')
            logout_tab.grid(row=0,column=4)
            my_notebook.add(logout_tab,text='Logout')
 
            space1 = Label(logout_tab,text='',bg = 'light green',height=15).grid(row=0,column=1)
            image = ImageTk.PhotoImage(file='images/logout.jpg')
            imageplace = Label(logout_tab,image= image,width=1688,bg='light green')
            imageplace.image = image
            imageplace.grid(row=1,column=1)
            space2 = Label(logout_tab,text='',bg = 'light green',height=2).grid(row=2,column=1)
            logout_button = Button(logout_tab,text = 'LOGOUT',width=30,bg='green',fg='white',font=('times new roman',20,'italic'),cursor='hand2',command=my_notebook.pack_forget).grid(row=1,column=1)
        

        #--------------------------------check if mailid and password is correct in admin login ------------------------------------------------------#   

        if self.aent_mail.get() != 'nj@mail.com':
            messagebox.showerror('Error','Enter valid mail address',parent = self.log)
        elif self.aent_password.get() != '123':
            messagebox.showerror('Error','Enter correct password',parent=self.log)
        else: 
            log.destroy() 
            admin_features()

          
    #-----------------------------Check if the data in the user login form is valid------------------------------------------------------------------------#
   
    def checkuserLogin(self):

        ###### user features #######
        def features():
            my_note = ttk.Notebook(root)
            my_note.pack(fill='both',expand=1)
            
            ttk.Style().configure('TNotebook.Tab',background='black',foreground = 'white',padding=[34,30],font=('times new roman',20,'bold'),width=17)
 

            #-----------------------------------------------------home tab--------------------------------------------------------------#
            home_tab = Frame(my_note,bg='light blue')
            home_tab.pack(fill='both',expand=1)
            my_note.add(home_tab,text='Home')

            text1 = Label(home_tab,text='Welcome to NBM bank',font=('times new roman',40,'bold'),fg='black',bg='light blue').pack(pady=50)
            text2 = Label(home_tab,text='Contact Us',font=('times new roman',20,'bold'),fg='black',bg='light blue').pack(pady=10)
            text3 = Label(home_tab,text='Email : nbmbank@gmail.com',font=('times new roman',15,'bold'),fg='black',bg='light blue').pack(pady=10)
            text4 = Label(home_tab,text='Contact Number : +91 9964672811',font=('times new roman',15,'bold'),fg='black',bg='light blue').pack(pady=10)
            img = ImageTk.PhotoImage(file='images/bg.jpg')
            imgplace = Label(home_tab,image=img)
            imgplace.img=img
            imgplace.pack()

            
            #--------------------------------------------------create account tab-----------------------------------------------------------------#


            #-----------------------------------check if data in the create account form is valid-----------------------------------------------------------#

       
                      
            create_acc = Frame(my_note,bg ='light blue')
            create_acc.pack()
            my_note.add(create_acc,text='Create Account')


            def checkfeatures():
            
                if depo_ent.get() == '' or id_ent.get() == '' or acctype_cmb.get() == 'select' or accbranch_cmb.get() == 'select':
                    messagebox.showerror('Error','Enter all the fields',parent=root) 
                elif  depo_ent.get().isnumeric() == False or int(depo_ent.get()) < 100:
                    messagebox.showerror('Error','Deposit minimum of Rs.100',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')

                        cur = con.cursor()
                        cur.execute("select cid from customer where cid='"+id_ent.get()+"'" )
                        row = cur.fetchone()
                     
                        if row == None:
                            messagebox.showerror('Error','User does not exists',parent=root)
                        else:
                            branch = accbranch_cmb.get().casefold()
                            cur.execute("select bid from branch where bname='"+branch+"'")
                            br = str(cur.fetchone())
                            cur.execute("select acctype,cid,bid from cusAccount where acctype=%s and cid=%s and bid=%s",(acctype_cmb.get(),id_ent.get(),br[1]))
                            rows= cur.fetchone()
                        
                        
                            if rows != None:
                                
                                messagebox.showerror('Error','Account already exits',parent=root)
        
                            else:
                                
                                cur.execute("insert into cusAccount(cid,acctype,balance,bid) values(%s,%s,%s,%s)",(id_ent.get(),acctype_cmb.get(),depo_ent.get(),br[1]))
                                con.commit()

                                cur.execute("select accno from cusAccount where acctype=%s and cid=%s",(acctype_cmb.get(),id_ent.get()))
                                r= cur.fetchone()  
                        
                                con.close()   
                                messagebox.showinfo('Success','Account created successfully\nYour account no. is '+str(r[0]),parent=root)
                                submit_button.grid_forget()   
                            
                    except Exception as es:
                        messagebox.showerror('Error',f"Error due to : {str(es)}",parent=root)
    
            

            dr = Label(create_acc,text='',bg='light blue',width=50,height=10).grid(row=0,column=0)
               
            depos = Label(create_acc,text='Deposit',font=('times new roman',20,'bold'),bg='light blue',fg='black').grid(row=1,column=1)
            a7 = Label(create_acc,text='',bg='light blue').grid(row=2,column=2)
            depo_ent = Entry(create_acc,width=30,font=('times new roman',20))
            depo_ent.grid(row=1,column=3)

            a7 = Label(create_acc,text='',bg='light blue').grid(row=3,column=2)

            
            acctype = Label(create_acc,text='Account type',font=('times new roman',20,'bold'),bg='light blue',height=2).grid(row=4,column=1)
            
            acctype_cmb = ttk.Combobox(create_acc,font=("times new roman",15),state='readonly',justify = CENTER,width=30)
            acctype_cmb['values'] = ("select","Savings account","Current account")
            acctype_cmb.grid(row=4,column=3)
            acctype_cmb.current(0)

            r6 = Label(create_acc,text='',bg='light blue').grid(row=5,column=0)
           
            idlabel = Label(create_acc,text='Enter Your id',font=('times new roman',20,'bold'),bg='light blue',height=2).grid(row=6,column=1)
            id_ent = Entry(create_acc,width=30,font=('times new roman',20))
            id_ent.grid(row=6,column=3)


            a = Label(create_acc,text='',bg='light blue').grid(row=7,column=0)

            accbranch = Label(create_acc,text='Select Branch',font=('times new roman',20,'bold'),bg='light blue',height=2).grid(row=8,column=1)
            accbranch_cmb = ttk.Combobox(create_acc,font=("times new roman",15),state='readonly',justify = CENTER,width=30)
            accbranch_cmb['values'] = ("select","NBM","BMC","NJ")
            accbranch_cmb.grid(row=8,column=3)
            accbranch_cmb.current(0)

            r8 = Label(create_acc,text='',bg='light blue').grid(row=9,column=0)

            submit_button = Button(create_acc,text='Submit',font = ('times new roman',20,'bold'),width=20,bg='green',fg='white',cursor='hand2',command = checkfeatures)
            submit_button.grid(row=10,column=1)

            #------------------------------------------------transactions tab---------------------------------------------------------#
            transfer_tab = Frame(my_note,bg='light blue')
            transfer_tab.pack()
            my_note.add(transfer_tab,text='Transactions')
            
            

            #----------------------------------------check if amount is filled in withdraw tab----------------------------------------#
            
            def checkWithAmount():
                if enter_entry.get() == '':
                    messagebox.showerror('Error','Enter account number',parent=root)
                elif enter_amentry.get() == '' or enter_amentry.get().isnumeric() == False:
                    messagebox.showerror('Error','Enter amount in rupees',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select accno from cusAccount where accno ='"+enter_entry.get()+"'")
                        row = cur.fetchone()
                        if row == None:
                            messagebox.showerror('Error','Account does not exists',parent=root)
                        else:
                            cur.execute("select balance from cusAccount where accno='"+enter_entry.get()+"'")
                            row = cur.fetchone()
                            res = decimal.Decimal(row[0])
                            amt = decimal.Decimal(enter_amentry.get())
                            bal = res-amt
                            result = res.compare(amt)
                            
                            if result == -1 or bal <= 100:
                                messagebox.showerror('Error','Your account balance is low',parent=root)
                            else:
                                bal = res-amt
                                cur.execute('update cusAccount set balance=%s where accno=%s',(bal,enter_entry.get()))
                                con.commit()
                                con.close()
                                messagebox.showinfo('Success','Amount withdrawn successfully\nBalance left: '+str(bal),parent=root)
                  
                    except Exception as es:
                        messagebox.showerror('Error',f'Error due to: {str(es)}',parent=root)

            #----------------------------------------check if amount is filled in deposit tab----------------------------------------#
            
            def checkDepoAmount():
                if enter_entry.get() == '':
                    messagebox.showerror('Error','Enter account number',parent=root)
                elif enter_amount.get() == '' or enter_amount.get().isnumeric() == False:
                    messagebox.showerror('Error','Enter amount in rupees',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select accno from cusAccount where accno ='"+enter_entry.get()+"'")
                        row = cur.fetchone()
                        if row == None:
                            messagebox.showerror('Error','Account does not exists',parent=root)
                        else:
                            cur.execute("select balance from cusAccount where accno='"+enter_entry.get()+"'")
                            row = cur.fetchone()
                            depores = decimal.Decimal(row[0])
                            amount = decimal.Decimal(enter_amount.get())
                            
                            balanc = depores+amount
                            cur.execute('update cusAccount set balance=%s where accno=%s',(balanc,enter_entry.get()))
                            con.commit()
                            con.close()
                            messagebox.showinfo('Success','Amount deposited successfully\nBalance left: '+str(balanc),parent=root)
                  
                    except Exception as es:
                        messagebox.showerror('Error',f'Error due to: {str(es)}',parent=root)
                
            ##############################################################################################################################
    
            r9 = Label(transfer_tab,text='',bg='light blue',height=1,width=80).grid(row=0,column=0)
            r14 = Label(transfer_tab,text='',bg='light blue',height=6).grid(row=7,column=1)

                        
            enter = Label(transfer_tab,text='Enter Account Number',font=('times new roman',20,'bold'),height=2,bg='light blue').grid(row=2,column=1) 

            r10 = Label(transfer_tab,text='',bg='light blue').grid(row=3,column=1)

            enter_entry = Entry(transfer_tab,font=('times new roman',20),width=30)
            enter_entry.grid(row = 4,column=1)

            
            r10 = Label(transfer_tab,text='',bg='light blue').grid(row=7,column=1)

            withdraw_label = Label(transfer_tab,text='Withdraw Amount',fg='green',bg='light blue',font=('times new roman',27,'bold')).grid(row=8,column=1)
            r11 = Label(transfer_tab,text='',bg='light blue',height=2,width=50).grid(row =9,column=0)
            enter_am = Label(transfer_tab,text='Enter Amount',font=('times new roman',20,'bold'),bg='light blue').grid(row=10,column=1) 

            r12 = Label(transfer_tab,text='',bg='light blue').grid(row=11,column=1)

            enter_amentry = Entry(transfer_tab,font=('times new roman',20),width=30)
            enter_amentry.grid(row = 12,column=1)
 
            r13 = Label(transfer_tab,text='',bg='light blue').grid(row=13,column=1)

            withdraw_button = Button(transfer_tab,text='Submit',font = ('times new roman',20,'bold'),width=20,bg='green',fg='white',cursor='hand2',command=checkWithAmount)
            withdraw_button.grid(row=14,column=1)

            r15 = Label(transfer_tab,text='',bg='light blue',height=6).grid(row=15,column=1)

            deposit_label = Label(transfer_tab,text='Deposit Amount',fg='green',bg='light blue',font=('times new roman',27,'bold')).grid(row=16,column=1)
            r16 = Label(transfer_tab,text='',bg='light blue',height=2,width=50).grid(row =17,column=0)
            enter_amo = Label(transfer_tab,text='Enter Amount',font=('times new roman',20,'bold'),bg='light blue').grid(row=18,column=1) 

            r17 = Label(transfer_tab,text='',bg='light blue').grid(row=19,column=1)

            enter_amount = Entry(transfer_tab,font=('times new roman',20),width=30)
            enter_amount.grid(row = 20,column=1)
 
            r18 = Label(transfer_tab,text='',bg='light blue').grid(row=21,column=1)

            deposit_button = Button(transfer_tab,text='Submit',font = ('times new roman',20,'bold'),width=20,bg='green',fg='white',cursor='hand2',command=checkDepoAmount)
            deposit_button.grid(row=22,column=1)


          
            #--------------------------------------------------loan tab-----------------------------------------------------------------------#
            apply_loan = Frame(my_note,bg='light blue')
            apply_loan.pack()
            my_note.add(apply_loan,text='Apply For Loans')

            #----------------------------------------check if all details are filled in loan tab----------------------------------------#
            
            def checkLoanInfo():
                if loan_amount.get() == ''or loan_amount.get().isnumeric == False or period.get() == '' or accent.get() == '':
                    messagebox.showerror('Error','Enter all details correctly',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select accno from cusAccount where accno='"+accent.get()+"'")
                        row = cur.fetchone()
                        if row == None:
                            messagebox.showerror('Error','Account does not exist',parent=root)
                        else:
                            cur.execute('select bid from cusAccount where accno=%s',(accent.get(),))
                            row=cur.fetchone()
                            cur.execute('insert into loan(bid,accno,amount,period) values(%s,%s,%s,%s)',(str(row[0]),accent.get(),loan_amount.get(),period.get()))
                            con.commit()
                            con.close()
                            messagebox.showinfo('Success','Query processed',parent=root)
                    except Exception as es:
                        messagebox.showerror('Error',f"Error due to :+{str(es)}",parent=root)
            
            def repayloan():
                if ramount.get()=='' or ramount.get().isnumeric()==False:
                    messagebox.showerror('Error','Enter amount in rupees',parent=root)
                if raccent.get() == '':
                    messagebox.showerror('Error','Enter account number',parent=root)

                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute('select accno from loan where accno=%s',(raccent.get(),))
                        row = cur.fetchone()
                        if row == None:
                            messagebox.showerror('Error','user does not exists',parent=root)
                        else:
                            cur.execute('select amount from loan where accno=%s',(raccent.get(),))
                            row= cur.fetchone()
                            curamt = row[0]
                            pay = decimal.Decimal(ramount.get())
                            total = curamt - pay
                            cur.execute('update loan set amount=%s where accno=%s',(total,raccent.get()))
                            con.commit()
                            cur.execute('select amount from loan where accno=%s',(raccent.get(),))
                            row=cur.fetchone() 
                            messagebox.showinfo('Success',f'Amount to be paid is {str(row[0])}',parent=root)
                       
                        con.close()

                    except Exception as es:
                        messagebox.showerror('Error',f'Error due to : {str(es)}',parent=root)
            ###########################################################################################################################

            r19 = Label(apply_loan,text='',bg='light blue',height=2,width=70).grid(row=0,column=0)
            

            loanlabel = Label(apply_loan,text='Enter amount',bg='light blue',height=2,font=('times new roman',27,'bold')).grid(row=8,column=1)
            r21 = Label(apply_loan,text='',bg='light blue',height=2).grid(row=9,column=1)
            loan_amount = Entry(apply_loan,font=('times new roman',20),width=30)
            loan_amount.grid(row = 9,column=1)  

            c18 = Label(apply_loan,text='',bg='light blue',height = 2).grid(row=10,column=1)
            timelabel = Label(apply_loan,text='Enter period in days or months or years',bg='light blue',font=('times new roman',27,'bold')).grid(row=11,column=1) 
            c21 = Label(apply_loan,text='',bg='light blue',height=1).grid(row=12,column=1)
            period = Entry(apply_loan,font=('times new roman',20))
            period.grid(row = 13,column=1)  

            c19 = Label(apply_loan,text='',bg='light blue',height = 2).grid(row=14,column=1)
            acclabel = Label(apply_loan,text='Enter your account number',bg='light blue',font=('times new roman',27,'bold')).grid(row=15,column=1) 
            c22 = Label(apply_loan,text='',bg='light blue',height=1).grid(row=16,column=1)
            accent = Entry(apply_loan,font=('times new roman',20))
            accent.grid(row = 17,column=1)  


            c20 = Label(apply_loan,text='',bg='light blue',height = 2).grid(row=18,column=1)
            apply_button = Button(apply_loan,text='Submit',command=checkLoanInfo,font = ('times new roman',20,'bold'),width=20,bg='green',fg='white',cursor='hand2')
            apply_button.grid(row=19,column=1)

            ttk.Separator(apply_loan).place(x=0,y=620,relwidth=1)
            c20 = Label(apply_loan,text='',bg='light blue',height = 6).grid(row=20,column=1)
            c21 = Label(apply_loan,text='Repay Loan Amount',bg='light blue',fg='green',font=('Times New Roman',30,'bold')).grid(row=21,column=1)
           
            c20 = Label(apply_loan,text='',bg='light blue',height = 2).grid(row=22,column=1)
            repaylabel = Label(apply_loan,text='Enter amount',bg='light blue',font=('times new roman',27,'bold')).grid(row=23,column=0) 
            ramount = Entry(apply_loan,font=('times new roman',20))
            ramount.grid(row = 24,column=0) 

            c20 = Label(apply_loan,text='',bg='light blue',height = 2).grid(row=22,column=1)
            repaylab = Label(apply_loan,text='Enter account number',bg='light blue',font=('times new roman',27,'bold')).grid(row=23,column=1) 
            raccent = Entry(apply_loan,font=('times new roman',20))
            raccent.grid(row = 24,column=1) 

            rbutton = Button(apply_loan,text='Submit',fg='white',bg='green',font=('Time New Roman',20),width=20,cursor='hand2',command=repayloan).grid(row=23,column=3)

            
            #------------------------------------------------view account info tab-------------------------------------------------------------#

            info_tab = Frame(my_note,bg ='light blue')
            info_tab.pack()
            my_note.add(info_tab,text=' Account Info')

            def view():
                if cid.get() == '' or caccount_ent.get() == '':
                    messagebox.showerror('Error','Enter all the fields',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select * from customer where cid = %s",(cid.get(),))
                        row=cur.fetchone()
                        con.close()
                        if row == None:
                            messagebox.showerror('Error','User does not exists',parent=root)
                        else:
                            newroot = Tk()
                            newroot.minsize(500,300)
                            newroot.maxsize(500,300)
                            newroot.geometry('500x300+650+590')
                            newroot.title('Personal Info')
                            for i in row:
                            
                                lb = Listbox(newroot,font=('aerial',15),bd=5,width=50,justify=CENTER)
                                lb.insert(1,'Your id is '+ str(row[0]))
                                lb.insert(3,'Your fname is '+ str(row[1]))
                                lb.insert(4,'Your lname is '+ str(row[2]))
                                lb.insert(5,'Your mail is '+ str(row[3]))
                                lb.insert(6,'Your number is '+ str(row[4]))
                                lb.insert(7,'Your address is '+ str(row[5]))
                                lb.insert(8,'Your dob is '+ str(row[6]))
                                lb.insert(9,'Your gender is '+ str(row[7]))
                                lb.insert(10,'Your password is '+ str(row[8]))
                                lb.pack()
                                break
                            newroot.mainloop()

                    except Exception as es:
                        messagebox.showerror('Error',f'Error due to: {str(es)}',parent=root)

            def accinfo():
                if cid.get() == '' or caccount_ent.get() == '':
                    messagebox.showerror('Error','Enter all the fields',parent=root)
                else:
                    try:
                        con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')
                        cur = con.cursor()
                        cur.execute("select accno,acctype,balance from cusAccount where accno='"+caccount_ent.get()+"'")
                        row=cur.fetchone()
                        if row == None:
                            messagebox.showerror('Error','User does not exists',parent=root)
                        else:
                            newroot2 = Tk()
                            newroot2.minsize(500,300)
                            newroot2.maxsize(500,300)
                            newroot2.geometry('500x300+650+590')
                            newroot2.title('Account Info')
                            for i in row:
                                lb = Listbox(newroot2,font=('aerial',15),bd=5,width=50,justify=CENTER)
                                lb.insert(1,'Your account no. is '+ str(row[0]))
                                lb.insert(2,'Your account type is '+ str(row[1]))
                                lb.insert(3,'Your balance is '+ str(row[2]))
                                lb.pack()
                                break
                            newroot2.mainloop()
                    except Exception as es:
                        messagebox.showerror('Error',f'Error due to: {str(es)}',parent=root)


            v19 = Label(info_tab,text='',bg='light blue',height=2,width=80).grid(row=0,column=0)
             
            cidlabel = Label(info_tab,text='Enter Your id',bg='light blue',height=2,font=('times new roman',27,'bold')).grid(row=8,column=1)
            v20 = Label(info_tab,text='',bg='light blue',height=2).grid(row=9,column=1)
            cid = Entry(info_tab,font=('times new roman',20),width=30)
            cid.grid(row = 9,column=1)  

            v21 = Label(info_tab,text='',bg='light blue',height = 2).grid(row=10,column=1)
            caccountLabel = Label(info_tab,text='Enter Your accno',bg='light blue',font=('times new roman',27,'bold')).grid(row=11,column=1) 
            v21 = Label(info_tab,text='',bg='light blue',height=1).grid(row=12,column=1)
            caccount_ent = Entry(info_tab,font=('times new roman',20))
            caccount_ent.grid(row = 13,column=1)  
            
            v22 = Label(info_tab,text='',bg='light blue',height = 2).grid(row=14,column=1)
            pinfo_button = Button(info_tab,text='View personal info',bg='green',fg='white',font=('times new roman',27,'bold'),cursor='hand2',command=view).grid(row=15,column=1) 
            v23 = Label(info_tab,text='',bg='light blue',height = 2).grid(row=16,column=1)
            accinfo_button = Button(info_tab,text='View account info',bg='green',fg='white',font=('times new roman',27,'bold'),cursor='hand2',command=accinfo).grid(row=17,column=1) 
            
            

            #-------------------------------------------------logout tab--------------------------------------------------------------------------#


            userlogout = Frame(my_note,bg = 'light blue')
            userlogout.pack()
            my_note.add(userlogout,text='Logout')
 
            space1 = Label(userlogout,text='',bg = 'light blue',height=15).grid(row=0,column=1)
            image = ImageTk.PhotoImage(file='images/logout.jpg')
            imageplace = Label(userlogout,image= image,width=1688,bg='light blue')
            imageplace.image = image
            imageplace.grid(row=1,column=1)
            space2 = Label(userlogout,text='',bg = 'light blue',height=2).grid(row=2,column=1)
            logout_button = Button(userlogout,text = 'LOGOUT',width=30,bg='green',fg='white',font=('times new roman',20,'italic'),cursor='hand2',command= my_note.pack_forget).grid(row=1,column=1)
        
         
       
        #--------------------------------check if mailid and password is correct in user login ---------------------------------------------------------# 

        if self.ent_mail.get() == '' or self.ent_password.get() == '':
            messagebox.showerror('Error','Enter mail address',parent = self.log)

        else: 
            try:
                con = mysql.connector.connect(host='localhost',user='root',password='',database='bankDB')

                cur=con.cursor()
                cur.execute('select * from customer where mail=%s and cpassword=%s',(self.ent_mail.get(),self.ent_password.get()))
                row = cur.fetchone()
                if row != None:
                    con.close()
                    log.destroy()
                    features()    
                else:
                    messagebox.showerror('Error','Enter valid Email and password',parent=self.log)
                    
            except Exception as es:
                messagebox.showerror('Error',f'Error due to : {str(es)}',parent=self.root)     
      
        


    
                  

register(root)

root.mainloop()