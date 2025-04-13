class Pet:

    def __init__(self, name):
        self.name = name
        type_name = type(self).__name__
        print(f'I am {self.name}, a {type_name}.')

class Dog(Pet):

    def speak(self):
        print(f'{self.name} says Woof!')

    def roll_over(self):
        print(f'{self.name} is rolling over!')

class Cat(Pet):

    def speak(self):
        print(f'{self.name} says Meow!')

class Parrot(Pet):

    def speak(self):
        print(f'{self.name} wants a cracker.')

sparky = Dog('Sparky')
tiny = Cat('Tiny')
polly = Parrot('Polly')

sparky.roll_over()

for pet in [sparky, tiny, polly]:
    pet.speak()
