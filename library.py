import pymysql as x
import matplotlib.pyplot as p
import getpass as passw
import tabulate as t
import numpy as num



print("")
print("""______________________________________________________________________________________________________________________________________""")
print('                                                                 (REPORT CARD)                                             ')
print ('                                                        ( ART INTEGRATED PROJECT )')
print("""______________________________________________________________________________________________________________________________________""")
print(" ")

while True:
    h=passw.getpass(prompt="enter your sql password: ")
    data=input("enter an existing database name: ")
    ex=True
    try:
        db=x.connect(host="localhost", user="root",passwd=h,db=data)
        print("Connected Successfully!\n")
        break
    except Exception as e:
        print("there is an error, please try again", e)
        ex=False
while ex:
    print("                                                           ")
    print("============================")
    print("STUDENT REPORTCARD DETAILS")
    print("============================")
    print("Menu")
    print("============================")
    print("1. Generate Table")
    print("2. Add Record")
    print("3. Display Record")
    print("4. Display Bar Graph")
    print("5. Exit")
    c=int(input("Enter Choice:"))

#Generates a premade table
    if c==1:
        try:
            tablen= input("enter table name")
            db=x.connect(host="localhost",user="root", passwd=h,db=data)
            cur=db.cursor()
            cur.execute("create table {}(roll int,name char(20),grade char(5),maths int, phy int, chem int, english int);".format(tablen))
            db.commit()
            cur.close()
            db.close()
            print("table created")
        except Exception as f:
            print('cannot create table,','reason:',f)
            pass
        

#Adds record to the table generated above
    elif c==2:
        tablen= input("enter table name")
        db=x.connect(host="localhost",user="root",passwd=h,db=data)
        cur=db.cursor()
        cur.execute("insert into {} values(1,'rahul','A1', 86,92,87,95);".format(tablen))
        cur.execute("insert into {} values(2,'manas','C1',78,83,81,74);".format(tablen))
        cur.execute("insert into {} values(3,'aditi','A2',90,88,85,91);".format(tablen))
        cur.execute("insert into {} values(4,'soumya','B1',84,61,88,90);".format(tablen))
        cur.execute("insert into {} values(5,'dev','B1',75,71,76,65);".format(tablen))
        cur.execute("insert into {} values(6,'riya','B2',76,84,85,79);".format(tablen))
        db.commit()
        cur.close()#
        db.close()
        print("record added")

#Option to display records
    elif c==3:
        tablen= input("enter table name")
        print("1. Display all student records")
        print("2. Display individual student records")
        print("3. Return")
        d=int(input("Enter choice: "))

        #Displays all
        if d==1:
            db=x.connect(host="localhost",user="root",passwd=h,db=data)
            print("=====================================")
            cur=db.cursor()
            whole=cur.execute("select * from {};".format(tablen))
            wholedata=cur.fetchall()
            print(t.tabulate(wholedata, headers=['rollno', ' name' ,'grade', 'maths','phyics' ,'chemistry','english'], tablefmt='grid'))
            cur.close()
            db.close()

        #Displays Individually
        elif d==2:
            db=x.connect(host="localhost",user="root",passwd=h,db=data)
            cur=db.cursor()
            rd=int(input("Enter Roll No.:"))
            aa=cur.execute("select * from {} where roll={}".format(tablen,rd))
            inddata=cur.fetchone()
            print(t.tabulate([inddata], headers=['rollno', ' name' ,'grade', 'maths','physics' ,'chemistry','english']))

        #Returns the program
        elif d==3:
            exit

        #For entering incorrect / non existing option
        else:
            print("invalid choice")

#Option To display graphs
    elif c==4:
        tablen= input("enter table name")
        print("1. Display Bar Graph - Total Student Marks")
        print("2. Display Bar Graph - Average Student Marks")
        print("3. Display Bar Graph - Individual Student Wise")
        print("4. Display Bar Graph - All")
        print("5. Return")
        d=int(input("enter choice: "))
        
        #Displays total student marks graph
        if d==1:
            db=x.connect(host="localhost",user="root",passwd=h,db=data)
            cur=db.cursor()
            whole=cur.execute("select * from {};".format(tablen) )
            data=cur.fetchall()
            total=[]
            students=[]
            for i in data:
                a=i[3]+i[4]+i[5]+i[6]
                avg=a/4
                total.append(a)
                b=i[1]
                students.append(b)

            p.bar(students,total,color="blue",width=0.5, label="student total marks")
            cur.close()
            db.close()
            p.legend()
            p.show()

        #Displays total student average marks graph
        elif d==2:
            db=x.connect(host="localhost",user="root",passwd=h,db=data)
            cur=db.cursor()
            whole=cur.execute("select * from {};".format(tablen))
            data=cur.fetchall()
            av=[]
            students=[]

            for i in data:
                a=i[3]+i[4]+i[5]+i[6]
                avg=a/4
                av.append(avg)
                b=i[1]
                students.append(b)

            p.bar(students,av,color="orange", width=0.5, label="student average marks")
            cur.close()
            db.close()
            p.legend()
            p.show()

        #Displays individual student marks graph
        elif d==3:
            db=x.connect(host="localhost",user="root",passwd=h,db=data)
            cur=db.cursor()
            r=int(input("Enter Roll No.:"))
            aa=cur.execute("select * from {} where roll={};".format(tablen,r) )
            data=cur.fetchall()

            subj=["maths","physics","chemistry","english"]
            for i in data:
                name=i[1]
                a=i[3]
                b=i[4]
                c=i[5]
                d=i[6]
                marks=[a,b,c,d]

            p.bar(subj,marks,width=0.5,color="cyan",label=name)
            cur.close()
            db.close()
            p.legend()
            p.show()

        #DIsplays all the graphs together   
        elif d==4:
            db=x.connect(host="localhost",user="root",passwd=h,db=data)
            cur=db.cursor()
            whole=cur.execute("select * from {};".format(tablen) )
            data=cur.fetchall()
            students=[]
            total=[]
            av=[]
            
            for i in data:
                a=i[3]+i[4]+i[5]+i[6]
                avg=a/4
                av.append(avg)
                total.append(a)
                b=i[1]
                students.append(b)
            index_shift=num.arange(len(students))

            p.bar(index_shift+0.4,total,color="yellow",width=0.4, label="student total marks")
            p.bar(index_shift,av,color="orange", width=0.4, label="student average marks")
            p.ylim(0,400)
            #changes labels
            p.xticks(index_shift, students,horizontalalignment='center')
            p.legend()
            p.show()
            cur.close()
            db.close()
            

        #Return to program
        elif d==5:
            exit
            
        #For entering incorrect / non existing option
        else:
            print("invalid choice, please select a number above")
                
    #Quit the program      
    elif c==5:
        quit()

    #For entering incorrect / non existing option
    else:
        print("invalid choice")   



