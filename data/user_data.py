from dataclasses import dataclass, asdict
import faker


VALID_USER_EMAIL = "eve.holt@reqres.in"
VALID_USER_PASSWORD = "pistol"
EXISTING_USER_ID = 2
NON_EXISTENT_USER_ID = 999

fake = faker.Faker()

@dataclass
class UserData:
    name: str
    email: str
    job: str
    password: str

    def as_dict(self):
        return asdict(self)

def fake_data_user() -> UserData:
    return UserData(
        name = fake.first_name(),
        email = f'{fake.email()[0:5]}@gmail.com',
        job = fake.job(),
        password = fake.password()
    )