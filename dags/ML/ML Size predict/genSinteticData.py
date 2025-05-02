import numpy as np
import pandas as pd


def genData(seed=42, nrmRegisters=2000):
    """
    Generates a synthetic dataset containing information about height, weight, age, gender, 
    and estimated size based on specific rules.
    Parameters:
    -----------
    seed : int, optional
        The random seed for reproducibility. Default is 42.
    nrmRegisters : int, optional
        The number of records to generate. Default is 2000.
    Returns:
    --------
    pandas.DataFrame
        A DataFrame containing the following columns:
        - 'altura': Height (in cm), rounded to the nearest integer.
        - 'peso': Weight (in kg), rounded to the nearest integer.
        - 'idade': Age (in years).
        - 'genero': Gender ('M' for male, 'F' for female).
        - 'tamanho': Estimated size, calculated based on height, weight, age, and gender.
    """
    np.random.seed(seed)

    # Geração dos dados base
    altura = np.round(np.random.normal(170, 10, nrmRegisters))
    peso = np.round(np.random.normal(70, 15, nrmRegisters))
    idade = np.random.randint(18, 60, nrmRegisters)
    genero = np.random.choice(['M', 'F'], nrmRegisters)

    # Nova fórmula para estimar o tamanho
    def estimar_tamanho(altura, peso, idade, genero):
        if genero == 'M':
            tamanho_base = 40 + (peso - 70) // 5 + (altura - 170) // 10
        else:
            tamanho_base = 38 + (peso - 60) // 5 + (altura - 160) // 10

        if idade > 40:
            tamanho_base -= 1  # Ajuste para idades mais altas

        return int(np.clip(tamanho_base, 36, 50))

    # Criação do DataFrame via list comprehension
    df = pd.DataFrame([
        {
            "altura": round(int(h),0),
            "peso": round(int(p),0),
            "idade": i,
            "genero": g,
            "tamanho": estimar_tamanho(h, p, i, g)
        }
        for h, p, i, g in zip(altura, peso, idade, genero)
    ])
    
    return df

