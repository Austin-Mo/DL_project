import yfinance as yf
import pandas as pd
import datetime

# Définir la période de collecte des données
start = "2007-01-03"
end = "2016-12-31"

# Liste des indices à récupérer
indices = {
    'KOSPI200': '^KS200',
    'Dollar': 'DX-Y.NYB',
    'SP500': '^GSPC',
    'Gold': 'GC=F',
    'Oil': 'CL=F'
}

# Dictionnaire pour stocker les données
data = {}

# Récupérer les données pour chaque indice
for name, ticker in indices.items():
    data[name] = yf.download(ticker, start=start, end=end)['Close']

# Convertir le dictionnaire en DataFrame
df = pd.DataFrame(data)

# Calculer les ratios de changement quotidiens
returns = df.pct_change()

# Check des nan (première ligne uniquement)
print(returns.isna().sum())
returns = returns.dropna()
print(returns.head())

# Définir la période de prédiction
q = 19

# Calculer les tendances basées sur le KOSPI 200
returns['trend'] = (df['KOSPI200'].shift(-q) - df['KOSPI200']) / df['KOSPI200']

# Supprimer les lignes avec des valeurs manquantes dans 'trend'
returns = returns.dropna(subset=['trend'])

# Supprimer les premières 19 lignes car elles ne peuvent pas avoir de tendance correcte
returns = returns.iloc[q:]

# Créer les vecteurs one-hot basés sur la tendance
returns['one_hot'] = returns['trend'].apply(lambda x: [1, 0] if x < 0 else [0, 1])

# Afficher les premières lignes des données avec la colonne 'trend'
print(returns.head())
