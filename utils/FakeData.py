from datetime import datetime

from faker import Faker
from mimesis import Person, Address, Datetime
from mimesis.enums import Gender
from mimesis.locales import Locale


def generate_fake_data_faker(cantidad: int) -> list[dict]:
    fake = Faker()
    birthday = fake.date_of_birth()
    #age = datetime.now() - birthday
    data = [{
        "name": fake.name(),
        "sex": fake.random_element(["M", "F"]),
        "birthday": birthday.strftime("%Y-%m-%d"),
        #"age": age,
        "job": fake.job(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "country": fake.country()
    } for _ in range(cantidad)]
    return data


def generate_fake_data_mimesis(cantidad: int) -> list[dict]:
    person = Person(locale=Locale.ES)
    address = Address(locale=Locale.ES)
    data = []
    for _ in range(cantidad):
        sexo = Gender.MALE if person.gender() == 'M' else Gender.FEMALE
        #birthday
        birthday = Datetime(locale=Locale.ES)
        #edad = datetime.now().year - birthday.year()
        registro = {
            "name": person.full_name(),
            "sex": sexo.name,  # Convertir a nombre completo (e.g., 'MALE' -> 'Masculino')
            "birthday": birthday.date(),
            #"age": edad,
            "job": person.occupation(),
            "email": person.email(),
            "phone": person.telephone(),
            "address": address.address(),
            "country": address.country()
        }
        data.append(registro)
    return data

def generate_fake_data(cantidad: int, tipo_generador: str) -> list[dict]:
    if tipo_generador == "faker":
        return generate_fake_data_faker(cantidad)
    if tipo_generador == "mimesis":
        return generate_fake_data_mimesis(cantidad)
    raise ValueError("Tipo de generador no soportado")