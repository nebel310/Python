

with open('python\IB\zener\data.txt', 'r', encoding='utf-8') as file:
    data = file.read()
    
with open('python\IB\zener\key.txt', 'r', encoding='utf-8') as file:
    key = file.read()

alp = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

ans = ''
key_index = 0

for char in data:
    if char not in alp:
        ans += char
    else:
        if char.isupper():
            index = key.upper().find(char.upper())
            if index == -1:
                ans += char
            else:
                ans += alp[(index + alp.find(char.lower())) % len(alp)].upper()
        else:
            index = key.find(char.lower())
            if index == -1:
                ans += char
            else:
                ans += alp[(index + alp.find(char)) % len(alp)]
            key_index = (key_index + 1) % len(key)

print(ans)
