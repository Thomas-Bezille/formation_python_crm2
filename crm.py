from dataclasses import dataclass


@dataclass
class User:
    first_name: str
    last_name: str
    phone_number: str = ""
    address: str = ""
    
    def __repr__(self) -> str:
        return f"User({self.first_name}, {self.last_name})"
    
    def __str__(self) -> str:
        return f"{self.full_name} - tel: {self.phone_number} - address: {self.address}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


if __name__ == "__main__":
    from faker import Faker
    fake = Faker(locale="fr_FR")
    
    for _ in range(10):
        user = User(fake.first_name(),
                    fake.last_name(),
                    fake.phone_number(),
                    fake.address())
        print(user)
        print("-" * 20)