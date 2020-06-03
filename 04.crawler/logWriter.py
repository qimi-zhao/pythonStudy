import sys

class logWriter():
    
    def write(self, astr):
        self.lf = open(r'./log.txt', 'a')

        try:
            self.lf.write(astr)
        except ConnectionError:
            print('connect Default')

        self.lf.close()