# SlotMachine
Course work

## 1. Polymorphism
Polymorphism is present in several places where objects of different classes can be used interchangeably:

class Game:
    def __init__(self, slot_machine):
        # Polymorphic - accepts any type of slot machine
        self.slot_machine = slot_machine

class HighStakes_SlotMachine(Regular_SlotMachine):
    def _calculate_winnings(self, first, second, third, bet_multiplier):
        # Method overriding - polymorphic behavior
        winnings = super()._calculate_winnings(first, second, third, bet_multiplier)
        if first == "BAR" and (second == "SEVEN" or third == "SEVEN"):
            winnings += 50 * bet_multiplier
        return winnings

## 2. Abstraction
Abstraction is implemented through the base SlotMachine class and its methods:

class SlotMachine:
    def __init__(self, symbols):
        self._symbols = symbols

    def _calculate_winnings(self, first, second, third, bet_multiplier):
        # Abstract logic for calculating winnings
        winnings = 0
        # ...winning combinations logic...
        return winnings * bet_multiplier

3. Inheritance
Inheritance is demonstrated through the class hierarchy:

class Regular_SlotMachine(SlotMachine):
    # Inherits from SlotMachine
    def __init__(self, initial_balance, symbols):
        super().__init__(symbols)

class HighStakes_SlotMachine(Regular_SlotMachine):
    # Inherits from Regular_SlotMachine
    def __init__(self, initial_balance, symbols):
        super().__init__(initial_balance, symbols)

4. Encapsulation
Encapsulation is implemented using private variables and protected methods:

class Wheel:
    def __init__(self, symbols):
        self.__symbols = symbols        # Private variable
        self.__current_symbol = None    # Private variable

class Regular_SlotMachine(SlotMachine):
    def __init__(self, initial_balance, symbols):
        self.__balance = initial_balance    # Private variable
        self.__wheel1 = Wheel(symbols)      # Private variable
        
    def _display_outcome(self, first, second, third, win):
        # Protected method (single underscore)
        if win > 0:
            print(f"{first}\t{second}\t{third} -- YOU WIN \033[92m${win}\033[0m")

## ////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Kortų žaidimas "Karas"

## Įvadas

### a. Kokia tai programa?

Tai skaitmeninė klasikinio kortų žaidimo „Karas“ versija. Du žaidėjai (du žmonės arba vienas žmogus ir kompiuteris) žaidžia su sumaišyta standartine 52 kortų kalade. Kiekviename raunde abu žaidėjai traukia po kortą – laimi 
aukštesnė korta. Lygiųjų atveju prasideda „karas“, kurio metu traukiamos papildomos kortos, kad būtų nustatytas nugalėtojas. Žaidimas tęsiasi tol, kol išnaudojama kaladė, o žaidėjas, laimintis daugiausiai raundų, 
paskelbiamas nugalėtoju.

### b. Kaip paleisti programą?

1. Įrašykite kodą į failą, pvz., `WAR.py`.

2. Terminale arba komandų eilutėje paleiskite šį scenarijų:
```
python WAR.py
```
3. Vykdykite nurodymus, kad įvestumėte žaidėjų vardus ir pasirinktumėte, ar žaisti prieš kompiuterį.

Norėdami paleisti unit testus:
```
python WAR.py test
```

### c. Kaip naudoti programą?

Paleidus žaidimą, jūsų bus paprašyta įvesti vardus ir nurodyti, ar norite žaisti prieš kompiuterį.
- Norėdami žaisti raundą, paspauskite bet kurį klavišą (išskyrus „q“).
- Norėdami anksčiau išeiti iš žaidimo, bet kuriuo metu paspauskite „q“.
- Programa registruoja kiekvieną raundą ir rodo rezultatą.
- Rezultatai išsaugomi faile `game_results.txt`, pagal tuos rezultatus rodo paskutinius tris laimėtojus.

## Struktūros analizė

### a. Paaiškinkite, kaip programa apima (įgyvendina) funkcinius reikalavimus.
- **4 OOP kolonos:**
- Klasės `Card`, `Deck`, `Player` ir `Game` visos naudoja inkapsuliaciją(apibūdina duomenų ir metodų, kurie dirba su duomenimis, sujungimą viename vienete.).
```py
class Card:
    suits = CardFactory.suits
    values = CardFactory.values

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __repr__(self):
        return f"{self.values[self.value]} of {self.suits[self.suit]}"
 ```
- Abstrakcija(principas, kurio esmė – paslėpti klasės ar funkcijos vidines įgyvendinimo detales, o vartotojui parodyti tik esmines funkcijas.) yra `CardFactory` klasėje.
 ```py
class CardFactory:
    suits = ["spades", "hearts", "diamonds", "clubs"]
    values = [None, None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    @classmethod
    def create_card(cls, value, suit):
        return Card(value, suit)
 ```
- Paveldėjimas( leidžia kurti naujas klases (poklasius), kurios paveldi savybes ir elgseną iš esamų klasių (superklasių). Tai skatina pakartotinį kodo naudojimą ir padeda užmegzti ryšius tarp klasių.) yra naudojamas Klasėje `Player`, jis turi subklasę `ComputerPlayer`.
```py
class Player:
    def __init__(self, name):
        self.wins = 0
        self.card = None
        self.name = name

    def __str__(self):
        return self.name

class ComputerPlayer(Player):
    def __init__(self):
        super().__init__("Computer")

```
- Polymorfizmas(programavimo koncepcija, leidžianti metodui atlikti skirtingas užduotis, priklausomai nuo objekto, su kuriuo jis dirba, net jei objektai yra skirtingų tipų.) naudojamas `Card` klasėje `__lt__` ir `__gt__` operatoriuose.
```py
 def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value
```
- **Kompozicija:** `Game` klasė turi `Deck` ir `Players`, o `Deck` klasė turi `Card` objektus.
```py
class Deck:
    def __init__(self):
        self.cards = [CardFactory.create_card(value, suit) for value in range(2, 15) for suit in range(4)]
```
- **Kortų kaladės kūrimas:** `Deck` klasė, naudodama "Factory" design patern, sukuria 52 kortų kaladę ir ją sumaišo.
```py
class CardFactory:
    suits = ["spades", "hearts", "diamonds", "clubs"]
    values = [None, None, "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
```
- **Kortų palyginimai:** Klasė `Card` įgyvendina `__lt__` ir `__gt__`, kad palygintų kortelių vertes.
```py
    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value
```
- **Žaidimo mechanika:** Klasė `Game` tvarko pagrindinę logiką, įskaitant raundo eigą, rezultatų stebėjimą ir nugalėtojo nustatymą.
- **Karo logika:** Įdiegta realistiška karo mechanika – kiekvienam karo scenarijui traukiamos trys užverstos kortos ir viena užversta.
```py
 def war(self, table_cards):
        if len(self.deck.cards) < 8:
            self.logger("Not enough cards to continue war. Ending war.")
            return

        self.logger("Each player places three cards face down and one face up.")

        for _ in range(3):
            table_cards.append(self.deck.remove_card()) 
            table_cards.append(self.deck.remove_card()) 

        p1_war_card = self.deck.remove_card()
        p2_war_card = self.deck.remove_card()
        table_cards.extend([p1_war_card, p2_war_card])
        self.draw(self.p1.name, p1_war_card, self.p2.name, p2_war_card)

        if p1_war_card > p2_war_card:
            self.p1.wins += 1
            self.logger(f"{self.p1.name} wins the war and takes {len(table_cards)} cards.")
        elif p2_war_card > p1_war_card:
            self.p2.wins += 1
            self.logger(f"{self.p2.name} wins the war and takes {len(table_cards)} cards.")
        else:
            self.logger("WAR again!")
            self.war(table_cards)
```
- **Žaidėjo sąveika:** Palaiko žmonių tarpusavio arba žmonių ir kompiuterio žaidimus su dinamine įvestimi.
- **Pastovumas:** Žaidimo rezultatai registruojami byloje, kad būtų galima juos saugoti.
- **Unit test:** „unittest“ modulis apžvelgia pagrindinę logiką: kortų palyginimą, kaladės dydį ir nugalėtojo nustatymą.

```py
class TestCard(unittest.TestCase):
    def test_card_comparison(self):
        c1 = Card(10, 2) 
        c2 = Card(11, 1) 
        self.assertTrue(c2 > c1)
        self.assertFalse(c1 > c2)
        self.assertTrue(c1 == Card(10, 0)) 

    def test_deck_size(self):
        deck = Deck()
        self.assertEqual(len(deck.cards), 52)

    def test_winner_determination(self):
        game = Game(name1="Mykolas", name2="Simonas", use_computer=False, logger=lambda *args: None)
        game.p1.wins = 3
        game.p2.wins = 1
        self.assertEqual(game.determine_winner(), "Mykolas")
        game.p1.wins = 2
        game.p2.wins = 2
        self.assertEqual(game.determine_winner(), "It was a tie!")
```
## Rezultatai ir santrauka

### a. Rezultatai

- Kortų žaidimas „Karas“ buvo sėkmingai įgyvendintas naudojant objektinius principus, tokius kaip kompozicija, todėl kodas tapo lengvai valdomas.

- Programa teisingai tvarko žaidimą tarp dviejų žmonių žaidėjų arba žmogaus ir kompiuterio, turi kortų traukimo, nugalėtojų nustatymo ir rezultatų saugojimo funkcijas.

- Unit testai patvirtino kortų palyginimo logiką ir nugalėtojo nustatymą, padėdami patvirtinti pagrindinę žaidimo mechaniką.

- Iššūkių buvo, vienas iš jų tai žaidimo galimybę spresti kraštutinius atvejus kaip kortų pritrūkimas karo metu, vienodų kortų ištraukimo karo mechanikos padarymas.

### b. Išvados

- Pagrindinė dilema kurią turejau atlikdamas šią programą, tai kortų permaišymo mechanika. "Karas" gali būti žaidžiamas ir ne pagal taškus kaip aš padariau, tačiau pagal visas kaladės kortas. Tai reiškia, kad pasibaigus kaladėje kortoms, jau atverstos kortos būtų permaišytos ir karas žaidžiamas toliau, iki kol vienas iš žaidėjų susirinks visą kaladę. Šis žaidimo metodas užtranka tikrai ilgą laiko tarpą, ir paprasta programos demonstracija bei testavimas tikrai užtruktų ilgai ir pasidarytu greitai nuobodu. Iš pradžių nebuvau tvirtas apie pasirinkimą daryti ši žaidima tokiu metodu, tačiau pasiklausęs pažystamų, interneto ir šiaip toliau pasigilinęs į "Karo" istoriją, sužinojau, kad tokį "Karo" variantą irgi žaisdavo.
- Galų gale visas kodas veikia be nesklandumų, ir manau šis kursinis darbas, tikrai mane motivavo bandyti kurti daugiau projektų ir toliau plėtoti savo python kalbos žinias.

### c. Kaip būtų galima papildyti savo programą?
- Galima ją vizualizuoti
- Galima implementuoti pinigų ir lažybų sistemą.
- Galima padaryti permaišymo mechaniką.


## Šaltiniai
- https://docs.python.org/3/library/unittest.html
- https://refactoring.guru/design-patterns/python
- https://www.freecodecamp.org/news/python-import-from-file-importing-local-files-in-python/
- https://www.w3schools.com/python/default.asp
- https://docs.github.com/en/get-started/start-your-journey/about-github-and-git
