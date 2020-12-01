import os

confirm = input("ATTN: This will DELETE every folder with the name 1111-2222. Type Y to confirm: ")

if confirm.upper() != "Y":
    exit()

opersys = input("What operating system is running? W/L: ")

if opersys.upper() == "W":
    for folder in os.listdir():
        try:
            if int(folder) in range(1111,2222):
                os.system(f"rmdir {folder} /s /q")
        except Exception as e:
            print(f"Exception occurred: {e}")
    os.system("rm mergefile.txt")
elif opersys.upper() == "L":
    for folder in os.listdir():
        try:
            if int(folder) in range(1111,2222):
                os.system(f"rm {folder} -rf")
        except Exception as e:
            print(f"Exception occurred: {e}")
    os.system("rm mergefile.txt")
else:
    print("Invalid entry. Exiting...")
