import json

class Boolexp(object):
    def __init__(self, filename = "input.json"):
        self.data = json.load(open("input.json", 'r'))
        self.exp_length = len(self.data)
    
    @property
    def length(self):
        return self.exp_length
    
    def yield_exp(self):
        for key, data in self.data.items():
            yield (key, data[0])

if __name__ == "__main__":
    a = Boolexp()
    # print(a.j_file)
    p = a.yield_exp()
    # print(type(a.data))
    for i in range (a.length):
        print(next(p))
    