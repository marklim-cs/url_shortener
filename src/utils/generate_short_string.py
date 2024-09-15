import string
import random

def generate_short_string(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url