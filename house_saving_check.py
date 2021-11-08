#Script which uses MYSQL and BeautifulSoup to store, scrape and eventually view plans for saving up for homes.
#The average house price for the user specified postcode has been taken from RightMove. 
import csv
from bs4 import BeautifulSoup
from urllib import request
import mysql.connector
#Database information is hidden.
mydb = mysql.connector.connect(
    host="sql4.freesqldatabase.com",
    user="xxxxxx",
    password="xxxxxx",
    database="xxxxxx")


cursor = mydb.cursor(buffered=True)

def create_tables():
    cursor.execute("CREATE TABLE users (username VARCHAR(255), password VARCHAR(255))")
    cursor.execute("CREATE TABLE checks (username VARCHAR(255), monthly VARCHAR(255), post_code VARCHAR(255), average_price VARCHAR(255))")

def login():
    global username
    username=input("Please enter your username\n")
    password=input("Please enter your password\n")
    #Need a way to validate usernames and passwords.
    
def register():
    username=input("Please enter your desired username\n")
    password=input("Please enter a password\n")
    usr_pass=(username, password)

    cursor.execute("SELECT username FROM users")
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if len(mycursor.fetchall())>=1:
        print("Already in use.")
        register()
    else:
        print("Proceed")
        mycursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", usr_pass)
        mydb.commit()
        mycursor.execute("INSERT INTO checks (username, monthly, post_code, average_price) VALUES (%s, %s, %s, %s)", (username, None, None, None))
        mydb.commit()
    

def new_plan():
#Monthly savings are inputted so possible long term investments can be suggested. 
    monthly=int(input("Enter your monthly savings:\n"))
    cursor.execute("UPDATE checks SET monthly = %s WHERE username = %s", (monthly, username))
    mydb.commit()

    post_code=input("Enter the post code where your potential home is going to be located:\n").strip().replace(" ", "").upper()
    split=list(post_code)
    split.append(split[len(split)-1])
    for x in [2,3]:
        split[len(split)-(x)]=split[len(split)-(x+1)]
    split[len(split)-4]=" "
    post_code=("".join(split))

#Checking that the entered post code is valid by seeing if it is present in a CSV file containing UK postcodes.
    with open('ukpostcodes.csv', 'rt') as f:
         reader = csv.reader(f, delimiter=',')
         for row in reader:
              for field in row:
                  if field == post_code:
                      print("Post code is valid")
                      del split[len(split)-4]
                      mod_post_code=("".join(split))

                      url="https://www.rightmove.co.uk/house-prices/"+ mod_post_code +".html?country=england&searchLocation="+ mod_post_code
                      html=request.urlopen(url).read().decode('utf8', 'ignore')
                      soup=BeautifulSoup(html, "html.parser")
                      
                      test=str(soup.find("meta", {'name':'description'}))
                      remove=test.replace(post_code,"");
                      final=re.sub("[^0-9]", "", remove)
                      final=list(final)
                      for x in [1,2,3,4]:
                          del final[(len(final)-1)]            
                      avg_house_price=("".join(final))

                      print("The average house price in your desired area is £"+avg_house_price + ".")

                      cursor.execute("UPDATE checks SET post_code = %s WHERE username = %s", (post_code, username))
                      mydb.commit()

                      cursor.execute("UPDATE checks SET average_price = %s WHERE username = %s", (avg_house_price, username))
                      mydb.commit()


#Checking if there are tables already in the database.
cursor=mydb.cursor(buffered=True)
cursor.execute("SHOW TABLES")
initial_tables=0
for x in cursor:
  print(x)
  initial_tables=initial_tables+1
if initial_tables==0:
    create_tables()

#Logging in and registering, currently the register function offers more options than the login one.
log_or_reg=input("Would you like to login or register?\n").lower()
if log_or_reg=="login":
    login()
    #Need to add a way for users with 'accounts' to view their previous plan or make a new one.
elif log_or_reg=="register":
    register()
    login()





