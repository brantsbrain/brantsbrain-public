# Cracking Passwords
Author/Creator - Brant Goings

Uses a dictionary builder and a hash cracker to break hash tables.

Updates are still being made and some commands may not work as expected. See comments within files to check.

HashCracker.py does not handle salted hashes as of now.

### HashlibBasics.py
See this for a quick tutorial on using the hashlib package

### DictionaryBuilder.py
Requires a pre-defined .txt with possible passwords for a given subject (example shown below) that will then be expanded on during run time.

dict.txt (lines that begin with a hyphen are ignored)
```
---------------------------- Original Dictionary ----------------------------
password
Brant
BrantGoings
hashcracker
dog
```

Below would be the updated dict.txt after running commands 3, 4, and 5 without enforcing a minimum length. Duplicates are automatically deleted.
```
---------------------------- Original Dictionary ----------------------------
password
Brant
BrantGoings
hashcracker
dog
---------------------------- Exhaustively Combining Original Passwords ----------------------------
passwordBrant
passwordBrantBrantGoings
passwordBrantBrantGoingshashcracker
passwordBrantBrantGoingshashcrackerdog
dogpassword
dogpasswordBrant
dogpasswordBrantBrantGoings
dogpasswordBrantBrantGoingshashcracker
hashcrackerdog
hashcrackerdogpassword
hashcrackerdogpasswordBrant
hashcrackerdogpasswordBrantBrantGoings
---------------------------- Swapping a For @ ----------------------------
p@ssword
Br@nt
Br@ntGoings
h@shcr@cker
p@sswordBr@nt
p@sswordBr@ntBr@ntGoings
p@sswordBr@ntBr@ntGoingsh@shcr@cker
p@sswordBr@ntBr@ntGoingsh@shcr@ckerdog
dogp@ssword
dogp@sswordBr@nt
dogp@sswordBr@ntBr@ntGoings
dogp@sswordBr@ntBr@ntGoingsh@shcr@cker
h@shcr@ckerdog
h@shcr@ckerdogp@ssword
h@shcr@ckerdogp@sswordBr@nt
h@shcr@ckerdogp@sswordBr@ntBr@ntGoings
---------------------------- Swapping s For $ ----------------------------
pa$$word
BrantGoing$
ha$hcracker
pa$$wordBrant
pa$$wordBrantBrantGoing$
pa$$wordBrantBrantGoing$ha$hcracker
pa$$wordBrantBrantGoing$ha$hcrackerdog
dogpa$$word
dogpa$$wordBrant
dogpa$$wordBrantBrantGoing$
dogpa$$wordBrantBrantGoing$ha$hcracker
ha$hcrackerdog
ha$hcrackerdogpa$$word
ha$hcrackerdogpa$$wordBrant
ha$hcrackerdogpa$$wordBrantBrantGoing$
p@$$word
Br@ntGoing$
h@$hcr@cker
p@$$wordBr@nt
p@$$wordBr@ntBr@ntGoing$
p@$$wordBr@ntBr@ntGoing$h@$hcr@cker
p@$$wordBr@ntBr@ntGoing$h@$hcr@ckerdog
dogp@$$word
dogp@$$wordBr@nt
dogp@$$wordBr@ntBr@ntGoing$
dogp@$$wordBr@ntBr@ntGoing$h@$hcr@cker
h@$hcr@ckerdog
h@$hcr@ckerdogp@$$word
h@$hcr@ckerdogp@$$wordBr@nt
h@$hcr@ckerdogp@$$wordBr@ntBr@ntGoing$
---------------------------- Swapping i For 1 ----------------------------
BrantGo1ngs
passwordBrantBrantGo1ngs
passwordBrantBrantGo1ngshashcracker
passwordBrantBrantGo1ngshashcrackerdog
dogpasswordBrantBrantGo1ngs
dogpasswordBrantBrantGo1ngshashcracker
hashcrackerdogpasswordBrantBrantGo1ngs
Br@ntGo1ngs
p@sswordBr@ntBr@ntGo1ngs
p@sswordBr@ntBr@ntGo1ngsh@shcr@cker
p@sswordBr@ntBr@ntGo1ngsh@shcr@ckerdog
dogp@sswordBr@ntBr@ntGo1ngs
dogp@sswordBr@ntBr@ntGo1ngsh@shcr@cker
h@shcr@ckerdogp@sswordBr@ntBr@ntGo1ngs
BrantGo1ng$
pa$$wordBrantBrantGo1ng$
pa$$wordBrantBrantGo1ng$ha$hcracker
pa$$wordBrantBrantGo1ng$ha$hcrackerdog
dogpa$$wordBrantBrantGo1ng$
dogpa$$wordBrantBrantGo1ng$ha$hcracker
ha$hcrackerdogpa$$wordBrantBrantGo1ng$
Br@ntGo1ng$
p@$$wordBr@ntBr@ntGo1ng$
p@$$wordBr@ntBr@ntGo1ng$h@$hcr@cker
p@$$wordBr@ntBr@ntGo1ng$h@$hcr@ckerdog
dogp@$$wordBr@ntBr@ntGo1ng$
dogp@$$wordBr@ntBr@ntGo1ng$h@$hcr@cker
h@$hcr@ckerdogp@$$wordBr@ntBr@ntGo1ng$
```

### HashCracker.py
Requires a hash table (from a shadow file for example) and a dictionary file (from DictionaryBuilder.py for example) to crack hashes. This program is very similar to John the Ripper.

hash.txt (again, lines that begin with a hyphen are ignored)
```
----- SHA256
2f60cc017038f16577b36e840233917b400ac62d4949bf8084dd1b2bf55cb82b
17E2AEE69F56F70FB2BA32928FCD6A3527575F9A94BCA8E93F92778E3F0524E7
BBA216AC1809E5DBEB0B1FA2652D68D6B98F0E228D012E316752CB918AA03116
0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e
----- MD5
4cfec6ac15c56014472852bec92321cb
34cc93ece0ba9e3f6f235d4af979b16c
5f4dcc3b5aa765d61d8327deb882cf99
7808a010a9fae8247caa04f05afe3b0e
----- SHA512
AE7AFBC9B4361E78C65B74B3B7BF0416263609AE5ABB16CE352CD54AD9AE6211883A57F83038B178675D5103CA277FEEEC3DA4D296E3B1C53B1B17CCFFF16D02
7FD3221EF8148D04D9A5451741E5ED598454BAEF85590B6515A12352EA0910B471D86BA58CDC14811DADAF4D7EB1B5F8A23404166EAA6348A07E1ABF00BB879A
```

Below takes in hashes from the above hash.txt and lines from the DictionaryBuilder.py example above and cracks using MD5, SHA256, and SHA512.
```
MD5 hash cracked -- 5f4dcc3b5aa765d61d8327deb882cf99 : password
MD5 hash cracked -- 7808a010a9fae8247caa04f05afe3b0e : br@ntgoings
SHA512 hash cracked -- 7fd3221ef8148d04d9a5451741e5ed598454baef85590b6515a12352ea0910b471d86ba58cdc14811dadaf4d7eb1b5f8a23404166eaa6348a07e1abf00bb879a : Br@ntGo1ng$
```
