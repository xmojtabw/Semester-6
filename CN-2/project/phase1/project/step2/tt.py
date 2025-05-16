

class Pizza:
    
    def __init__(self, ingredients):
        self.ingredients = ingredients

    @classmethod
    def margherita(cls):
        return cls(["cheese", "tomato"])

class dad:
    def __init__(self,*args, **kwargs):
        print(self.ali())
        self.c = "boom"
        self.build(*args, **kwargs)

    def build(self, *args, **kwargs):
        print("1")
        pass 
    
    
class sun(dad):
    def build(self, *args, **kwargs):
        print("2")
        self.b = args[0]
          
          
    def __str__(self):
        return str(self.c)
    
    def ali(self):
        return "hi"

p = Pizza.margherita()
print(p.ingredients)  # ['cheese', 'tomato']


b = sun(4)
print(b.__class__)
print(b)