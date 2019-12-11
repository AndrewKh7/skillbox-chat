
class User:
    first_name: str
    last_name: str

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name 

    def fullName(self):
        # return " ".join((self.first_name,self.last_name))
        return f"Full name: {self.first_name} {self.last_name}"

john = User("John","Doe")
Artur = User("Artur","Doe")

print(john.fullName())
print(Artur.fullName())

