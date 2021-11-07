import numpy as np
import matplotlib.pyplot as plt

def main():
    x = np.linspace(-np.pi, np.pi, 256, endpoint=True)
    c, s = np.cos(x), np.sin(x)
    plt.figure(1)
    plt.plot(x, c)
    plt.plot(x, s)
    plt.title('Cos and Sin')
    plt.show()


if __name__ == "__main__":
    main()