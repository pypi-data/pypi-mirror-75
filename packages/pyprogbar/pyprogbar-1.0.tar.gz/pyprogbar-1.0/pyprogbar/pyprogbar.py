import time, math, sys

class ProgressBar:
    def __init__(self, min, max, unfilled = "-", filled = '■'):
        self.min = min
        self.max = max
        self.width = max - min
        self.filled = filled
        self.unfilled = unfilled

    def update(self, val, message = ''):
        percent = val / self.width
        sys.stdout.write('\r[{0}{1}] {2}% :: {3}  '.format(self.filled * int(percent * 50), self.unfilled * (50 -  int(percent * 50)) , int(percent * 100), message))
        if val >= self.max:
            print("\n -- Finished --")

    def config(self, min = None, max = None, unfilled = "-", filled = '■'):
        self.min = min or self.min
        self.max = max or self.max
        self.unfilled = unfilled
        self.filled = filled
        self.width = self.max - self.min

    def info(self):
        print("\nMinimum: " + str(self.min))
        print("Maximum: " + str(self.max))
