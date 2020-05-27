class Car:
    # Defining the constants we want to use with the car here.
    METRES_IN_MILE = 1609.34

    def __init__(self, colour, make, top_speed_mph):
        """
        Here we define what makes up a car, and what we want to be exposed to the user so they can change it.
        :param colour: the colour of the car the user wants to choose
        :param make: the make of the car
        :param top_speed_mph: the top speed of the car in mph
        """
        self.colour = colour
        self.make = make
        self.top_speed_mph = top_speed_mph
        self.top_speed_ms = self.top_speed_ms()
        self.distance_travelled = 0

    def top_speed_ms(self):
        """
        Calculating the top speed of our car in metres per second instead of mph for calculations
        :return: the top speed in metres per second
        """
        return self.top_speed_mph * self.METRES_IN_MILE / 60**2

    def drive(self, time_to_drive):
        """
        This function "drives" like a car. Given a specific time, it drives at the top speed of the vehicle.
        :param time_to_drive: the amount of time to drive for
        """
        self.distance_travelled += time_to_drive * self.top_speed_ms


# Defining our two cars and adding them to an array of all the cars
Car1 = Car("blue", "Vauxhall", 65)
Car2 = Car("red", "Ferrari", 120)
Cars = [Car1, Car2]

# Driving each of our cars for 10 seconds (or whatever you'd like) to compare the distances they travel.
time_to_drive_sec = 10
for car in Cars:
    car.drive(time_to_drive_sec)
    print(f"In {time_to_drive_sec} seconds, the {car.colour} {car.make} travels {int(car.distance_travelled)}m at top speed of {car.top_speed_mph} mph.")
