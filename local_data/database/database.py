import sqlite3
import os

class Database:
     def __init__(self):
          # Loading/Conecting Databse
          db_path = os.path.abspath("local_data/database/Database.db")
          self.connection = sqlite3.connect(db_path) 
          self.cursor = self.connection.cursor()
     
     def createDbTable(self):
               # Creates the main table.
               self.cursor.execute(f"CREATE TABLE IF NOT EXISTS USERS(ID INTEGER PRIMARY KEY AUTOINCREMENT,NAME VARCHAR(255),USERNAME VARCHAR(255) UNIQUE,PASSWORD VARCHAR(255),ACCESS_LEVEL INT,PROFILEPIC_PATH VARCHAR(255))")
              
               self.cursor.execute(f"CREATE TABLE IF NOT EXISTS ITEM(NAME, REFERENCE, CODE, LINE, CAPACITY, QUANTITY, IMAGE)")
               
               #self.cursor.execute("DROP TABLE users")
               
               self.connection.commit()
               
               print("\n dev note: createDbTable script ran successfully. \n ")

class Item:
     def __init__(self, code, name, line, reference, quantity, image = None):

          self.no_image=str("icons/no_image_icon.png")
          self.name=name
          self.line=line
          self.quantity=quantity
          self.image=image if image is not None else self.no_image
          self.code=code
          self.reference=reference

class User:
     def __init__(self, name, username, password, access_level, image=None):
          self.no_image_path=str("icons/user_icon.png")
          self.name=name
          self.username=username
          self.password=password
          self.access_level=access_level
          self.image=image if image is not None else self.no_image_path

class Access(Database):
     def __init__(self):
          super(). __init__()

     def searchDb_username(self, username):
          
          self.cursor.execute ("SELECT * FROM USERS WHERE USERNAME =?", (username,))
          
          self.answer = self.cursor.fetchone()
          
          if self.answer is not None:
               try:
                    self.user_profilePic = self.answer[5]
                    self.user_Id = self.answer[0]
                    print(f"\nLocal Database method called: searchDb_username\n"
                          f"\nLocal Database Response: User Id: {self.user_Id}, User Picture: {self.user_profilePic}\n")
                    return self.user_profilePic, self.user_Id
               
               except Exception as e:
                    print(e)
     
     def searchDb_userPassword(self, id, password):
          self.cursor.execute ("SELECT * FROM USERS WHERE ID =? AND PASSWORD=?", (id, password))
          self.answer = self.cursor.fetchone()
          if self.answer is not None:
               try:
                    self.user_password = self.answer[3]
                    return self.user_password
               
               except Exception as e:
                    print(e)

     def searchDb_item(self, user_search = None):
          if user_search:
               query = "SELECT * FROM ITEM WHERE NAME LIKE ? OR CODE LIKE ? OR LINE LIKE ? OR REFERENCE LIKE ?"
               params = [f"%{user_search}%",f"%{user_search}%",f"%{user_search}%",f"%{user_search}%"]
          
          else:
               query = "SELECT * FROM ITEM"
               params = []
          
          self.cursor.execute(query, params) # Tell the cursor that points to the server to execute query + list of any params filled:
          results = self.cursor.fetchall()   # Store the results into a variable 
          self.connection.commit()           # Send all the previous command to the database
          
          for item in results:
               print(item)
              
          return results

     def print_all_users(self):
          self.cursor.execute("SELECT * FROM USERS")
          all_users = self.cursor.fetchall()  # Fetch all user records

          # Print each user's information
          for user in all_users:
               print(f"User: {user}")  # This will print each user tuple

     def add_new_user(self, name, username, password, access_level, profile_picture_path):
          query = "INSERT INTO USERS (NAME,USERNAME,PASSWORD,ACCESS_LEVEL, PROFILEPIC_PATH) VALUES (?,?,?,?,?)"   
          try:
               self.cursor.execute(query, (name,username,password,access_level,profile_picture_path))#>------/\
               self.connection.commit()
               print(f"\n {name} added to the database.\n")
          except Exception as e :
               if "UNIQUE constraint failed" in str(e):
                    print("\nUser not added: UNIQUE TYPE error.\n")


if __name__=="__main__":
     Acesso = Access()
     Acesso.searchDb_item(user_search=None)
     #Acesso.add_new_user(name="Christian Rodrigues", username="Christian", password="Christian123", access_level=3, profile_picture_path="local_data/user_profile_pics/christian_pfp.png")
     Acesso.print_all_users()
