import hashlib

barcode = "01/12/1234"
company = barcode[:2]+"/"
user_id = barcode[3:5]+"/"
password = barcode[6:]
hashed_password = hashlib.md5(str(password).encode()).hexdigest()

print(company)
print(user_id)
print(password)
print(hashed_password)