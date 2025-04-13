class GoodDog:

    def __init__(self, name):
        self.name = name
        print(f'Constructor for {self.name}')

    def speak(self):
        print(f'{self.name} says Woof!')

    def roll_over(self):
        print(f'{self.name} is rolling over.')

clover = GoodDog('Clover')
clover.speak()
clover.roll_over()

caroline = GoodDog('Caroline')
caroline.speak()
caroline.roll_over()
