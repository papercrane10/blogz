def is_valid(user_input):
        length = len(str(user_input))
        if length >= 3 and length<=20:
            return True
        else:
            return False
def validate(username, password, validate):
  
    username = username
    user_password = password
    password_confirm = validate
     
    test = 0
    if is_valid(username):
        test += 1
    else:
        test = 0
    if is_valid(user_password):
        test += 1
    else:
        test = 0
    if is_valid(password_confirm):
        test += 1
    if str(user_password) == str(password_confirm):
        test += 1
        if is_valid(user_password) == False or is_valid(password_confirm) == False:
            test = 0  
    else:
        test = 0
                   
    if test == 4:
        return True
    else: 
        return False