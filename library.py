import pymysql as x
import getpass as passw
import tabulate as t
import numpy as num



print("")
print("""______________________________________________________________________________________________________________________________________""")
print('                                                                 (LIBRARY)                                             ')
print ('                                                        ( ART INTEGRATED PROJECT )')
print("""______________________________________________________________________________________________________________________________________""")
print(" ")


#functions used in the code
def user_menu():
    global b
    print("1. Issue a book")
    print("2. Return a book")
    print("3. Search for a book")
    print("4. View all the available books")
    print("5. Raise a request for extension of due date")
    print("6. Exit")
    b=int(input("Enter Choice:"))






#code

while True:
    h=passw.getpass(prompt="enter your sql password: ")
    val=input("does your database exist? y or n: ") #i have to add a generate table right here
    if val == 'y':
        data=input("enter an existing database name: ")
        ex=True
        try:
            db=x.connect(host="localhost", user="root",passwd=h,db=data)
            print("Connected Successfully!\n")
            break
        except Exception as e:
            print("there is an error, please try again", e)
            print(e)
            ex=False
    elif val == 'n':
        try:
            db=x.connect(host="localhost", user="root",passwd=h)
            cur=db.cursor()
            cur.execute('create database library')
            print("A database named library is created")# i need to add a generate table and records here too
            ex=True
            break
        except Exception as e:
            print("there is some error, try rechecking the password")
            print(e)
            ex=False
while ex:
    print("============================")
    print("LIBRARY DATABASE SYSTEM")
    print("============================")
    print("Welcome, please select portal")
    print("1. User")
    print("2. Admin")
    c=int(input("Enter Choice:"))

    if c==2:
        passwd=passw.getpass(prompt="enter password: ")
        if passwd == h:
            print("Welcome admin, please select an option below")
#make functions and add here for admin to run as that is convenient, menu too


            
        else:
            print("access denied, incorrect password")
    elif c==1:
        print("Welcome user, please select an option below")
        user_menu()
        if b==1:
            issue= input("which book do you wish to issue?: ")
            # i would need to add some commands here



