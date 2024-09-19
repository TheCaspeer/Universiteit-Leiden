from datetime import datetime
timestamp = datetime.now()
print(timestamp.strftime("%Y-%m-%d-%H%M%S"))

filename = f'data {timestamp.strftime("%Y-%m-%d-%H%M%S")}'


print(filename)
