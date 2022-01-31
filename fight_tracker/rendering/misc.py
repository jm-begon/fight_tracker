class HPBar:
    def __init__(self, hp, hp_max):
        self.hp = hp
        self.hp_max = hp_max

    def __str__(self):
        return f"{self.hp}/{self.hp_max}"
