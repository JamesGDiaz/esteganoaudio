import numpy as np
import matplotlib.pyplot as plt


def plot2signals(s1, s2, t1, t2):
    for i in range(len(s1)):
        if s2[i] == s1[i]:
            s2[i] = 0
        else:
            s2[i] = 50*s2[i]

    ys2 = np.ma.masked_where(s2 == 0, s2)
    dt = 1/44100
    t = np.arange(t1, t2, dt)  # [:-1]
    fig, axis = plt.subplots()
    axis.plot(t, s1, "blue", linewidth=0.2)
    axis.plot(t, ys2, "ro")
    axis.set_xlim(t1, t2)
    axis.set_xlabel('Tiempo [s]')
    axis.set_ylabel('Amplitud')
    axis.grid(True)
    plt.legend(('Señal original', 'Señal del mensaje secreto amplificada x100'),
               loc='upper right')
    plt.title('Señales de audio')
    fig.tight_layout()
    plt.show()
