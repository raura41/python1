import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Параметры функции
D = 2
m = 10
x10, x20 = 2.20, 1.57
step = 0.05  # Шаг для гладкого графика

# Создание сетки значений
x1 = np.arange(0, np.pi + step, step)
x2 = np.arange(0, np.pi + step, step)
X1, X2 = np.meshgrid(x1, x2)

# Вычисление функции
def f(x1, x2):
    term1 = -np.sin(x1) * (np.sin(x1**2 / np.pi))**(2*m)
    term2 = -np.sin(x2) * (np.sin(x2**2 / np.pi))**(2*m)
    return term1 + term2

Y = f(X1, X2)

# Срезы функции
y_x2_fixed = f(x1, x20)  # x2 фиксировано
y_x1_fixed = f(x10, x2)  # x1 фиксировано

# Создание окна с 4 графиками
fig = plt.figure(figsize=(16, 12))
fig.suptitle('Графики функции: $f(x_1, x_2) = - \sum_{i=1}^2 \sin(x_i) \sin^{20}\\left(\\frac{x_i^2}{\\pi}\\right)$', fontsize=16)

# 1. 3D поверхность (изометрический вид)
ax1 = fig.add_subplot(221, projection='3d')
surf = ax1.plot_surface(X1, X2, Y, cmap='viridis', edgecolor='none')
ax1.set_xlabel('x1', fontsize=12)
ax1.set_ylabel('x2', fontsize=12)
ax1.set_zlabel('f(x1, x2)', fontsize=12)
ax1.set_title('3D Поверхность (Изометрия)', fontsize=14)
fig.colorbar(surf, ax=ax1, shrink=0.5, aspect=10)

# 2. Вид сверху (проекция на плоскость XOY)
ax2 = fig.add_subplot(222)
contour = ax2.contourf(X1, X2, Y, 50, cmap='viridis')
ax2.set_xlabel('x1', fontsize=12)
ax2.set_ylabel('x2', fontsize=12)
ax2.set_title('Вид сверху (XOY)', fontsize=14)
fig.colorbar(contour, ax=ax2, shrink=0.5, aspect=10)

# 3. Срез при x2 = x20
ax3 = fig.add_subplot(223)
ax3.plot(x1, y_x2_fixed, 'b-', linewidth=2)
ax3.set_xlabel('x1', fontsize=12)
ax3.set_ylabel(f'f(x1, {x20})', fontsize=12)
ax3.set_title(f'Срез при $x_2$ = {x20}', fontsize=14)
ax3.grid(True)

# 4. Срез при x1 = x10
ax4 = fig.add_subplot(224)
ax4.plot(x2, y_x1_fixed, 'r-', linewidth=2)
ax4.set_xlabel('x2', fontsize=12)
ax4.set_ylabel(f'f({x10}, x2)', fontsize=12)
ax4.set_title(f'Срез при $x_1$ = {x10}', fontsize=14)
ax4.grid(True)

# Отображение тестовой точки
f_test = f(x10, x20)
plt.figtext(0.5, 0.01, 
            f'Тестовая точка: (x10, x20) = ({x10}, {x20}), f(x10, x20) = {f_test:.6f}',
            ha='center', fontsize=14, bbox=dict(facecolor='lightyellow', alpha=0.5))

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig('task_03_plot.png')
plt.show()
