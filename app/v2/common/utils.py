from datetime import date

# https://stackoverflow.com/questions/2217488/age-from-birthdate-in-python
def age_from_birt_date(birth_date):
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
