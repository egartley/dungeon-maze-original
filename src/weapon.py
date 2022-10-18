class Weapon:
    def __init__(self):
        self.damage = 0
        self.sprite = None
        self.cooldown = 0
        self.in_cooldown = False
        self.range = 0


class Sword(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 10
        self.cooldown = 1
        self.range = 8


class Bow(Weapon):
    def __init__(self):
        super().__init__()
        self.damage = 15
