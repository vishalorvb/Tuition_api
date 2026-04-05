from cryptography.fernet import Fernet
import base64
import hashlib

        
class encryption():
    def convert_to_32_byte_key(input_string):
        hashed_string = hashlib.sha256(input_string.encode()).digest()
        encoded_key = base64.urlsafe_b64encode(hashed_string)
        padded_key = encoded_key.ljust(32, b'=')
        return padded_key  
    
    def __init__(self,secret_key):
        self.key =encryption.convert_to_32_byte_key(secret_key) 
        
    def encrypt_string(self,input_string):
        cipher = Fernet(self.key)
        input_bytes = input_string.encode()
        encrypted_bytes = cipher.encrypt(input_bytes)
        encrypted_string = encrypted_bytes.decode()
        return encrypted_string
    
    def decrypt_string(self,encrypted_string):
        try:
            cipher = Fernet(self.key)
            encrypted_bytes = encrypted_string.encode()
            decrypted_bytes = cipher.decrypt(encrypted_bytes)
            decrypted_string = decrypted_bytes.decode()
            return decrypted_string
        except :
           return None
    

class GenerateString:
    def __init__(self,value):
        self.value = value
        self.__Code = ["R", "p", "M", "l", "^", "$", "m", "r", "F", "z"] 
        
    def encode(self):
        num = int(self.value) + 70762
        s = ""
        while(num != 0):
            rem = num % 10
            s = s + self.__Code[rem]
            num = num // 10
            
        
        return s   