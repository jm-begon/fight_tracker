class Speed:
    def __init__(self, speed_in_feet):
        self.in_feet = speed_in_feet

    @property
    def feet(self):
        return self.in_feet

    @property
    def meters(self):
        return int(self.in_feet * 0.3048)

    @property
    def square_grid(self):
        return self.in_feet / 5.

    def __str__(self):
        return f"{self.feet} ft./{self.meters} m/{self.square_grid} sq."
