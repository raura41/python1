import numpy as np
import os

# Параметры функции
A = 418.9829
x_min, x_max = -500, 500
step = 0.5  # Шаг для гладкого графика

# Создание директории results
os.makedirs('results', exist_ok=True)

# Генерация данных
x_values = np.arange(x_min, x_max + step, step)
y_values = A - x_values * np.sin(np.sqrt(np.abs(x_values)))

# Сохранение в файл
with open('results/task_01_results.txt', 'w') as f:
    for x, y in zip(x_values, y_values):
        f.write(f"{x:.6f}    {y:.6f}\n")

# Построение графика (опционально для отчета)
import matplotlib.pyplot as plt
plt.plot(x_values, y_values)
plt.title('График функции: $f(x) = A - x \sin(\sqrt{|x|})$')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.savefig('results/task_01_plot.png')
plt.show()
