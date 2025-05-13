import matplotlib.pyplot as plt
import os
from datetime import datetime
import numpy as np

def bairstow(a, r, s, tol=1e-6, max_iter=100):
    n = len(a) - 1
    roots = []
    steps = []

    def solve(a, r, s):
        n = len(a) - 1
        b = np.zeros(n+1)
        c = np.zeros(n+1)
        b[n] = a[n]
        b[n-1] = a[n-1] + r*b[n]
        for i in range(n-2, -1, -1):
            b[i] = a[i] + r*b[i+1] + s*b[i+2]
        c[n] = b[n]
        c[n-1] = b[n-1] + r*c[n]
        for i in range(n-2, -1, -1):
            c[i] = b[i+1] + r*c[i+1] + s*c[i+2]
        return b, c

    while n >= 3:
        for i in range(max_iter):
            b, c = solve(a, r, s)
            det = c[2]*c[2] - c[3]*c[1]
            if abs(det) < tol:
                break
            dr = (-b[1]*c[2] + b[0]*c[3]) / det
            ds = (-b[0]*c[2] + b[1]*c[1]) / det
            r += dr
            s += ds
            steps.append((r, s))
            if abs(dr) < tol and abs(ds) < tol:
                break
        discriminant = r**2 + 4*s
        if discriminant >= 0:
            root1 = (r + np.sqrt(discriminant)) / 2
            root2 = (r - np.sqrt(discriminant)) / 2
        else:
            real = r / 2
            imag = np.sqrt(-discriminant) / 2
            root1 = complex(real, imag)
            root2 = complex(real, -imag)
        roots.extend([root1, root2])
        a = solve(a, r, s)[0][2:]
        n = len(a) - 1
    if n == 2:
        r = -a[1] / a[2]
        s = -a[0] / a[2]
        discriminant = r**2 + 4*s
        if discriminant >= 0:
            root1 = (r + np.sqrt(discriminant)) / 2
            root2 = (r - np.sqrt(discriminant)) / 2
        else:
            real = r / 2
            imag = np.sqrt(-discriminant) / 2
            root1 = complex(real, imag)
            root2 = complex(real, -imag)
        roots.extend([root1, root2])
    elif n == 1:
        roots.append(-a[0]/a[1])
    return roots, steps



def graficar_convergencia(steps, save_path):
    r_vals = [step[0] for step in steps]
    s_vals = [step[1] for step in steps]
    iteraciones = list(range(1, len(steps)+1))

    plt.figure(figsize=(10, 5))
    plt.plot(iteraciones, r_vals, label='r', marker='o')
    plt.plot(iteraciones, s_vals, label='s', marker='x')
    plt.xlabel('Iteración')
    plt.ylabel('Valor')
    plt.title('Convergencia de r y s')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()

    filename = f"convergencia_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
    full_path = os.path.join(save_path, filename)
    plt.savefig(full_path)
    plt.close()

    return filename