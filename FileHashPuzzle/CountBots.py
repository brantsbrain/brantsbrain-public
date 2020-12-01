import hashlib, os

# To merge files in Windows CMD - for /R %f in (*.sha1) do type "%f" >> mergefile.txt
# To merge files in Linux - sudo find ./ -name '*.sha1' -exec cat {} \; >> mergefile.txt

counter = 0

print("\nATTN: Run this file in the root directory of all the account folders\n")

opersys = input("\nWhat OS is running? (L/W): ")

if opersys.upper() == "W":
    os.system('for /R %f in (*.sha1) do type "%f" >> mergefile.txt')
elif opersys.upper() == "L":
    os.system("find ./ -name '*.sha1' -exec cat {} \; >> mergefile.txt")
else:
    print("Invalid entry. Exiting...")
    exit()

with open("mergefile.txt", "r") as mergefile:
    for line in mergefile:
        if hashlib.sha1("000".encode()).hexdigest().lower() in line.lower():
            counter += 1
        elif hashlib.sha1("0000".encode()).hexdigest().lower() in line.lower():
            counter += 1
        elif hashlib.sha1("00000".encode()).hexdigest().lower() in line.lower():
            counter += 1

print(f"\nFound {counter} bots")
