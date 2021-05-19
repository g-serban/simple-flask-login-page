import string
import random  # define the random module


n = 50
num = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
dash_value = f'/{num}/'

print(dash_value)

