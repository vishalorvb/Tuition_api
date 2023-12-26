from cryptography.fernet import Fernet
import base64
import hashlib





def usefulPrint():
    print(secret_key)
    
    
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
    
