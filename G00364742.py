# Applied Database
# Final Project
# Section 4.4 - Python program answers
# Author : Somu

#mySQL modules import
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import pandas as pd
#Mongo modules import
import pymongo
from pymongo import MongoClient
#Pandas printing module
from tabulate import tabulate

# This function will display a Menu as requested in the project specification
def menu():
    print("--------")
    print("World DB")
    print("--------")
    print("Menu")
    print("====")
    print("1  -  View 15 Cities")
    print("2  -  View Cities by population")
    print("3  -  Add New City")
    print("4  -  Find Car by Engine Size")
    print("5  -  Add New Car")
    print("6  -  View Countries by name")
    print("7  -  View Countries by population")
    print("x  -  Exit application")

Mongoclnt = None

def Mongoconnect(csize):
    global Mongoclnt
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    DB_NAME = 'MongoDB'
    COLLECTION_NAME = 'MongoDB'
    Mongoclnt = MongoClient(MONGODB_HOST,MONGODB_PORT)
    Mongoclnt.admin.command('ismaster')
    db = Mongoclnt['MongoDB']
    doc = db["MongoDB"]
    query="{'car.engineSize': " + str(csize) + "}"
    print(query)
    car=doc.find(query)
    for p in car:
        print(p)

global dfp, df
dfp =""
df = pd.DataFrame()

def globalSet ():
    global dfp
    dfp = "2"

def DBconnection(query,choice,code,param1):
    try:
        connection = mysql.connector.connect(host='localhost',database='world', user='root', password='Somu@1975')
        cursor = connection.cursor(prepared=True)
        global dfp,df
        if (choice == "6" or choice == "7") and dfp != "2" :
            df = pd.read_sql_query(query, connection)
            globalSet()

        if choice == "1" :
            cursor.execute(query) 
            names = list(map(lambda x: x[0], cursor.description))
            print("----------------------------------------------------------------------------------")
            print("{:5} | {:^20} | {:^12} | {:^20} | {:10}".format(names[0],names[1],names[2],names[3],names[4]))
            print("----------------------------------------------------------------------------------")
            for (id,name, countrycode, district,population, latitue,longitude) in cursor:
                print("{:5} | {:^20} | {:^12} | {:^20} | {:d}".format(id,name, countrycode, district,population))
        elif choice == "2" :
            cursor.execute(query) 
            names = list(map(lambda x: x[0], cursor.description))
            print("----------------------------------------------------------------------------------")
            print("{:5} | {:^20} | {:^12} | {:^20} | {:10}".format(names[0],names[1],names[2],names[3],names[4]))
            print("----------------------------------------------------------------------------------")
            for (id,name, countrycode, district,population, latitue,longitude) in cursor:
                print("{:5} | {:^20} | {:^12} | {:^20} | {:d}".format(id,name, countrycode, district,population))
        elif choice == "3":
            cursor.execute(query) 
            connection.commit
            print("**** RESULT ***** The new city record is inserted into the table")
        elif choice == "6" :
            df1 = df[df["Name"].str.contains(code)].loc[:,["Name","Continent","population","HeadofState"]]
            #print tabulate(df1.to_string(index=False))
            print(tabulate(df1, headers="keys",tablefmt="orgtbl"))
        elif choice == "7":
            if param1 == ">":
                df1 = df[(df["population"] > int(code)) ].loc[:,["Name","Continent","population","HeadofState"]]
            elif param1 == "<":
                df1 = df[(df["population"] < int(code)) ].loc[:,["Name","Continent","population","HeadofState"]]
            elif param1 == "=":
                df1 = df[(df["population"] == int(code)) ].loc[:,["Name","Continent","population","HeadofState"]]
            print(tabulate(df1, headers="keys",tablefmt="orgtbl"))

    except mysql.connector.Error as error :
        if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif error.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        elif error.errno == 1452:
            print("----------------------------------------------------")
            print("***ERROR***: Country Code "+ code + " does not exist")
            print("----------------------------------------------------")

        else:
            print("Failed to connect to the database: {}".format(error))
        connection.rollback()

    finally:
        #closing database connection.
        if(connection.is_connected()):
            connection.close()

def displaymenu():
    print("This is not a valid choice. You can only choose from the above options")
    input("\nPress enter to continue...")

def main():
    while True:
        menu()
        choice = input("Choice : --> ")
        Code,param1 = "",""
        if choice == "x":
            print("Bye - Program Terminate now and welcome back anytime!")
            return
        elif choice == "1":
            query= "select * from city limit 15"
            DBconnection (query, choice,Code,param1)
        elif choice == "2":
            print("Cities by Population")
            print("--------------------")
           
            while True:
                Comparison = input("Enter  <, > or =   :")
                if Comparison == "<" or Comparison == ">" or Comparison == "=":
                    query = "select * from city where population" + Comparison
                    break
                else:
                    displaymenu()
            
            while True:
                Value= input("Enter Population :")
                if Value.isdigit() == True:
                    query = query +  str(Value)
                    break
                else:
                    displaymenu()
            DBconnection (query, choice,Code,param1)
        elif choice == "3":
            print("Add New City")
            print("------------")
            City= input("Enter City Name :")
            Code= input("Country Code :")
            district= input("District :")
            pop= input("Population :")
            query = "Insert INTO city (name, countrycode,district,population) VALUES ('" + City + "','" + Code + "','" + district + "',"+ str(pop)+")"
            DBconnection (query, choice, Code,param1)
        elif choice == "6":
            print("Countries by Name")
            print("-----------------")
            Ctyname = input("Enter Country Name :")
            query = "select code, Name, Continent,population,HeadofState from country" 
            Code=Ctyname
            DBconnection (query, choice, Code,param1)
        elif choice == "7":
            print("Countries by Population")
            print("-----------------------")
            query = "select code, Name, Continent,population,HeadofState from country" 
            while True:
                Comparison = input("Enter  <, > or =   :")
                if Comparison == "<" or Comparison == ">" or Comparison == "=":
                    param1=Comparison
                    break
                else:
                    displaymenu()
            while True:
                Value= input("Enter Population :")
                if Value.isdigit() == True:
                    Code = Value
                    break
                else:
                    displaymenu()
            DBconnection (query, choice, Code,param1)
        elif choice == "4":
            print("Enter car engine size")
            print("---------------------")
            csize = input("Enter Car Engine Size :")
            Mongoconnect(csize)
            

        else:
            print("That is not a valid choice. You can only choose from the menu.")
        input("\nPress enter to continue...")

if __name__ == "__main__":
    main()