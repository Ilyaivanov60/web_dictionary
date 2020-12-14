cards = [
    {'cat' : 'кот'},
    {'dog' : 'собака, пес'},
    {'car' : 'автомобиль, машина'},
    {'bag' : 'сумка, мешок'},
    {'bed' : 'кровать, постель}'},
    {'box' : 'коробка, ящик'},
    {'bottle' : 'бутылка'},
    {'bank' : 'банк'},
    {'book' : 'книга'}
    ]

print(cards)

#word = input('слово ')
login = "yas"
user_name = 'Max'

def word_add(word):

    if type(word) is int:
        print('Слово должно быть написано буквами')

    elif login == 'yas':
        person = {'user_name' : user_name}
        cards.append(person)

    for seach in cards:
        if word in seach:
            seach.get(word)
            print(seach.get(word))
            break

    else:
        if type(word) is not int:
            translation_word = input('перевод ')
            new_word = {word : translation_word}
            cards.append(new_word)

                
            

p = word_add('book')
print(p)
print(cards)