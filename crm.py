import re
import string

from dataclasses import dataclass
from tinydb import TinyDB, where
from typing import ClassVar, List
from pathlib import Path


@dataclass
class User:
    DB: ClassVar[TinyDB] = TinyDB(Path(__file__).resolve().parent / "db.json", indent=4)
    
    first_name: str
    last_name: str
    phone_number: str = ""
    address: str = ""
    
    def __repr__(self) -> str:
        return f"User({self.first_name}, {self.last_name})"
    
    def __str__(self) -> str:
        return f"{self.full_name} - tel: {self.phone_number} - address: {self.address}"
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def find_user(self):
        return User.DB.get((where("first_name") == self.first_name) & (where("last_name") == self.last_name))
    
    def _check_phone_number(self):
        phone_number = re.sub(r"[+()\s]*", "", self.phone_number)
        if len(phone_number) < 10 or not phone_number.isdigit():
            raise ValueError(f"Numéro de téléphone {self.phone_number} invalide.")
    
    def _check_names(self):
        special_characters = string.punctuation + string.digits
        
        if not (self.first_name and self.last_name):
            raise ValueError("Le prénom et le nom de famille ne peuvent pas être vides.")
        
        for character in self.first_name + self.last_name:
            if character in special_characters:
                raise ValueError(f"Nom invalide {self.full_name}")
    
    def _checks(self):
        self._check_phone_number()
        self._check_names()
    
    def save(self, validate_data=False) -> str | None:
        if validate_data:
            self._checks()
        
        if User.DB.insert(self.__dict__):
            return "✅ Élément ajouté ✅"
    
    def exists(self) -> bool:
        return bool(self.find_user)
    
    def delete(self) -> List[int] | List[None]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.find_user.doc_id]) # type: ignore
        return []


def get_all_users():
    return [User(**user) for user in User.DB.all()]


# === TESTS ===
if __name__ == "__main__":
    from faker import Faker
    fake = Faker(locale="fr_FR")
    
    # for _ in range(10):
    #     user = User(fake.first_name(),
    #                 fake.last_name(),
    #                 fake.phone_number(),
    #                 fake.address())
    #     print(user.save(validate_data=True))
    laure = User("Laure", "Barbe")
    print(laure.delete())