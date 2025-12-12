import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson

class DipoleAntenna:
    """Класс для расчета характеристик симметричного вибратора"""
    
    def __init__(self, f_ghz, ratio_2l_lambda):
        self.f = f_ghz * 1e9
        self.ratio_2l_lambda = ratio_2l_lambda
        self.c = 3e8
        self.Z0 = 120 * np.pi
        
        self.lambda_ = self.c / self.f
        self.l = self.lambda_ * ratio_2l_lambda / 2
        self.k = 2 * np.pi / self.lambda_
        
        # Вычисляем Dmax один раз при инициализации
        self.Dmax = self._calculate_Dmax()
    
    def field_pattern(self, theta_deg):
        """Нормированная характеристика направленности F(θ)"""
        theta = np.deg2rad(theta_deg)
        sin_theta = np.sin(theta)
        
        # Защита от деления на ноль
        mask = np.abs(sin_theta) < 1e-10
        sin_theta = np.where(mask, 1e-10, sin_theta)
        
        # Формула (3) из задания
        F = np.abs((np.cos(self.k * self.l * np.cos(theta)) - np.cos(self.k * self.l)) / sin_theta)
        
        # Нормировка
        return F / np.max(F)
    
    def _calculate_Dmax(self):
        """Расчет максимального КНД Dmax (формула 2)"""
        theta_rad = np.linspace(0, np.pi, 1000)
        F = self.field_pattern(np.rad2deg(theta_rad))
        integrand = F**2 * np.sin(theta_rad)
        
        integral = simpson(integrand, theta_rad)
        return 4 * np.pi / (2 * np.pi * integral) if integral > 0 else 1.0
    
    def calculate_D_theta(self, theta_deg):
        """КНД в зависимости от угла θ (формула 4)"""
        F = self.field_pattern(theta_deg)
        return F**2 * self.Dmax


class ResultVisualizer:
    """Класс для визуализации результатов"""
    
    def __init__(self, antenna):
        self.antenna = antenna
    
    def plot_diagrams(self):
        """Построение всех графиков"""
        theta = np.linspace(0, 180, 361)
        D_analytical = self.antenna.calculate_D_theta(theta)
        D_analytical_dB = 10 * np.log10(D_analytical + 1e-10)
        
        print(f"Максимальный КНД: {self.antenna.Dmax:.4f} (в разах)")
        print(f"Максимальный КНД: {10*np.log10(self.antenna.Dmax):.4f} дБ")
        
        # Декартовы графики
        fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        ax1.plot(theta, D_analytical, 'b-', linewidth=2)
        ax1.set_xlabel('Угол θ, градусы')
        ax1.set_ylabel('КНД D(θ)')
        ax1.set_title('Диаграмма направленности (линейный масштаб)')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, 180)
        ax1.set_ylim(bottom=0)
        
        ax2.plot(theta, D_analytical_dB, 'b-', linewidth=2)
        ax2.set_xlabel('Угол θ, градусы')
        ax2.set_ylabel('КНД D(θ), дБ')
        ax2.set_title('Диаграмма направленности (децибелы)')
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, 180)
        
        plt.tight_layout()
        plt.savefig('dipole_cartesian.png', dpi=150)
        plt.show()
        
        # Полярные графики
        fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(12, 6), subplot_kw={'projection': 'polar'})
        
        theta_rad = np.deg2rad(theta)
        ax3.plot(theta_rad, D_analytical, 'b-', linewidth=2)
        ax3.set_title('Полярная диаграмма (линейный масштаб)')
        
        ax4.plot(theta_rad, D_analytical_dB + 30, 'b-', linewidth=2)
        ax4.set_title('Полярная диаграмма (дБ + 30)')
        
        plt.tight_layout()
        plt.savefig('dipole_polar.png', dpi=150)
        plt.show()


def main():
    """Главная функция"""
    antenna = DipoleAntenna(f_ghz=4.0, ratio_2l_lambda=0.7)
    visualizer = ResultVisualizer(antenna)
    visualizer.plot_diagrams()


if __name__ == "__main__":
    main()