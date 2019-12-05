import hashlib


def encryption(salt, pwd):
    md5 = hashlib.md5(salt.encode())
    md5.update(pwd.encode())
    return md5.hexdigest()
