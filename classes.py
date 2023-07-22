from collections import UserDict
from datetime import date


class Field:
    
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)
        

class Name(Field):
    ...
    

class Phone(Field):
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value: str):
        if value:
            value = value.removeprefix("+")
            if len(value) != 12 or not value.isdigit():
                try:
                    raise ValueError(f"Invalid phone format in {value}. Please use +XXXXXXXXXXXX format.")
                except ValueError as e:
                    print(f"ValueError: {e}")
            else:
                value = f"+{value}"       
                self.__value = value 

    def __str__(self):
        return f"{self.value}"


class Birthday(Field):
    
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value:str):
        if value:
            try:
                day, month, year = map(int, value.split('.'))
                self.__value = date(year, month, day)              
            except ValueError:
                 raise ValueError("Invalid birthday format. Please use dd.mm.YYYY format.")
            
    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Record:
    
    def __init__(self, name: Name, birthday: Birthday = None, phone: Phone = None) -> None:
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"
    
    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone} change to {new_phone}"
        return f"{old_phone} not present in phones of contact {self.name}"
    
    def delete_phone(self, phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)
                return f"Phone {phone} deleted from contact {self.name}."
        return f"Phone {phone} not found in contact {self.name}."
    
    def __str__(self) -> str:
        return f"{self.name} {str(self.birthday)} ({self.days_to_birthday(self.birthday)}): {', '.join(str(p) for p in self.phones)}"

    def days_to_birthday(self, birthday:date):
        if birthday:
            day, month  = map(int, str(birthday)[:5].split('.'))
            today = date.today()
            try:
                birthday = date(today.year, month, day)
            except ValueError:
                birthday = date(today.year, 3, 1)
            if birthday < today:
                try:
                    birthday = date(today.year + 1, month, day)
                except ValueError:
                    birthday = date(today.year + 1, 3, 1)
            delta = (birthday - today).days    
            return delta
        else:
            return None


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())

    def iterator(self, n):
        count = 0
        page = ""
        for record in self.data.values():
            page += (str(record)) + "\n"
            count += 1
            if count >= n:
                yield page
                count = 0
                page = ""
        if page:
            yield page