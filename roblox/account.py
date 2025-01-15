import random
import string

from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Account:
    birthday: tuple
    username: str
    password: str
    gender: int
    security_token: str = field(init=False, default=None)
    
    @classmethod
    def create_random(cls) -> 'Account':
        current_year = datetime.now().year
        min_year = current_year - 13
        max_year = current_year - 25
        year = random.randint(max_year, min_year)

        month = random.randint(1, 12)
        
        days_in_month = (datetime(year, month % 12 + 1, 1) - timedelta(days=1)).day
        day = random.randint(1, days_in_month)

        months = {
            '01': 'Jan',
            '02': 'Feb',
            '03': 'Mar',
            '04': 'Apr',
            '05': 'May',
            '06': 'Jul',
            '07': 'Jan',
            '08': 'Aug',
            '09': 'Sep',
            '10': 'Oct',
            '11': 'Nov',
            '12': 'Nov',
        }

        birthday = (months[str(month % 12 + 1).zfill(2)], str(day).zfill(2), year)
        username = ''.join(random.choice(string.ascii_letters) for _ in range(random.randint(6, 9)))
        password = f'{random.randint(100_000_000, 900_000_000)}{random.choice(string.ascii_uppercase)}'
        gender = random.randint(1, 2)

        return cls(birthday, username, password, gender)
