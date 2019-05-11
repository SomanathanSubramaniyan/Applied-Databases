# Applied Database
# Final Project
# Section 4.4 - Python program answers
# Author : Somu

#!/usr/bin/python
import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

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

def DBconnection(query,choice,code):
    try:
        connection = mysql.connector.connect(host='localhost',database='world', user='root', password='Somu@1975')
        cursor = connection.cursor(prepared=True)
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
    main()

def main():
    while True:
        menu()
        choice = input("Choice : --> ")
        if choice == "x":
            print("Bye - Program Terminate now and welcome back anytime!")
            return
        elif choice == "1":
            query= "select * from city limit 15"
            DBconnection (query, choice,"")
        elif choice == "2":
            print("Cities by Population")
            print("--------------------")
            Comparison = input("Enter  <, > or =   :")
            if Comparison == "<" or Comparison == ">" or Comparison == "=":
                query = "select * from city where population" + Comparison
            else:
                displaymenu()
                return
            Value= input("Enter Population :")
            try:
                Value = int(Value)
            except ValueError:
                displaymenu()
                return
            query = "select * from city where population" + Comparison + str(Value)
            DBconnection (query, choice,"")
        elif choice == "3":
            print("Add New City")
            print("------------")
            City= input("Enter City Name :")
            Code= input("Country Code :")
            district= input("District :")
            pop= input("Population :")
            query = "Insert INTO city (name, countrycode,district,population) VALUES ('" + City + "','" + Code + "','" + district + "',"+ str(pop)+")"
            DBconnection (query, choice, Code)
            

        else:
            print("That is not a valid choice. You can only choose from the menu.")
        input("\nPress enter to continue...")

if __name__ == "__main__":
    main()