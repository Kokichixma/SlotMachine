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

