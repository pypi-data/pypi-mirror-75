def decrypt(message, amount = 1):
    return shift_message(message, -1 * amount)


def encrypt(message, amount = 1):
    return shift_message(message, amount)


def shift_message(message, direction):
    return "".join([shift_char(c, direction) for c in message])


def shift_char(c, direction):
    return chr(ord(c) + direction)
