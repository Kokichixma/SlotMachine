# Lošimo automatas "SlotMachine"

## Įvadas

### 1. Kokia tai programa?

Tai yra konsolinis lošimo automato "Slot Machine" žaidimas. Žaidimo pradžioje žaidėjas pasirenka vieną iš dviejų automatų tipų – Regular arba High Stakes – tiesiog pažymėdamas nenorimą komentaru su simboliu `#`. Veikimo principas grindžiamas atsitiktinumo generavimu ir tam tikra struktūrizuota lošimo logika. Žaidėjui yra suteikta galimybė įvesti sumą iš kurios bus lošiama. Sukimo metu būgnai sustos ir bus rodomi atsitiktiniai simboliai. Nepaisant "Slot Machine" pasirinkimo bus 7 simboliai (CHERRY, ORANGE, PLUM, LEMON, BELL, BAR, SEVEN) kurių vertė kyla iš kairės į dešinę, išskyrus vienu atveju, nes PLUM lygus LEMON. Laimėjimai apskaičiuojami remiantis iš anksto numatytais algoritmais. Žaidimas gali būti tęsiamas iki tol kol yra patenkinamos žaidimo sąlygos t.y. netikrų skaitmeninių pinigų. P.s. Žaidimas neskatina lošimo, bandymai rodė, kad žaidėjas nebus linkęs laimėti.

### 2. Kaip paleisti ir naudoti programą?

1. Pasirinkite automato tipą:
   Regular Slot Machine (galima įvesties vertė nuo 1 iki 50).
   High Stakes Slot Machine (galima įvesties vertė nuo 50 iki 500).
   Tuomet nenorimą aparatą kodo apačioje (iki kol prasideda testavimo sekcija - `class TestWheel(unittest.TestCase):`) pažymėkite komentaru su simboliu `#`.
   
2. Įrašykite kodą į failą, pvz., `SlotMachine.py`.

3. Terminale arba komandų eilutėje paleiskite šį scenarijų:
```
python SlotMachine.py
```
4. Vykdykite nurodymus:
   **Įveskite `y/n` priklausomai ar norite žaisti.**
   **Įvedę `y` įrašykite sumą iš kurios bus lošiama.**

Norėdami paleisti unit testus:
```
python SlotMachine.py test
```
### 3. Žaidimo taisyklės:
```
| CHERRY | = $2
| CHERRY | CHERRY | = $5
| CHERRY | CHERRY | CHERRY | = $7
| ORANGE | ORANGE | ORANGE arba BAR | = $10
|  PLUM  |  PLUM  |  PLUM arba BAR  | = $14
|  LEMON |  LEMON |  LEMON arba BAR | = $14
|  BELL  |  BELL  |  BELL arba BAR  | = $20
|   BAR  |   BAR  |   BAR  | = $250
|  SEVEN |  SEVEN |  SEVEN | = $500
```

## Struktūros analizė

### a. Paaiškinkite, kaip programa apima (įgyvendina) funkcinius reikalavimus (4 OOP kolonos).
  
-### Polimorfizmas
**Polimorfizmas yra pastebimas keliose vietose kur skirtingų klasių objektai gali būti naudojami pakaitomis:**

```py
class Game:
    def __init__(self, slot_machine):
        # Polimorfiškas - priima bet kokį automatą
        self.slot_machine = slot_machine

class HighStakes_SlotMachine(Regular_SlotMachine):
    def _calculate_winnings(self, first, second, third, bet_multiplier):
        # Metodo perrašymas - Polimorfizmo sąvybė
        winnings = super()._calculate_winnings(first, second, third, bet_multiplier)
        if first == "BAR" and (second == "SEVEN" or third == "SEVEN"):
            winnings += 50 * bet_multiplier
        return winnings
```

-## Abstrakcija
**Abstrakcija yra įterpta per pagrindinę SlotMachine klasę ir jos metodus:**

```py
class SlotMachine:
    def __init__(self, symbols):
        self._symbols = symbols

    def _calculate_winnings(self, first, second, third, bet_multiplier):
        # Abstrakti logika laimėjimų apskaičiavimui
        winnings = 0
        # ...laimėjimo kombinacijos logika...
        return winnings * bet_multiplier
```

-## Paveldėjimas
**Paveldėjimas yra demonstruojamas per klasės hierarchiją:**

```py
class Regular_SlotMachine(SlotMachine):
    # Paveldi iš SlotMachine
    def __init__(self, initial_balance, symbols):
        super().__init__(symbols)

class HighStakes_SlotMachine(Regular_SlotMachine):
    # Paveldi iš Regular_SlotMachine
    def __init__(self, initial_balance, symbols):
        super().__init__(initial_balance, symbols)
```

-## Inkapsuliacija
**Inkapsuliacija yra iterpta naudojant privačius kintamuosius (du apatiniai brūkšniai) ir apsaugotus metodus (vienas apatinis brūkšnys):**

```py
class Wheel:
    def __init__(self, symbols):
        self.__symbols = symbols        # Privatus kintamasis
        self.__current_symbol = None    # Privatus kintamasis

class Regular_SlotMachine(SlotMachine):
    def __init__(self, initial_balance, symbols):
        self.__balance = initial_balance    # Privatus kintamasis
        self.__wheel1 = Wheel(symbols)      # Privatus kintamasis
        
    def _display_outcome(self, first, second, third, win):
        # Apsaugotas metodas
        if win > 0:
            print(f"{first}\t{second}\t{third} -- YOU WIN \033[92m${win}\033[0m")
```

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////



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
