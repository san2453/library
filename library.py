import pymysql as x
import getpass as passw
import tabulate as t
import numpy as num
import datetime as time




print("")
print("""______________________________________________________________________________________________________________________________________""")
print('                                                                 (LIBRARY)                                             ')
print ('                                                        ( ART INTEGRATED PROJECT )')
print("""______________________________________________________________________________________________________________________________________""")
print(" ")


#functions used in the code
#ADMIN FUNCTIONS
def view_admin():
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    print("=====================================")
    cur=db.cursor()
    wholeA=cur.execute("select * from admin;")
    wholedataA=cur.fetchall()
    #print(wholedataA)
    print(t.tabulate(wholedataA, headers=['USER', 'BOOK NAME', 'ID', 'DATE OF ISSUE', 'DATE OF RETURN', 'FINE', 'COPIES'], tablefmt='grid'))
    cur.close()
    db.close()
    admin_menu()

def add_lib():
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    cur=db.cursor()
    c=int(input("""hello admin, would you like to add a new book or update an existing book?
1) add a new book
2) update an existing book
enter choice: """))
    if c == 1:
        addn= input("please enter the name of the book to be added: ")
        addid= input("please enter the ID of the book: ")
        fetchid=cur.execute("select ID from lib;")
        tup=cur.fetchall()
        #print(tup)
        ids = [] 
        temp = set() 
        for inner in tup: 
                for ID in inner: 
                    if not ID in temp: 
                        temp.add(ID) 
                        ids.append(ID)
        #print(ids)
        if addid in ids:
            print('the id is already taken, try again')
            add_lib()
        elif addid not in ids:
            pass
        addau = input("please enter the author of the book: ")
        addcopy= int(input("please enter the number of copies: "))
        
        cur.execute(f"insert into {tablen} values('{addid}','{addn}','{addau}',{addcopy});")
        db.commit()
        cur.close()
        db.close()
        print('book added')
        admin_menu()
        
    elif c == 2:
        updn= input("please enter the name of the book to be updated: ")
        upd= int(input("please enter the number of copies: "))
        try:
            cur.execute(f"update {tablen} set copies= {upd} where book like '%{updn}%';")
            db.commit()
            cur.close()
            db.close()
            print("record updated")
        except Exception as e:
            print(e)
        admin_menu()
    else:
        print("invalid response, please try again")
        add_lib()



def admin_lib():
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    print("=====================================")
    cur=db.cursor()
    lib=cur.execute("select * from {};".format(tablen))
    libdata=cur.fetchall()
    #print(libdata)
    print(t.tabulate(libdata, headers=['ID', 'BOOK NAME', 'AUTHOR', 'COPIES'], tablefmt='grid'))
    cur.close()
    db.close()
    admin_menu()



#USER FUNCTIONS AND PORTALS
    
def fine():
    try:
        db=x.connect(host="localhost",user="root",passwd=h,db=data)
        cur=db.cursor()
        m=cur.execute(f"select * from admin where user = '{user}' ")
        k=cur.fetchone()
        #print(today)
        #print(k[4])
        if today>k[4]:
            fine=(today-k[4]).days*20
            fine_update=cur.execute(f"update admin set fine = {fine} where user = '{user}'")
            db.commit()
            cur.close()
            db.close()
    
        else:
            pass
    except Exception as e:
        #print(e)
        pass
def rec():
    global users
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    
    cur=db.cursor()
    users=[]
    ab=cur.execute('select * from admin')
    rec=cur.fetchall()
    db.commit()
    cur.close()
    db.close()
    for row in rec:
        users.append(row[0])
    #print(users, rec)
        

def Issue():
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    cur=db.cursor()
    issue= input("which book do you wish to issue? enter ID: ")
    try:
        get=cur.execute(f"select * from {tablen} where ID = '{issue}'")
        f=cur.fetchone()
        if f[3]==0:
            print('the book you are trying to issue seems to be unavailable at the moment, try again when it is in stock')
        elif f[3]>0:
            rec()
            if user in users:
                print('it seems like you have already issued a book, return the previous book to issue another')
            elif user not in users:
                admin_add=cur.execute(f"insert into admin(user, book,ID,date_of_issue,date_of_return) values('{user}','{f[1]}','{f[0]}','{today}','{deadline}')")
                update=cur.execute(f"update {tablen} set copies = copies - 1 where ID = '{issue}'")
                print(f"""the book {f[1]} has been issued to you with deadline {deadline}. Please note that a fine of 20rs per day will be added for delay after the deadline""")
                db.commit()
                cur.close()
                db.close()
    except Exception as e:
        print('the id that you have entered is incorrect, try rechecking ID by selecting search a book or display all available books')


def Return():
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    cur=db.cursor()
    ac=cur.execute(f"select * from admin where user = '{user}'")
    rec=cur.fetchone()
    if rec == None:
        print("you have no book issued at the moment")
    elif rec[5]==0:
        ret=input(f"you currently have issued book {rec[1]} with ID {rec[2]} having a deadline of {rec[4]}, would you like to return it? y or n: ")
        if ret == 'y' or ret == 'Y':
            update=cur.execute(f"update {tablen} set copies = copies + 1 where ID = '{rec[2]}'")
            admin_update=cur.execute(f"delete from admin where user = '{user}'")
            print(f"the book {rec[1]} has been returned successfully")
            db.commit()
            cur.close()
            db.close()
        elif ret == 'n' or ret == 'N':
            pass
        else:
            print("invalid choice, please select again")
            Return()
    elif rec[5]>0:
        ret=input(f"you currently have issued book {rec[1]} with ID {rec[2]} having a deadline of {rec[4]} and a fine of {rec[5]}rs due to late return, would you like to return it? y or n: ")
        if ret == 'y' or ret == 'Y':
            update=cur.execute(f"update {tablen} set copies = copies + 1 where ID = '{rec[2]}'")
            admin_update=cur.execute(f"delete from admin where user = '{user}'")
            print(f"the book {rec[1]} has been returned successfully")
            db.commit()
            cur.close()
            db.close()
            
        elif ret == 'n' or ret == 'N':
            pass
        else:
            print("invalid choice, please select again")
            Return()
    
def Search():
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    cur=db.cursor()
    rd=input("Enter name of book: ")
    aa=cur.execute(f"select * from {tablen} where book like '%{rd}%'")
    inddata=cur.fetchall()
    if aa>0:
        print(t.tabulate(inddata, headers=['ID', 'BOOK NAME', 'AUTHOR', 'COPIES', 'STATUS'], tablefmt='grid'))
    elif aa==0:
        print()
        print("book not available")
    db.commit()
    cur.close()
    db.close()


def View():
    db=x.connect(host="localhost",user="root",passwd=h,db=data)
    print("=====================================")
    cur=db.cursor()
    whole=cur.execute("select * from {} where copies > 0;".format(tablen))
    wholedata=cur.fetchall()
    #print(wholedata)
    print(t.tabulate(wholedata, headers=['ID', 'BOOK NAME', 'AUTHOR', 'COPIES'], tablefmt='grid'))
    cur.close()
    db.close()
    User_Menu()



    
def User_Menu():
    while True:
        print()
        print(f"\t\t\t Welcome {user}, please select an option below")
        print("\t\t\t 1. Issue a book")
        print("\t\t\t 2. Return a book")
        print("\t\t\t 3. Search for a book")
        print("\t\t\t 4. View all the available books")
        print("\t\t\t 5. Exit")
        print()
        
        b=int( input("Enter Choice: ") )
        print()

        if b == 1:
            Issue()

        elif b == 2:
            Return()
            
            #User_menu()

        elif b == 3:
            Search()
            User_Menu()

        elif b == 4:
            View()

        elif b==5:
            Portals()

        else:
            print("invalid option, please try again")


def Portals():
    global deadline
    global today
    global pass_admin
    today=time.date.today()
    delta=time.timedelta(10)
    deadline=today+delta
    
    global user
    while True:
        print("============================")
        print("LIBRARY DATABASE SYSTEM")
        print("============================")
        print("Welcome, please select portal")
        print("1. Admin")
        print("2. User")
        print("3. exit")
        print()
        
        c=int( input("Enter Choice: ") )
        print()
        
        if c == 1:
            pass_admin= passw.getpass(prompt="enter your password for admin: ")
            admin_menu()
            break

        elif c == 2:
            usr=input("welcome user, please enter your name ")
            user=usr.lower()
            fine()
            User_Menu()
            break
        elif c==3:
            exit()

        else:
            print("invalid input, please try again")


        
#code
#1st loop for seeing if the database exists or not
while True:
    h=passw.getpass(prompt="enter your sql password: ")
    val=input("does your database exist? y or n: ") #i have to add a generate table right here
    if val == 'y' or val == 'Y':
        data=input("enter an existing database name: ")
        ex=True
        try:
            db=x.connect(host="localhost", user="root",passwd=h,db=data)
            print("Connected Successfully!\n")
            break
        except Exception as e:
            print("there is an error, try checking the password or database name", e)
            ex=False
    elif val == 'n' or val== 'N':
        try:
            db=x.connect(host="localhost", user="root",passwd=h)
            cur=db.cursor()
            cur.execute('create database library')
            data='library'
            print("A database named library has been created")
            ex=True
            break
        except Exception as e:
            print("there is some error, try rechecking the password")
            print(e)
            ex=False
    else:
        print("invalid option, please try again")

#2nd loop for seeing if there are entries or not, only gets executed if 1st loop works        
while True:        
    tab=input("does your table exist with records? y or n: ")
    if tab== 'n' or tab == 'N':
            try:
                tablen= input("enter table name: ")
                if tablen == 'admin' or tablen == 'Admin':
                    print("you are not allowed to use that name as table name, try some other name")
                else:
                    db=x.connect(host="localhost",user="root", passwd=h,db=data)
                    cur=db.cursor()
                    #table create
                    cur.execute("create table {}(ID char(10) primary key, book char(50), author char(40), copies int(6));".format(tablen))
                    #recs add
                    cur.execute("insert into {} values('A0245','Adventures of huckleberry finn','mark twain', 6);".format(tablen))
                    cur.execute("insert into {} values('A0247','inferno','dan brown',3);".format(tablen))
                    cur.execute("insert into {} values('A0265','Da vinci code','dan brown',4);".format(tablen))
                    cur.execute("insert into {} values('A0227','percy jackson: sea of monsters','rick riordan',3);".format(tablen))
                    cur.execute("insert into {} values('A0527','The Great Gatsby','F scott fitzgerald',7);".format(tablen))
                    cur.execute("insert into {} values('A0286','to kill a mockingbird','harper lee',3);".format(tablen))
                    cur.execute("insert into {} values('A0341','jane eyre','charlotte bronte',2);".format(tablen))
                    cur.execute("insert into {} values('A0217','percy jackson: the last olympian','rick riordan',0);".format(tablen))
                    cur.execute("insert into {} values('A0677','the hunger games: catching fire','suzanne collins',3);".format(tablen))
                    db.commit()
                    cur.close()
                    db.close()
                    print(f"table named {tablen} created with records")
                    ex = True
                    break
            except Exception as e:
                print("there is some error", e)
                ex=False
    elif tab=='y' or tab == 'Y':
            tablen=input('enter table name: ')
            ex=True
            break
    else:
        print("invalid option, please try again")

        
#admin database
try:
    db=x.connect(host="localhost", user="root",passwd=h, db=data)
    cur=db.cursor()
    print('admin database connected')
except Exception as e:
    print("error in connection of table admin", e)
try:
    cur.execute("create table admin (user char(30), book char(50), ID char(10) , date_of_issue date, date_of_return date, fine int(10) default 0, copies int (3) default 1 );")
    print("admin table created")
except Exception as e:
    print("admin table exists")
    pass


#ADMIN

def admin_menu():
    
    if pass_admin == h:
        print()
        print(f"\t\t\t Welcome admin, please select an option below")
        print("\t\t\t 1. view the admin database")
        print("\t\t\t 2. add a book")
        print("\t\t\t 3. view the books in library")
        print("\t\t\t 4. search for a book")
        print("\t\t\t 5. Exit")
        print()

        ch= int(input("enter choice: "))
        if ch == 1:
            view_admin()
            
        if ch == 2:
            add_lib()
            
        if ch == 3:
            admin_lib()
            
        if ch == 4:
            Search()
            admin_menu()
            
        if ch == 5:
            Portals()
    elif pass_admin != h:
        print("access denied")
        Portals()
    
Portals()



