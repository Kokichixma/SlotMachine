import unittest
from unittest.mock import patch
import io
import random

class Wheel:
    def __init__(self, symbols):
        self.__symbols = symbols
        self.__current_symbol = None

    def spin(self):
        self.__current_symbol = random.choice(self.__symbols)
        return self.__current_symbol

    def get_current_symbol(self):
        return self.__current_symbol

class SlotMachine:
    def __init__(self, symbols):
        self._symbols = symbols

    def _calculate_winnings(self, first, second, third, bet_multiplier):
        winnings = 0
        if (first == "CHERRY") and (second != "CHERRY"):
            winnings = 2
        elif (first == "CHERRY") and (second == "CHERRY") and (third != "CHERRY"):
            winnings = 5
        elif (first == "CHERRY") and (second == "CHERRY") and (third == "CHERRY"):
            winnings = 7
        elif (first == "ORANGE") and (second == "ORANGE") and (third in ["ORANGE", "BAR"]):
            winnings = 10
        elif (first == "PLUM") and (second == "PLUM") and (third in ["PLUM", "BAR"]):
            winnings = 14
        elif (first == "LEMON") and (second == "LEMON") and (third in ["LEMON", "BAR"]):
            winnings = 14
        elif (first == "BELL") and (second == "BELL") and (third in ["BELL", "BAR"]):
            winnings = 20
        elif (first == "BAR") and (second == "BAR") and (third == "BAR"):
            winnings = 250
        elif (first == "SEVEN") and (second == "SEVEN") and (third == "SEVEN"):
            winnings = 500
        else:
            winnings = -1

        return winnings * bet_multiplier
    
class Regular_SlotMachine(SlotMachine):
    def __init__(self, initial_balance, symbols):
        super().__init__(symbols)
        self.__balance = initial_balance
        self.__wheel1 = Wheel(symbols)
        self.__wheel2 = Wheel(symbols)
        self.__wheel3 = Wheel(symbols)

    def play_round(self, bet_multiplier):
        if bet_multiplier <= 0:
            print("Bet multiplier must be greater than 0.")
            return False

        first_symbol = self.__wheel1.spin()
        second_symbol = self.__wheel2.spin()
        third_symbol = self.__wheel3.spin()

        winnings = self._calculate_winnings(first_symbol, second_symbol, third_symbol, bet_multiplier)
        self.__balance += winnings

        self._display_outcome(first_symbol, second_symbol, third_symbol, winnings)
        return True

    def get_balance(self):
        return self.__balance

    def _display_outcome(self, first, second, third, win):
        if win > 0:
            print(f"{first}\t{second}\t{third} -- YOU WIN \033[92m${win}\033[0m")
        else:
            print(f"{first}\t{second}\t{third} -- YOU LOSE \033[91m${abs(win)}\033[0m")

class HighStakes_SlotMachine(Regular_SlotMachine):
    def __init__(self, initial_balance, symbols):
        super().__init__(initial_balance, symbols)

    def _calculate_winnings(self, first, second, third, bet_multiplier):
        winnings = super()._calculate_winnings(first, second, third, bet_multiplier)
        if first == "BAR" and (second == "SEVEN" or third == "SEVEN"):
            winnings += 50 * bet_multiplier
        return winnings

    def _display_outcome(self, first, second, third, win):
        super()._display_outcome(first, second, third, win)
        if win > 50:
            print("BIG WIN!")

class Game:
    def __init__(self, slot_machine):
        self.slot_machine = slot_machine

    def start(self):
        print("Welcome to the Slot Machine!")
        while True:
            if self.slot_machine.get_balance() <= 0:
                print("You don't have enough money to play.")
                break

            answer = input(f"You have ${self.slot_machine.get_balance()}. Would you like to play? (yes/no): ").lower()
            if answer in ["y", "yes"]:
                while True:
                    try:
                        bet_multiplier = float(input("Enter the amount you want to play with (multiplier): "))
                        if bet_multiplier <= 0:
                            print("Please enter a value greater than 0.")
                            continue
                        break
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                if not self.slot_machine.play_round(bet_multiplier):
                    break
                print(f"Current balance: ${self.slot_machine.get_balance()}")
            elif answer in ["n", "no"]:
                print(f"Thanks for playing! You ended the game with ${self.slot_machine.get_balance()} in your hand.")
                break
            else:
                print("Wrong input!")

class SlotMachineFactory:
    def create_slot_machine(self, type, initial_balance, symbols):
        if type == "regular":
            return Regular_SlotMachine(initial_balance, symbols)
        elif type == "high_stakes":
            return HighStakes_SlotMachine(initial_balance, symbols)
        else:
            raise ValueError("Invalid slot machine type")

symbols = ["CHERRY", "LEMON", "ORANGE", "PLUM", "BELL", "BAR", "SEVEN"]
factory = SlotMachineFactory()
regular_game = Game(factory.create_slot_machine("regular", 150, symbols))
high_stakes_game = Game(factory.create_slot_machine("high_stakes", 250, symbols))

#regular_game.start()
high_stakes_game.start()

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