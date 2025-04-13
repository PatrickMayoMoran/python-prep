class Car:

    def __init__(self, model, year, color):
        self.model = model
        self.year = year
        self.color = color
        self.speed = 0

    def engine_on(self):
        print('Car is on!')

    def engine_off(self):
        print('Car is off!')

    def accelerate(self, speed):
        if self.speed == 100:
            print("Can't go any faster - already going 100 mph!")
        elif speed <= 0:
            print("Can't accelerate to that speed - maintaining previous speed")
        elif speed > 0 and self.speed + speed <= 100:
            self.speed += speed
            print(f'Car is now going {self.speed} miles per hour.')
        elif self.speed + speed > 100:
            self.speed = 100
            print(f"That's too fast! Car speeding up to 100 instead")

    def brake(self):
        print(f'Braking! Car is stopped.')
        self.speed = 0

    def current_speed(self):
        print(f'This car is going {self.speed} miles per hour.')

mocha = Car('CRV', 2011, 'maroon')
mocha.engine_on()
mocha.accelerate(45)
mocha.accelerate(45)
mocha.current_speed()
mocha.accelerate(45)
mocha.current_speed()
mocha.brake()
mocha.current_speed()
mocha.engine_off()
