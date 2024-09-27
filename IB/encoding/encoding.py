with open('python\IB\encoding\data.txt', encoding='utf-8') as f:
    text = f.read()


with open('python\IB\encoding\key_vizener.txt', encoding='utf-8') as f:
    key_viz = f.read()


with open('python\IB\encoding\keyVP.txt', encoding='utf-8') as f:
    key_vp = f.read()


alp = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'

ans = ""
rot_cesr = 35


#Расшифровка виженера_________________________________________
alp_viz = 'аАбБвВгГдДеЕжЖзЗиИйЙкКлЛмМнНоОпПрРсСтТуУфФхХцЦчЧшШщЩъЬыЫьЪэЭюЮяЯ'


for i in range(len(text)):
    char = text[i]
    if char not in alp:
        ans += char
    else:
        key_char = key_viz[i % len(key_viz)]
        key_idx = alp.index(key_char)
        char_idx = alp.index(char)
        new_idx = (char_idx - key_idx) % len(alp)
        ans += alp[new_idx]




#Расшифровка VP_________________________________________________
def decrypt_vertical_permutation(ciphertext, key):
    # Преобразуем ключ в список чисел
    key_list = list(map(int, key.split()))
    # Разбиваем шифртекст на блоки по длине ключа
    blocks = [ciphertext[i:i+len(key_list)] for i in range(0, len(ciphertext), len(key_list))]
    # Добавляем пробелы в конец блоков для удобства
    blocks = [block + ' ' * (len(key_list)-len(block)) for block in blocks]
    # Транспонируем блоки, чтобы получить исходный текст
    transposed_blocks = [''.join([block[i] for block in blocks]) for i in range(len(key_list))]
    # Сортируем ключ по возрастанию и переставляем блоки в соответствующем порядке
    sorted_key = sorted(list(enumerate(key_list)), key=lambda x: x[1])
    plaintext = ''.join([transposed_blocks[i] for i, k in sorted_key]).replace('_', ' ')
    return plaintext