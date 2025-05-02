import numpy as np
import math

def generate_bcc_lattice_indices(N):
    indices = []
    for n1 in range(-N, N + 1):
        for n2 in range(-N, N + 1):
            for n3 in range(-N, N + 1):
                indices.append((n1, n2, n3))
    return indices

def madelung_constant_cscl(N_max):
    a = 1
    a1 = 0.5 * a * np.array([1, 1, -1])
    a2 = 0.5 * a * np.array([1, -1, 1])
    a3 = 0.5 * a * np.array([-1, 1, 1])
    count = 0
    indices = generate_bcc_lattice_indices(N_max)

    M = 0.0
    d0 = math.sqrt(0.5**2 + 0.5**2 + 0.5**2)
    for (n1, n2, n3) in indices:
        count += 1
        if n1 == 0 and n2 == 0 and n3 == 0:
            continue

        r_vec = n1 * a1 + n2 * a2 + n3 * a3
        r = np.linalg.norm(r_vec)

        if r == 0:
            continue

        if (n1 + n2 + n3) % 2 == 0:
            charge = -1  
        else:
            charge = 1  
        M += charge /(r/d0)
        num = count
    return M, num

if __name__ == "__main__":
    N_max = 30

    M, num = madelung_constant_cscl(N_max)

    print(f"Number of atoms generated: {num}")
    print(f"Madelung constant for CsCl BCC lattice (N_max = {N_max}): {M:.6f}")
