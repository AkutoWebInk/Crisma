import sqlite3

class Database:
     def __init__(self):
          # Loading/Conecting Databse
          self.connection = sqlite3.connect("Database") 
          self.cursor = self.connection.cursor() 
          #self.createDbTable()
     def createDbTable(self):
               # Creates the main table.
               self.cursor.execute(f"CREATE TABLE IF NOT EXISTS USER(USERNAME, PASSWORD, PROFILEPIC)")
               self.cursor.execute(f"CREATE TABLE IF NOT EXISTS ITEM(NAME, REFERENCE, CODE, LINE, CAPACITY, QUANTITY, IMAGE)")
               
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

class ServerAccess(Database):
     def __init__(self):
          super(). __init__()

     def searchDb_username(self, username):
          self.cursor.execute ("SELECT * FROM USER WHERE USERNAME = ?", (username,))
          self.returned_user = self.cursor.fetchone()
          #print(f"{self.returned_user}")
          return self.returned_user
     
     def searchDb(self, user_search = None):
          if user_search:
               query = "SELECT * FROM ITEM WHERE NAME LIKE ? OR CODE LIKE ? OR LINE LIKE ? OR REFERENCE LIKE ?"
               params = [f"%{user_search}%",f"%{user_search}%",f"%{user_search}%",f"%{user_search}%"]
          
          else:
               query = "SELECT * FROM ITEM"
               params = []
          
          self.cursor.execute(query, params) # Tell the cursor that points to the server to execute query + list of any params filled:
          results = self.cursor.fetchall()   # Store the results into a variable
          self.connection.commit()           # Send all the previous command to the database

          return results

     def print_all_users(self):
          self.cursor.execute("SELECT * FROM USER")
          all_users = self.cursor.fetchall()  # Fetch all user records

          # Print each user's information
          for user in all_users:
               print(f"User: {user}")  # This will print each user tuple

if __name__ == "__main__":
     Access = ServerAccess()
     Access.print_all_users()
     Access.cursor.execute("UPDATE USER SET PROFILEPIC = ? WHERE USERNAME = ?", ("user_profile_pics/christian_pfp.png", "Christian"))
     Access.connection.commit()
