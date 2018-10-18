import hashlib

def hash_file(fileame):
    h = hashlib.md5()
    with open(fileame, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

res = hash_file('../db.sqlite3')
print(res)


"""
    6674fef618a5091b70f954cb7f502843
    6674fef618a5091b70f954cb7f502843
    6674fef618a5091b70f954cb7f502843
"""