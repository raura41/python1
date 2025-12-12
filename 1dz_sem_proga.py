import json
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt

class RCSCalculator:
    def __init__(self, D, f_min, f_max, num_points=1000):
        self.D = D
        self.r = D / 2
        self.f_min = f_min
        self.f_max = f_max
        self.num_points = num_points
        self.freqs = np.linspace(f_min, f_max, num_points)
        self.c = 3e8  # Скорость света

    def calculate_rcs(self):
        wavelengths = self.c / self.freqs
        k = 2 * np.pi / wavelengths
        rcs = []

        for i, freq in enumerate(self.freqs):
            kr = k[i] * self.r
            n_max = int(np.ceil(kr + 4 * (kr)**(1/3) + 2))
            total = 0j

            for n in range(1, n_max + 1):
                jn = spherical_jn(n, kr)
                jn_prev = spherical_jn(n-1, kr)
                yn = spherical_yn(n, kr)
                hn = jn + 1j * yn
                hn_prev = spherical_jn(n-1, kr) + 1j * spherical_yn(n-1, kr)

                a_n = jn / hn
                numerator = kr * jn_prev - n * jn
                denominator = kr * hn_prev - n * hn
                b_n = numerator / denominator

                term = (-1)**n * (n + 0.5) * (b_n - a_n)
                total += term

            sigma = (wavelengths[i]**2 / np.pi) * np.abs(total)**2
            rcs.append(sigma)

        return {
            'freq': self.freqs.tolist(),
            'lambda': wavelengths.tolist(),
            'rcs': rcs
        }

class ResultOutput:
    @staticmethod
    def save_to_json(data, filename):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def plot_rcs(data, save_path=None):
        plt.figure(figsize=(10, 6))
        plt.plot(data['freq'], data['rcs'])
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('RCS (m²)')
        plt.title('ЭПР идеально проводящей сферы')
        plt.grid(True)
        if save_path:
            plt.savefig(save_path)
        plt.show()

def main():
    # Чтение параметров из JSON-файла
    with open('task_rcs_01.json') as f:
        data = json.load(f)
    
    # Выбор варианта (например, вариант 1)
    variant = data['data'][3]['variant']
    D = float(variant['D'])
    f_min = float(variant['fmin'])
    f_max = float(variant['fmax'])

    # Расчёт ЭПР
    calculator = RCSCalculator(D, f_min, f_max)
    result = calculator.calculate_rcs()

    # Сохранение результатов
    ResultOutput.save_to_json(result, 'rcs_result.json')
    ResultOutput.plot_rcs(result, 'rcs_plot.png')

if __name__ == '__main__':
    main()