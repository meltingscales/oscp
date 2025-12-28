#!/usr/bin/env python3
import base64

print(base64)

print(dir(base64))

# uncomment and run to see help
# help(base64)
# help(base64.b64decode)
# help(base64.decode)


fh = open('./pwdbackup.txt','r')
print(fh)

# read all lines into a list like this
# [0: comment; 1: big_binary_blob]
lines = fh.readlines()

# get the last item in the list of two
encodedPassword = lines[1]

# print a lil bit
print(encodedPassword[0:10])


# base case
# nop
decodedSomeTimes = encodedPassword

# strip whitespace just in case 
decodedSomeTimes=decodedSomeTimes.strip()

decodedSomeTimes=decodedSomeTimes.replace(' ','')

def ensure_padding(s):
    """Ensures the Base64 string has the correct padding."""
    missing_padding = len(s) % 4
    if missing_padding:
        s += '=' * (4 - missing_padding)
    return s

# recurse (sort of.)
for i in range(0,15):
    decodedSomeTimes = base64.b64decode(ensure_padding(decodedSomeTimes))
    decodedSomeTimes = decodedSomeTimes.decode('latin-1')  # Or 'ascii' if needed
print("i="+(str(i)))
print(decodedSomeTimes)

# base64.decode()

fh.close()

# OKAY! It actually fails, but, I got close. I think.

# I used an online decoder.

#        Charix!2#4%6&8(0