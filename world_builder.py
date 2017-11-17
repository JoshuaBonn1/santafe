import random

name = 'dense_'
for i in range(1, 2):
    file_name = name + 'test' + '.txt'
    f = open(file_name, 'w')
    for _ in range(0, 32):
        for _ in range(0, 32):
            char = random.choice(('0', '1'))
            f.write(char)
        f.write('\n');
    f.close()

name = 'moderate_'
for i in range(1, 2):
    file_name = name + 'test' + '.txt'
    f = open(file_name, 'w')
    for _ in range(0, 32):
        for _ in range(0, 32):
            char = random.choice(('0', '0', '0', '1'))
            f.write(char)
        f.write('\n');
    f.close()

name = 'sparse_'
for i in range(1, 2):
    file_name = name + 'test' + '.txt'
    f = open(file_name, 'w')
    for _ in range(0, 32):
        for _ in range(0, 32):
            char = random.choice(('0', '0', '0', '0', '0', '0', '0', '0', '0', '1'))
            f.write(char)
        f.write('\n');
    f.close()