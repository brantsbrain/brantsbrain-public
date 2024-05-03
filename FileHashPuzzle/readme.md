# File Hash Puzzle

### Background

I came across this puzzle in a cyber competition I tried back in 2018 or so. The environment had a web server in it with a very basic HTML tree pointing towards 1000+ "account" directories, each with a .sha1 file containing a cryptographic hash for that particular "account holder" on that server. The account holders were supposedly gamblers on that site, but some were bots. You could tell an account was a bot if that account's .sha1 file could be cracked to 000, 0000, or 00000. My job was to find out how many bot accounts there were.

__ATTN:__ If you want to experience the puzzle for yourself without spoilers, take `GenFileStructure.py` (works on Windows/Linux/Mac) and run it inside an arbitrary puzzle folder on your computer. This creates 1,000 folders each with a .sha1 file containing a hash. It also creates a `SecretNum.txt` file and stores the number of bots in it to check your work!

### Goal

Create a Python script that reads in all the hashes created through `GenFileStructure.py` and outputs the number of hashes that are equal to 000, 0000, or 00000

### Learning Objectives

- Basic Python knowledge
  - Navigating file structures
  - Using the Hashlib library
- How to "crack" hashes using a rainbow table