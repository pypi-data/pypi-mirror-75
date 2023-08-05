from .user_database import Users_DB
class User():
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

def authenticate(username, password):
    user_DB = Users_DB(username, password)
    user_details = user_DB.findUsername()
    return User(user_details[0], user_details[1], user_details[2])

def identity(payload):
    user_DB = Users_DB(username = "", password = "")
    user_id = payload['identity']
    user_details = user_DB.findID(user_id)
    return User(user_details[0], user_details[1], user_details[2])
        

        
    
    


    

