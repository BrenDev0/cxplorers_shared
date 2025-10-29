from cryptography.fernet import Fernet
import os 

from cxplorers_shared.domain.services.encryption_service_base import EncryptionServiceBase

class EncryptionService(EncryptionServiceBase):
    def __init__(self):
        self.secret_key = os.getenv("ENCRYPTION_KEY")
        self.fernet = Fernet(self.secret_key)

    def encrypt(self, plaintext: str) -> str:
        encrypted = self.fernet.encrypt(plaintext.encode())
        return encrypted.decode()

    def decrypt(self, ciphertext: str) -> str:
        decrypted = self.fernet.decrypt(ciphertext.encode())
        return decrypted.decode()