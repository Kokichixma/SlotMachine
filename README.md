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

### 1. Paaiškinkite, kaip programa apima (įgyvendina) funkcinius reikalavimus (4 OOP kolonos).
  
- ### Polimorfizmas
**Polimorfizmas (tai principas, leidžiantis naudoti tą patį metodų pavadinimą skirtingose klasėse, tačiau su skirtingu elgesiu) yra pastebimas keliose vietose kur skirtingų klasių objektai gali būti naudojami pakaitomis:**

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

- ### Abstrakcija
**Abstrakcija (tai principas, kuris leidžia slėpti sudėtingą klasės veikimo logiką ir pateikti tik esminę informaciją, reikalingą objektui naudoti) yra įterpta per pagrindinę `SlotMachine` klasę ir jos metodus:**

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

- ### Paveldėjimas
**Paveldėjimas (tai principas, leidžiantis vienai klasei perimti kitos klasės savybes (kintamuosius) ir elgseną (metodus)) yra demonstruojamas per klasės hierarchiją:**

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

- ### Inkapsuliacija
**Inkapsuliacija (tai principas, kuris reiškia duomenų (kintamųjų) ir su jais susijusių veiksmų (metodų) apjungimą į vieną vienetą – klasę, bei apsaugą nuo tiesioginės prieigos iš išorės) yra iterpta naudojant privačius kintamuosius (du apatiniai brūkšniai) ir apsaugotus metodus (vienas apatinis brūkšnys):**

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

- ### Gamyklos metodo modelis
**Tai yra įterpta `SlotMachineFactory` klasėje:**

```py
  class SlotMachineFactory:
    def create_slot_machine(self, type, initial_balance, symbols):
        if type == "regular":
            return Regular_SlotMachine(initial_balance, symbols)
        elif type == "high_stakes":
            return HighStakes_SlotMachine(initial_balance, symbols)
        else:
            raise ValueError("Invalid slot machine type")
```
**Panaudotas, nes:**

- Tai apima objekto kūrimo logiką
- Jis sukuria įvairių tipų lošimo automatus pagal įvesties parametrą
- Tai leidžia lengvai išplėsti, jei reikia pridėti naujų tipų lošimo automatų
- Kliento kodas (žaidimo klasė) veikia su produktais per bendrą sąsają
 
**Panaudojimo pavyzdys kode:**

```py
factory = SlotMachineFactory()
regular_game = Game(factory.create_slot_machine("regular", 150, symbols))
high_stakes_game = Game(factory.create_slot_machine("high_stakes", 250, symbols))
```

- ### Kompozicija
**1. Kompozicija yra pastebima `Regular_SlotMachine` klasėje**

```py
class Regular_SlotMachine(SlotMachine):
    def __init__(self, initial_balance, symbols):
        super().__init__(symbols)
        self.__wheel1 = Wheel(symbols)  # Kompozicija
        self.__wheel2 = Wheel(symbols)  # Kompozicija
        self.__wheel3 = Wheel(symbols)  # Kompozicija
```
**2. Kompozicija yra pastebima `Game` klasėje**

```py
class Game:
    def __init__(self, slot_machine):
        self.slot_machine = slot_machine  # Kompozicija
```

- Dalys `Wheel` sukuriamos esančioje klasėje
- Dalys negali egzistuoti atskirai
- Dalys yra priklausomos nuo automato likimo

**Žaidimo mechanika:** Klasė `Game` tvarko pagrindinę logiką.

**Unit test:** „unittest“ modulis apžvelgia pagrindinę logiką bei patikrina ar viskas veikia taip kaip turi veikti.

```py
class TestWheel(unittest.TestCase):
    def test_spin(self):
        wheel = Wheel(["A", "B", "C"])
        result = wheel.spin()
        self.assertIn(result, ["A", "B", "C"])

    def test_get_current_symbol(self):
        wheel = Wheel(["A", "B", "C"])
        wheel.spin()
        result = wheel.get_current_symbol()
        self.assertIn(result, ["A", "B", "C"])

class TestSlotMachine(unittest.TestCase):
    def setUp(self):
        self.symbols = ["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR", "SEVEN"]
        self.slot_machine = SlotMachine(self.symbols)

    def test_calculate_winnings(self):
        self.assertEqual(self.slot_machine._calculate_winnings("CHERRY", "LEMON", "ORANGE", 1), 2)
        self.assertEqual(self.slot_machine._calculate_winnings("CHERRY", "CHERRY", "ORANGE", 1), 5)
        self.assertEqual(self.slot_machine._calculate_winnings("CHERRY", "CHERRY", "CHERRY", 1), 7)
        self.assertEqual(self.slot_machine._calculate_winnings("ORANGE", "ORANGE", "ORANGE", 1), 10)
        self.assertEqual(self.slot_machine._calculate_winnings("ORANGE", "ORANGE", "BAR", 1), 10)
        self.assertEqual(self.slot_machine._calculate_winnings("PLUM", "PLUM", "PLUM", 1), 14)
        self.assertEqual(self.slot_machine._calculate_winnings("PLUM", "PLUM", "BAR", 1), 14)
        self.assertEqual(self.slot_machine._calculate_winnings("LEMON", "LEMON", "LEMON", 1), 14)
        self.assertEqual(self.slot_machine._calculate_winnings("LEMON", "LEMON", "BAR", 1), 14)
        self.assertEqual(self.slot_machine._calculate_winnings("BELL", "BELL", "BELL", 1), 20)
        self.assertEqual(self.slot_machine._calculate_winnings("BELL", "BELL", "BAR", 1), 20)
        self.assertEqual(self.slot_machine._calculate_winnings("BAR", "BAR", "BAR", 1), 250)
        self.assertEqual(self.slot_machine._calculate_winnings("SEVEN", "SEVEN", "SEVEN", 1), 500)
        self.assertEqual(self.slot_machine._calculate_winnings("LEMON", "ORANGE", "PLUM", 1), -1)
        self.assertEqual(self.slot_machine._calculate_winnings("CHERRY", "LEMON", "ORANGE", 5), 10)
        
class TestRegularSlotMachine(unittest.TestCase):
    def setUp(self):
        self.symbols = ["CHERRY", "LEMON", "ORANGE"]
        self.initial_balance = 100
        self.slot_machine = Regular_SlotMachine(self.initial_balance, self.symbols)

    @patch('random.choice')
    def test_play_round_winning(self, mock_choice):
        mock_choice.side_effect = ["CHERRY", "CHERRY", "CHERRY"]
        bet_multiplier = 1
        self.slot_machine.play_round(bet_multiplier)
        self.assertEqual(self.slot_machine.get_balance(), self.initial_balance + 7 * bet_multiplier)

    @patch('random.choice')
    def test_play_round_losing(self, mock_choice):
        # Changed to a combination that ensures a loss
        mock_choice.side_effect = ["LEMON", "ORANGE", "CHERRY"]  
        bet_multiplier = 1
        self.slot_machine.play_round(bet_multiplier)
        # For a losing combination, winnings = -1 * bet_multiplier
        expected_balance = self.initial_balance - bet_multiplier
        self.assertEqual(self.slot_machine.get_balance(), expected_balance)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_round_invalid_bet(self, mock_stdout):
        bet_multiplier = 0
        result = self.slot_machine.play_round(bet_multiplier)
        self.assertFalse(result)
        self.assertEqual(mock_stdout.getvalue().strip(), "Bet multiplier must be greater than 0.")

    def test_get_balance(self):
        self.assertEqual(self.slot_machine.get_balance(), self.initial_balance)

class TestHighStakesSlotMachine(unittest.TestCase):
    def setUp(self):
        self.symbols = ["CHERRY", "LEMON", "ORANGE", "BAR", "SEVEN"]
        self.initial_balance = 200
        self.slot_machine = HighStakes_SlotMachine(self.initial_balance, self.symbols)

    @patch('random.choice')
    def test_calculate_winnings_high_stakes_bonus(self, mock_choice):
        mock_choice.side_effect = ["BAR", "SEVEN", "ORANGE"]
        bet_multiplier = 1
        self.slot_machine.play_round(bet_multiplier)
        # Base winnings (-1) plus high stakes bonus (50)
        expected_balance = self.initial_balance + (50 - 1) * bet_multiplier
        self.assertEqual(self.slot_machine.get_balance(), expected_balance)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_big_win_message(self, mock_stdout):
        with patch.object(HighStakes_SlotMachine, '_calculate_winnings', return_value=100):
            self.slot_machine._display_outcome("BAR", "SEVEN", "ORANGE", 100)
            self.assertIn("BIG WIN!", mock_stdout.getvalue())

class TestSlotMachineFactory(unittest.TestCase):
    def setUp(self):
        self.symbols = ["CHERRY", "LEMON", "ORANGE"]
        self.factory = SlotMachineFactory()

    def test_create_regular_slot_machine(self):
        slot_machine = self.factory.create_slot_machine("regular", 100, self.symbols)
        self.assertIsInstance(slot_machine, Regular_SlotMachine)
        self.assertEqual(slot_machine.get_balance(), 100)

    def test_create_high_stakes_slot_machine(self):
        slot_machine = self.factory.create_slot_machine("high_stakes", 200, self.symbols)
        self.assertIsInstance(slot_machine, HighStakes_SlotMachine)
        self.assertEqual(slot_machine.get_balance(), 200)

    def test_create_invalid_slot_machine(self):
        with self.assertRaises(ValueError):
            self.factory.create_slot_machine("invalid", 100, self.symbols)

if __name__ == '__main__':
    unittest.main()
```
## Rezultatai ir santrauka

### 1. Rezultatai

- Lošimo automatas "Slot Machine" buvo sėkmingai sukurtas pasinaudojant objektiniais principais.

- Unit testai padėjo išsiaiškinti problemas, todėl kodas veikia sklandžiai.

### 2. Išvados

- Problemų daug nebuvo, nes yra žaidžiama su konsole, o ne prieš kompiuterį ar tikrus žaidėjus. Buvo kilusi problema su atskirų automatų veikimu ir bėda paskirstant tam tikrą sumą simbolių algoritmams. Šis žaidimas dažniausiai neužtrunka labai ilgai, nebent yra laimima labai didelė pinigų suma kuomet tiesiog galima baigti žaidimą su `n`. 
- Manau šis kursinis įkvėpė mane užsiimti tokia veikla laisvalaikiu ir tikrai pasistengti padaryti kokybiškesnį, optimalesnį projektą. Beto padėjo pramokti Pythono kalbą.

### 3. Kaip būtų galima patobulinti savo programą?
- Galima buvo pridėti būdą kaupti bandymų rezultatus "Leaderboard" kada buvo išeita iš žaidimo su didžiausia pinigų suma.
- Galima buvo pridėti būdą kaupti istorijoje paskutinius 3 ar daugiau bandymų.
- Galima buvo pridėti profilio sistemą.
- Galima buvo sukurti GUI.


## Šaltiniai
- https://docs.github.com/en/get-started/start-your-journey/about-github-and-git
- https://docs.python.org/3/library/unittest.html
