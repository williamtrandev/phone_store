import time
import hashlib
import uuid


def generate_unique_id_24char():
    current_timestamp = str(int(time.time()))
    result = hashlib.md5(f"{uuid.uuid1().hex}{current_timestamp}".encode()).hexdigest()
    return result[:24]