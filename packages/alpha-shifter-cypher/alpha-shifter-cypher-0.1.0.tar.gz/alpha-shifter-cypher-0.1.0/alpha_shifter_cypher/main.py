from fire import Fire
from cypher import encrypt, decrypt

def activate():
    Fire({
        "encrypt": encrypt,
        "decrypt": decrypt
    })
