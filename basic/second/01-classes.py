

class User:
    first_name: str
    last_name: str

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name 

    def fullName(self):
        # return " ".join((self.first_name,self.last_name))
        return f"Full name: {self.first_name} {self.last_name}"

    def show_age(self):
        print("I have'n age!")
class AgedUser(User):
    __age: int

    def __init__(self, first_name, last_name, age):
        super().__init__(first_name, last_name)
        self.__age = age

    def fullName(self):
        return f"{super().fullName()}, {self.__age}"

    def show_age(self):
        return self.__age


aged_jhon = AgedUser("Jhom", "Due", 15)
artur = User("Artur","Due")


print(aged_jhon.fullName())
