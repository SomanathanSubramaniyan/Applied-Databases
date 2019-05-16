# Applied Database
# Final Project
# Section 4.4 - Python program 
# Author : Somu

#mySQL modules import
#Mongo modules import
#Pandas printing module
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
import pandas as pd
import pymongo
from pymongo import MongoClient
from tabulate import tabulate

# This function will display a Menu as requested in the project specification document
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

# Set the global variable to ensure Option 6 and option 7 are executed only once
# Option 6: View countries by name 
# Option 7: View countries by population
# Declare a pandas dataframe and dfp as a global variable

myclient = None
global dfp, df
dfp =""
df = pd.DataFrame()

# This function will set the global variable dfp so that the SQL connector connects to the DB only once
def globalSet():
    global dfp
    dfp = "2"


# Function to make a connect to the MongoDB database
# Connection parameters are localhost and the port number is 27017
# Option 4: Find car by Engine Size
# Option 5: Add New car

def Mongoconnect(csize,choice,id,reg,size):
    try:
        global myclient
        myclient =pymongo.MongoClient(host = "localhost",port=27017)
        myclient.admin.command('ismaster')
        mydb = myclient['docs']
        docs = mydb["docs"]
        if choice == "4":
            query = {"car.engineSize":float(csize)}
            car = docs.find(query)
            for p in car:
                print ('{0} | {1}| {2} | {3}'.format(p["_id"],p['car']["reg"],p["car"]['engineSize'],p['addresses']))
        if choice == "5":
            query={"_id":int(id), "car": { "reg":reg,"engineSize":float(size)}}
            x = docs.insert_one(query)
            query = {"_id":int(id)}
            car = docs.find(query)
            for p in car:
                print ("-------------Results------------------------------")
                print (p)
                print ("--------------------------------------------------")
    except:
        print("*************** Error occured while executing MongoDB connection commands****************")

# MYSQL connections. The below code block establishes SQL connetion and executes the required query
# Option 1: View 15 cities
# Option 2: View cities by population
# Option 3: Add new city
# Option 6: View countries by name 
# Option 7: View countries by population
# The data retrieved for option 6 or 7 are stored in the panda's and retrieved for the other options (6 or 7) without making additional connection to databse
# Try and exception block handles any database connection or duplicate key issues

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
        elif error.errno == 2003:
            print("----------------------------------------------------")
            print("***ERROR***: mySQL server is down.")
            print("----------------------------------------------------")
        else:
            print("Undefined error")

# Function to repeat the incorrect choice
def displaymenu():
    print("This is not a valid choice. You can only choose from the above options")
    input("\nPress enter to continue...")

# The below code block accepts input values for all the 8 options and calls either mysql or mongodb function blocks
    # Option 1: View 15 cities
    # Option 2: View cities by population
    # Option 3: Add new city
    # Option 4: Find car by Engine Size
    # Option 5: Add New car
    # Option 6: View countries by name 
    # Option 7: View countries by population
# User input validations are performed for the all entered values using << while loop>> until correct values are entered
# <<if loop>> is used to select the individual code block for each of the menu options

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
            print("show cars by engine size")
            print("------------------------")
            while True:
                csize = input("Enter Car Engine Size :")
                break
            Mongoconnect(csize,choice,"","","")
        elif choice == "5":
            print("Add New Car")
            print("-----------")
            id= input("_ids:")
            reg= input("Enter reg :")
            size= input("Enter Size :")
            Mongoconnect("",choice,id,reg,size)
            
        else:
            print("That is not a valid choice. You can only choose from the menu.")
        input("\nPress enter to continue...")

# Main function
if __name__ == "__main__":
    main()