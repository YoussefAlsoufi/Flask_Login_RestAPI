import string
import random
rooms ={}
def generate_unique_code(length_of_code=4):
    characters = string.ascii_uppercase + string.digits
    while True:
        room_code = ''.join(random.choice(characters) for _ in range (length_of_code))
        if room_code not in rooms:
            break
    
    return room_code
        



