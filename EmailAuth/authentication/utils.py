import random
import string

def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))
    return otp