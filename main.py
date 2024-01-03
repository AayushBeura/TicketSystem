import mysql.connector as mscl
import random
import time 
obj = mscl.connect(host="localhost", user="root", passwd="system", database="BusTravels")
c=obj.cursor()
DDict = {}
c.execute("SELECT PhoneNo, Password from LoginCreds")
D = c.fetchall()
    
for i in D:
    DDict[i[0]]=i[1]
print(DDict)    
def PostSignIn():
    maincheckpoint=True
    while maincheckpoint:
        print('''
        -------------------------------------------------
                       Welcome to the Menu.
            Please choose your desired task operation -
                1. Create New Booking
                2. Check Status of Existing Booking
                3. Exit''')
        obj = mscl.connect(host="localhost", user="root", passwd="system", database="BusTravels")
        MenuInp = int(input("Your choice: "))
        if MenuInp ==1:
            No=int(input("Enter the number of Tickets: "))
            TicketIDDict = {}
            print("==========================================")
            Dest = input("Choose your Destination: ")
            DestinationDict = {}
            if Dest.lower() not in DestinationDict:
                DestinationDict[Dest.lower()] = Dest
            ID = Dest[:2] + str(random.randint(1000,9999))
            TicketIDDict[ID] = "Already Done"
            print("==========================================")
            print('''
                    Seat-Type - - 
                    1. A/C Sleeper
                    2. A/C Seater
                    3. Non-A/C Sleeper
                    4. Non-A/C Seater''')
            Type = int(input("Choose Seat-Type: "))
            TypeDict = {1:"AS01", 2:"AS02", 3:"NS01", 4:"NS02"}
            TicketInfo={}
            for i in range(No):
                        #Passenger Information
                Name = input("Passenger's Name: ")
                Age = int(input("Age :"))
                Gender = input("Gender (M/F): ")
                c=obj.cursor()
                while ID in TicketIDDict:
                    ID = Dest[:2] + str(random.randint(1000,9999))

                TicketIDDict[ID] = "Already Done"
                TicketInfo[i]=ID
                c.execute("SELECT NOW()")
                Date=c.fetchall()
                sql="INSERT INTO PassengersInfo (PSName, Age, Gen, TicketID, DateOfBooking, Dest, UniqueCode) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (Name, Age, Gender, ID, Date[0][0], Dest, TypeDict[Type])
                c.execute(sql, val)


            c=obj.cursor()
            sql="SELECT Price from PriceList where UniqueCode = %s"
            var = (TypeDict[Type])
            c.execute(sql,(var,))
            D=c.fetchall()
            A = D[0][0]
            print("The total price is", No*A)

            Confirm = input("Do you wish to continue ? (Y/N): ")

            if Confirm=='Y':
                c=obj.cursor()
                sql="UPDATE PriceList SET Tickets=Tickets-(%s) WHERE UniqueCode= %s"
                var = (No, TypeDict[Type])
                c.execute(sql,var)
                obj.commit()
                print("Processing transaction...")
                time.sleep(2)
                print("Your ticket has been booked successfully !")
                print('Your Ticket Unique IDS alloted are:') 
                for i in range(No):
                    print(TicketInfo[i])
                time.sleep(1)    
        elif MenuInp==2:
            print('''
                1. Generate Ticket Information
                2. Cancel Booking''')
            MI2 = int(input("Your choice: "))
            if MI2 ==1:
                
                checkpoint=True
                
                while checkpoint:
                    UID = input("Enter your Ticket Unique ID: ")
                    c=obj.cursor()
                    sql="SELECT * from PassengersInfo where TicketID = %s"
                    var = (UID)
                    c.execute(sql,(var,))
                    D=c.fetchall()
                    print(DDict)
                    if UID in DDict:
                        print(f'''
                        ------------------------------------------------
                            Date of Booking: {D[0][4]}

                                Name:        {D[0][0]}
                                Age:         {D[0][1]}
                                Gender:      {D[0][2]}
                                Ticket ID:   {D[0][3]}
                        ------------------------------------------------          ''')
                        time.sleep(1)
                        checkpoint=False
                    else:     
                        print("This Ticket ID doesn't exist. Kindly re-check the entered Ticket ID.")
#DDict

            elif MI2==2:      
                UID = input("Enter your Ticket Unique ID: ")      
                ans= input("Confirm the deletion of your ticket ? (Y/N): ")
                if ans.lower()=='y':
                    print("Deleting your ticket...")
                    c=obj.cursor()
                    sql="SELECT UniqueCode FROM PassengersInfo WHERE TicketID=%s"
                    var = (UID)
                    c.execute(sql,(var,))
                    UnID=c.fetchall()

                    time.sleep(1)
                    sql1="UPDATE PriceList SET Tickets=Tickets+1 WHERE UniqueCode= %s"
                    var1 = (UnID[0][0])
                    c.execute(sql1,(var1,))
                    sql2="DELETE FROM PassengersInfo where TicketID = %s"
                    var2 = (UID)
                    c.execute(sql2,(var2,))
                    print("Your ticket has been deleted successfully...")
                    obj.commit()
        elif MenuInp==3:
            print("Thanks for using our Service.")
            time.sleep(1)
            print("Have a Nice Day !!")
            maincheckpoint=False
        else:
            print("An error occured.")            


print('''
---------------------------------------------
       Welcome to BusTravels Agency
---------------------------------------------''')
print("Thanks for Choosing our Service !!") 

print('''
    1. Login [Existing User]
    2. Sign-Up [New User] ''')

LSD = int(input("Your Choice: "))   

if LSD==2:
    PhoneNo = int(input("Enter your Phone Number :"))
    Pass = input("Enter Password : ")
    RePass= input("Re-enter your Password : ")
    
    
    # print(type(D))
    if PhoneNo in DDict:

        print("This number has already been registered. Kindly Login using your credentials.")
        exit()
    elif Pass == RePass:
        sql="INSERT INTO LoginCreds (PhoneNo, Password) VALUES (%s, %s)"
        DDict[PhoneNo]=Pass
        val = (PhoneNo, Pass)
        c.execute(sql, val)
        obj.commit()
        print("Your account has been successfully registered. Redirecting...")
        time.sleep(1)
        PostSignIn()
    else:
        print("Please re-enter the same password.")
elif LSD==1:
    PhoneNo = int(input("Enter your Phone Number :"))
    checkpoint=True
    while checkpoint:
        Pass = input("Enter Password : ")
        if DDict[PhoneNo]==Pass:
            print("Login verified ! Redirecting...")
            checkpoint=False
            time.sleep(1)
            PostSignIn()
        else:
            print("Your Password is wrong ! Re-enter your Password")
            Opt = input("Do you want to re-enter your password ? (Y/N): ")
            if Opt=="N":
                checkpoint=False
                exit()
else:
    print("Choose one of the given options. THANK YOU !")
    time.sleep(1)
    exit()

