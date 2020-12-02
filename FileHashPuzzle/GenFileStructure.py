import hashlib, os, random

# Need to generate a folder with 1000+ folders each containing a .sha1 file that has a SHA1 hash of random words, plus a few 000, 0000, and 00000 entries

pause = input("ATTN: Continuing will create 1,000 folders in this directory each with a file containing a hash. Enter Y to continue, otherwise the program will exit: ")

if pause.upper() != "Y":
    print("Did not enter y/Y. Exiting...")
    exit()

accountlist = ["000", "0000", "00000", "Jim", "Bob", "Jane", "Doe", "Billy", "Dorris", "John", "Jannette", "Kelly", "Davis", "Kevin", "Juan", "Jen", "Tom", "Tim", "Tommy", "Timothy"]

num = 1111
zerocounter = 0

print("Creating folders and files...")
while num <= 2111:
    os.system(f"mkdir {num}")
    entry = random.randrange(len(accountlist) - 1)
    os.system(f"echo {hashlib.sha1(accountlist[entry].encode()).hexdigest().lower()} > ./{num}/{num}.sha1")
    num += 1

    if entry == 0 or entry == 1 or entry == 2:
        zerocounter += 1

print(f"Take note: There are {zerocounter} bot hashes")
