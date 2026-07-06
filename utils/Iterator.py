class InternID:
    def __init__(self):
        self.num = 1

    def __iter__(self):
        return self

    def __next__(self):
        val = f"TES{self.num:03d}"
        self.num += 1
        return val