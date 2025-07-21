import argparse
import numpy as np
import matplotlib.pyplot as plt

# Парсинг аргументов
parser = argparse.ArgumentParser(description='Построение графика функции')
parser.add_argument('file', help='Файл с данными (txt)')
parser.add_argument('--fill', action='store_true', help='Заливка под кривой')
args = parser.parse_args()

# Чтение данных
x, y = [], []
with open(args.file, 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 2:
            x.append(float(parts[0]))
            y.append(float(parts[1]))

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=1.5, label='f(x)')
plt.title('График функции')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

if args.fill:
    plt.fill_between(x, y, color='skyblue', alpha=0.4)

plt.legend()
plt.show()
