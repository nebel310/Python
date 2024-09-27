alp = "абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"

def vigenere_encrypt(text, key):
    ans = ""
    for i in range(len(text)):
        char = text[i]
        if char not in alp:
            ans += char
        else:
            key_char = key[i % len(key)]
            key_idx = alp.index(key_char)
            char_idx = alp.index(char)
            new_idx = (char_idx - key_idx) % len(alp)
            ans += alp[new_idx]
    return ans

ans = ""
with open('python\IB\zener\data.txt', 'r', encoding='utf-8') as file:
    text = file.read()
    
with open('python\IB\zener\key.txt', 'r', encoding='utf-8') as file:
    key = file.read()

with open('python\IB\zener\output.txt', 'w') as f:
    output = f.write(ans)