from random import shuffle
import sys
sys.stdout.reconfigure(encoding='utf-8')


def carte_to_chaine(card):
    color = chr(9824)
    if card['color'] == 'H':
        color = chr(9825)
    if card['color'] == 'D':
        color = chr(9826)
    if card['color'] == 'C':
        color = chr(9827)
    # if card['value'] == '10':
    #    return card['value'] + card['color']
    # else:
    #    return ' ' + card['value'] + card['color']
    return card['value'] + color


def display_deck(deck):
    for i in range(len(deck)):
        print(carte_to_chaine(deck[i]), end=" ")
    print('\n')


def deck_from_file(filename):
    deck = []
    with open(filename) as f:
        word = f.read().split()
        for item in word:
            card = dict()
            if len(item) == 3:
                card['value'] = item[0]
                card['color'] = item[2]
            else:
                card['value'] = item[0:2]
                card['color'] = item[3]
            deck.append(card)
    return deck


def deck_to_file(filename, deck):
    with open(filename, 'w') as f:
        for item in deck:
            f.write(item['value'] + '-' + item['color'] + ' ')


def make_deck(full_deck=False, shuffle_deck=True):
    values = ['7', '8', '9', '10', 'V', 'D', 'R', 'A']
    if full_deck:
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'V', 'D', 'R', 'A']
    colors = ['S', 'H', 'D', 'C']
    deck = []
    for i in range(len(values)):
        for j in range(len(colors)):
            carte = dict()
            carte['value'] = values[i]
            carte['color'] = colors[j]
            deck.append(carte)
    if shuffle_deck:
        shuffle(deck)
    return deck


def alliance(card1, card2):
    value1 = card1['value']
    color1 = card1['color']
    value2 = card2['value']
    color2 = card2['color']
    if (value1 == value2) or (color1 == color2):
        return True
    else:
        return False


def jump_possible(stack, card_number):
    if card_number >= len(stack):
        return False
    elif card_number < 2:
        return False
    else:
        card1 = stack[card_number - 2]
        card2 = stack[card_number]
        if alliance(card1, card2):
            stack[card_number - 2] = stack[card_number - 1]
            del(stack[card_number - 1])
            return True
        else:
            return False


def play_step(stack, deck, display=False):
    stack.append(deck[0])
    if display:
        display_deck(stack)
    del(deck[0])
    jump = jump_possible(stack, len(stack) - 1)
    if jump and display:
        display_deck(stack)
    while jump and len(stack) > 2:
        for i in range(2, len(stack)):
            jump = jump_possible(stack, i)
            if jump:
                if display:
                    display_deck(stack)
                break


def auto_play(deck, display=False):
    stack = deck[0:3]
    del(deck[0:3])
    display_deck(stack)
    while len(deck) > 0:
        play_step(stack, deck, display)
    return stack


def menu():
    print('1. Add a card to the stack')
    print('2. Make a jump')
    print('3. End the game automatically')
    print('4. Quit')
    choice = input('Your choice: ')
    return choice


def ask_jump(stack):
    print('Which card do you want to jump with?')
    for i in range(len(stack)):
        print(str(i + 1) + '. ' + carte_to_chaine(stack[i]), end=' | ')
    choice = int(input('\nYour choice: '))
    return choice


def manual_game(deck, max_cards=5):
    stack = deck[0:3]
    del(deck[0:3])
    display_deck(stack)
    while len(deck) > 0:
        choice = menu()
        if choice == '1':
            stack.append(deck[0])
            del(deck[0])
            display_deck(stack)
        elif choice == '2':
            choice = ask_jump(stack)
            if jump_possible(stack, choice):
                display_deck(stack)
            else:
                print('Impossible jump')
        elif choice == '3':
            stack = auto_play(deck, True)
            break
        elif choice == '4':
            break
    if len(stack) > max_cards:
        print('You lose')
    else:
        print('You win')
    return stack
