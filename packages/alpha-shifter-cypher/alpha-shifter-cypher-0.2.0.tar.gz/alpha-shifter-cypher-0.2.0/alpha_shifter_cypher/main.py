from fire import Fire


# configured as tool script in pyproject.toml
def activate():
    # create a new CLI with commands mapped to functions
    Fire({
        "encrypt": encrypt,
        "decrypt": decrypt
    })

# decrypt a message by shifting its characters backward
def decrypt(message, amount = 1):
    return shift_message(message, -1 * amount)

# encrypt a message by shifting its characters forward
def encrypt(message, amount = 1):
    return shift_message(message, amount)

# shift a character in a direction
# e.g. a, 1 -> b; x, 2 -> z
def shift_char(c, direction):
    return chr(ord(c) + direction)

# shift a message in a direction
# e.g. hello, 1 -> ifmmp; ifmmp, -1 -> hello
def shift_message(message, direction):
    return "".join([shift_char(c, direction) for c in message])
