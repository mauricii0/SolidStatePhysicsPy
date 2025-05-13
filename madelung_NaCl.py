import numpy as np
import matplotlib.pyplot as plt
import math

# Función que genera las posiciones relativas de los iones en la celda unitaria del tipo NaCl, es posible agregar más tipos de cristales cubicos conociendo su base
def generar_base(tipo):
    if tipo == 'NaCl':
        # Posiciones relativas de los iones Cl⁻ en la celda unitaria FCC
        Cl = (np.array([
            [0., 0., 0.],
            [0.5, 0.5, 0.],
            [0.5, 0., 0.5],
            [0., 0.5, 0.5]
        ]), -1)  # Carga del ion Cl⁻

        # Posiciones relativas de los iones Na⁺ desplazadas 0.5 unidades en x respecto a los Cl⁻
        Na = (Cl[0] - np.array([0.5, 0, 0]), +1)  # Carga del ion Na⁺

        return [Cl, Na]  # Retorna las bases para NaCl

# Función principal que genera la red, calcula la suma de Madelung y grafica la estructura
def calcular_sumas_y_graficar(tipo='NaCl', N=1):
    bases = generar_base(tipo)  # Obtener la base de la celda unitaria
    puntos_totales = []         # Lista para almacenar posiciones de todos los iones
    cargas_totales = []         # Lista para almacenar las cargas correspondientes

    # Conjuntos para almacenar las posiciones únicas de Na⁺ y Cl⁻ para graficar
    if tipo == 'NaCl':
        puntos_Na = set()
        puntos_Cl = set()

    # Recorre un cubo de celdas unitarias de tamaño (2N+1)^3 centrado en el origen
    for i in range(-N, N+1):
        for j in range(-N, N+1):
            for k in range(-N, N+1):
                for base_pos, carga in bases:
                    for b in base_pos:
                        # Calcula la posición absoluta de cada ion en la red
                        punto = np.array([i + b[0], j + b[1], k + b[2]])
                        puntos_totales.append(punto)
                        cargas_totales.append(carga)

                        # Guarda las posiciones redondeadas en tuplas para evitar duplicados
                        if tipo == 'NaCl':
                            punto_redondeado = tuple(np.round(punto, 8))
                            if carga > 0:
                                puntos_Na.add(punto_redondeado)
                            else:
                                puntos_Cl.add(punto_redondeado)

    # Convertir listas a arreglos NumPy para facilitar operaciones posteriores
    puntos = np.array(puntos_totales)
    cargas = np.array(cargas_totales)

    # Convertir los conjuntos a arrays para graficar
    if tipo == 'NaCl':
        puntos_Na = np.array(list(puntos_Na))
        puntos_Cl = np.array(list(puntos_Cl))

    # === Cálculo de la suma de Madelung ===
    d0 = 0.5  # Distancia Na⁺-Cl⁻ más cercana en la estructura de NaCl
    Madelung_sum = 0  # Inicializa la suma de Madelung

    # Recorre todos los iones, y suma las contribuciones electrostáticas
    for p, z in zip(puntos, cargas):
        r = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)/d0  # Distancia adimensional
        if r != 0:  # Evita dividir entre cero para el ion en el origen
            Madelung_sum += z / r  # Suma de Madelung (sin constantes)

    # Mostrar resultados
    print(f"\nEstructura: {tipo}")
    print("Total de puntos generados:", len(puntos))
    print("Suma Madelung:", Madelung_sum)

    # === GRAFICAR la estructura cristalina ===
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Graficar iones Na⁺ y Cl⁻ en colores diferentes
    if tipo == 'NaCl':
        ax.scatter(puntos_Na[:, 0], puntos_Na[:, 1], puntos_Na[:, 2], s=40, c='orangered', label='Na⁺')
        ax.scatter(puntos_Cl[:, 0], puntos_Cl[:, 1], puntos_Cl[:, 2], s=40, c='dodgerblue', label='Cl⁻')
        ax.legend()

    # Configuraciones del gráfico
    ax.set_title(f'{tipo} lattice, N={N}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_box_aspect([1, 1, 1])  # Mantener proporciones iguales en ejes
    plt.tight_layout()
    plt.show()

# ==== EJECUTAR SOLO PARA NaCl con tamaño de supercelda N=10 ====
calcular_sumas_y_graficar('NaCl', N=1)