class Calc:
    def __init__(self, base_size):
        self.base_size = base_size

    def calc_loop(self):
        rem_target = ""
        while rem_target != 'n':
            rem_target = self.get_px()
            self.print_calc(self.calculate(rem_target))

    def calculate(self, px):
        rem = (float(px) / float(self.base_size))

        return rem

    def calculate_inverse(self, rem):
        rem = int((float(rem) * float(self.base_size)))

        return rem

    @staticmethod
    def print_calc(value, method):
        if method == 'rem':
            print(f'{value}rem')
        elif method == 'px':
            print(f'{value}px')

    @staticmethod
    def get_px():
        px = input('Enter target pixel:\n')

        return px
