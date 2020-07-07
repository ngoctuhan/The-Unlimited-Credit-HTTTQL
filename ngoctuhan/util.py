import random
import string

class Handel:
    # def __init__(seft):
    def get_password(seft):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join((random.choice(lettersAndDigits) for i in range(8)))

    def get_username(seft, username):
        letters = string.ascii_letters
        temp = ''.join(random.choice(letters) for i in range(5))
        return username + temp
    
    def handel_Hoten(seft, name):
        str = name.split(" ")
        return str[len(str)-1]
    
if __name__ == '__main__':
    hd = Handel()
    print(hd.get_username("viet"))
    print(hd.get_password())
    print(hd.handel_Hoten("viet le ngoc"))