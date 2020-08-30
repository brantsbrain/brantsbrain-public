import hashlib

print("\nTo hash anything using hashlib, the string must be encoded using encode(), plugged into the desired hashlib algorithm, then run through hexdigest()")

print("\nHere are the hashing steps for the word 'apple'")
encodedapple = "apple".encode()
print("Encoded apple - " + str(encodedapple))
print("Encoded apple run through hashlib.md5() - " + str(hashlib.md5(encodedapple)))
print("MD5 run through hexdigest - " + str(hashlib.md5(encodedapple).hexdigest()))

# All of this can be shortened into one line
print("\nApple hash - " + hashlib.md5("apple".encode()).hexdigest())
