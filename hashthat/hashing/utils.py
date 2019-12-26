import hashlib

def get_hash(algo, text):
    hashFunc = hashlib.new(algo)
    hashFunc.update(text.encode('utf-8'))
    text_hash = hashFunc.hexdigest()

    return text_hash
