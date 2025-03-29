class InputText() : 
    input_pos = 0
    def __init__(self,file_name:str):
        with open(file_name,'r') as file:
            self.input_text = file.read()
    
    def getchar(self):
        try:
            c = self.input_text[self.input_pos]
        except IndexError :
            raise EOFError
        self.input_pos += 1
        return  c 

    def retract(self):
        self.input_pos -= 1 




it = InputText('input.txt')
while True:
    try :
        print(it.getchar(),end='')
    except EOFError:
        break
    





