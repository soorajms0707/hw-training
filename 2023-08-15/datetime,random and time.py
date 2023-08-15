# import datetime

# current= datetime.datetime.now()
# print(current)

# current_date = datetime.date.today()
# print(current_date)

# date = datetime.date(2023, 8, 14)
# print(date)

# datetime = current.strftime('%Y-%m-%d %H:%M:%S')
# print(datetime)


import time

# time = time.time()
# print(time)


# time.sleep(10)
# print("Done waiting.")

# timee= time.time()
# struct_time = time.localtime(timee)
# print(struct_time)

import random


integer= random.randint(1, 10)
print(integer)


float = random.random()
print(float)


range = random.uniform(2.5, 5.5)
print(range)


fruits = ['apple', 'banana', 'orange']
fruit = random.choice(fruits)
print(fruit)


shuffled= random.sample(fruits, len(fruits))
print(shuffled)

random.shuffle(fruits)
print(fruits)


