import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import math
import numpy as np
colors = plt.get_cmap('Blues')(np.linspace(1, 0.5,15))


df = pd.read_csv(r"D:\Users\User\Desktop\Studia\MGR\SEM2\MEIAD\muzyczka_z_gatunkami.csv")

kopia = df.copy()
kopia['Suma_odtw'] = kopia['Stream'] + kopia["Views"]

print(df.info())
print(df.duplicated().sum())
print(df["Genre"].value_counts())

def GatunkiWykres():
    gatunki_ilosc = df["Genre"].value_counts()
    print(gatunki_ilosc.index)
    # print(gatunki_ilosc[1])
    plt.figure(figsize = (20, 6))
    ax = gatunki_ilosc[0:15].plot(kind = 'bar', rot = 0, color=colors, zorder = 100)
    ax.set_xticklabels(gatunki_ilosc.index[0:15], fontweight = 'bold')
    for p in ax.patches:
        ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() + 1), ha = 'center', va = 'bottom', color = 'black')
    # plt.grid()
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', zorder=-100, which='both', axis = 'y')
    plt.title("")
    plt.xlabel("Gatunek")
    plt.ylabel("Ilosc wystapien")
    plt.savefig("Gatunki_wykres.png")
    plt.show()
# GatunkiWykres()

def Top10Spotify():
    
    sort = df.sort_values(by = 'Stream', ascending= False)
    top10 = sort.head(10)
    print(top10)
    labels = [f"{autor} \n {tytul}" for autor, tytul in zip(top10['Artist'],top10['Track'])]
    plt.figure(figsize = (15, 6))
    ax = plt.bar(labels, top10['Stream'], color=colors,zorder = 100)
    # for p in ax.patches:
    #     ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() + 1), ha = 'center', va = 'bottom', color = 'black')
    # plt.yticks(1e8)
    y_major = MultipleLocator(base = 0.1e9)

    for bar, odtworzenia in zip(ax, top10['Stream']):
        plt.annotate(str(f"{odtworzenia/1e9:.2f} mld"), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom')

    plt.xticks(rotation = 30)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.tight_layout()
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', zorder=-100, which='both', axis = 'y')
    plt.title("Top 10 Piosenek wg odtwarzan na spotify")
    plt.xlabel("Wykonawca i tytul")
    plt.ylabel("Ilosc wyswietlen [mld]")
    plt.show()

def Top10YT():
    
    sort = df.sort_values(by = 'Views', ascending= False)
    top10 = sort.head(10)
    print(top10)
    labels = [f"{autor} \n {tytul}" for autor, tytul in zip(top10['Artist'],top10['Track'])]
    plt.figure(figsize = (15, 6))
    ax = plt.bar(labels, top10['Views'], color=colors,zorder = 100)
    # for p in ax.patches:
    #     ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() + 1), ha = 'center', va = 'bottom', color = 'black')
    # plt.yticks(1e8)
    y_major = MultipleLocator(base = 0.5e9)

    for bar, odtworzenia in zip(ax, top10['Views']):
        plt.annotate(str(f"{odtworzenia/1e9:.2f} mld"), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom')

    plt.xticks(rotation = 30)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.tight_layout()
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', zorder=-100, which='both', axis = 'y')
    plt.title("Top 10 Piosenek wg odtwarzan na YT")
    plt.xlabel("Wykonawca i tytul")
    plt.ylabel("Ilosc wyswietlen [mld]")
    plt.show()

def Top10Sum():
    sort = kopia.sort_values(by = 'Suma_odtw', ascending= False)
    top10 = sort.head(10)
    print(top10)
    labels = [f"{autor} \n {tytul}" for autor, tytul in zip(top10['Artist'],top10['Track'])]
    plt.figure(figsize = (15, 6))
    ax = plt.bar(labels, top10['Suma_odtw'], color=colors,zorder = 100)
    # for p in ax.patches:
    #     ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() + 1), ha = 'center', va = 'bottom', color = 'black')
    # plt.yticks(1e8)
    y_major = MultipleLocator(base = 0.5e9)

    for bar, odtworzenia in zip(ax, top10['Suma_odtw']):
        plt.annotate(str(f"{odtworzenia/1e9:.2f} mld"), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom')

    plt.xticks(rotation = 30)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.tight_layout()
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', zorder=-100, which='both', axis = 'y')
    plt.title("Top 10 Piosenek wg sumy odtworzen na Spotify i YT")
    plt.xlabel("Wykonawca i tytul")
    plt.ylabel("Ilosc wyswietlen [mld]")
    plt.show()

def Top10Artists():
    suma = kopia.groupby('Artist')["Suma_odtw"].sum()
    sort = suma.sort_values(ascending= False)
    print(sort)
    sort = sort.head(10)
    gatunki = []
    artysta = list(sort.index)
   
    for i in range(len(sort)):
        gatunki.append(kopia.loc[df['Artist'] == artysta[i], 'Genre'].iloc[0])

    labels = [f"{autor} \n {tytul}" for autor, tytul in zip(sort.index,gatunki)]
    plt.figure(figsize = (15, 6))
    ax = plt.bar(labels, sort, color=colors,zorder = 100)
    # for p in ax.patches:
    #     ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() + 1), ha = 'center', va = 'bottom', color = 'black')
    # plt.yticks(1e8)
    y_major = MultipleLocator(base = 1e9)

    for bar, odtworzenia in zip(ax, sort):
        plt.annotate(str(f"{odtworzenia/1e9:.2f} mld"), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom')

    plt.xticks(rotation = 30)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.tight_layout()
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', zorder=-100, which='both', axis = 'y')
    plt.title("Top 10 wykonawcow wg sumy odtworzen na Spotify i YT")
    plt.xlabel("Wykonawca i gatunek")
    plt.ylabel("Ilosc wyswietlen [mld]")
    plt.show()

def Top10Genre():
    suma = kopia.groupby('Genre')["Suma_odtw"].sum()

    sort = suma.sort_values(ascending= False)
    print(sort)
    sort = sort.head(10)
    # gatunki = []
    # artysta = list(sort.index)
   
    # for i in range(len(sort)):
    #     gatunki.append(kopia.loc[df['Artist'] == artysta[i], 'Genre'].iloc[0])

    # labels = [f"{autor} \n {tytul}" for autor, tytul in zip(sort.index,gatunki)]
    plt.figure(figsize = (15, 6))
    ax = plt.bar(sort.index, sort, color=colors,zorder = 100)
    # for p in ax.patches:
    #     ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() + 1), ha = 'center', va = 'bottom', color = 'black')
    # plt.yticks(1e8)
    y_major = MultipleLocator(base = 0.5e11)

    for bar, odtworzenia in zip(ax, sort):
        plt.annotate(str(f"{odtworzenia/1e9:.2f} mld"), xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()), xytext=(0, 3),
                 textcoords="offset points", ha='center', va='bottom')

    plt.xticks(rotation = 30)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.tight_layout()
    plt.grid(True, linestyle='--', linewidth=0.5, color='gray', zorder=-100, which='both', axis = 'y')
    # plt.title("Top 10 gatunków wg sumy odtworzen na Spotify i YT")
    plt.xlabel("Gatunek")
    plt.ylabel("Ilosc wyswietlen [mld]")
    plt.savefig("top10gatunkow.png")
    plt.show()

def HistDance():
    
    df_cleaned = df.dropna(subset=['Danceability'])

    print(df_cleaned['Energy'].min(), df_cleaned['Energy'].max())

    bins = [i/100 for i in range(0,105,5)]
    plt.hist(df_cleaned['Danceability'], bins=bins, edgecolor='black', alpha=0.7, color='skyblue',density=True)
    df_cleaned['Danceability'].plot(kind = 'kde',color = 'red',xlim=(0,1))
    y_major = MultipleLocator(base = 0.1)
    x_major = MultipleLocator(base = 0.05)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.gca().xaxis.set_major_locator(x_major)
    plt.ylabel('Ilosc/gestosc')
    plt.xlabel('Danceability')
    plt.legend(['Gestosc prawdopodobienstwa','Histogram'])
    plt.grid()
    plt.show()

def HistEnergy():
    
    df_cleaned = df.dropna(subset=['Energy'])

    print(df_cleaned['Energy'].min(), df_cleaned['Energy'].max())
    print(df_cleaned.info())
    bins = [i/100 for i in range(0,105,5)]
    plt.hist(df_cleaned['Energy'], bins=bins, edgecolor='black', alpha=0.7, color='skyblue',density=True,zorder = 50)
    df_cleaned['Energy'].plot(kind = 'kde',color = 'red',xlim=(0,1), zorder = 100)
    
    y_major = MultipleLocator(base = 0.1)
    x_major = MultipleLocator(base = 0.05)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.gca().xaxis.set_major_locator(x_major)
    plt.ylabel('Ilosc/gestosc')
    plt.xlabel('Energy')
    plt.legend(['Gestosc prawdopodobienstwa','Histogram'])
    plt.grid(zorder = -1000)
    plt.show()

def Hist(column):
    df['Duration_ms'] = df['Duration_ms'] / 60000
    df_cleaned = df.dropna(subset=[column])
    df_cleaned = df_cleaned[df_cleaned[column] >= 0]
    a, b = df_cleaned[column].min(), df_cleaned[column].max()
    a = int(a)
    b = math.ceil(b)
    print(a, b)
    plt.figure(figsize = (18, 8))
    # print(df_cleaned.info())
    bins = [i/100 for i in range(0,105,5)]
    plt.hist(df_cleaned[column], bins=30, edgecolor='black', alpha=0.7, color='skyblue',density=True,zorder = 50)
    df_cleaned[column].plot(kind = 'kde',color = 'red',xlim=(int(a),math.ceil(b)), zorder = 100)
    
    # y_major = MultipleLocator(base = 0.1)
    # x_major = MultipleLocator(base = 1)
    # plt.gca().yaxis.set_major_locator(y_major)
    # plt.gca().xaxis.set_major_locator(x_major)
    plt.locator_params(axis='y', nbins=20)
    plt.title(f"Rozklad zmiennej {column}")
    plt.ylabel('Ilosc/gestosc')
    plt.xlabel(column)
    plt.legend(['Gestosc prawdopodobienstwa','Histogram'])
    plt.grid(zorder = -1000)
    plt.savefig(f"Histogram_{column}.png")
    plt.show()

from matplotlib.ticker import ScalarFormatter

def HistLog(column):
    df['Duration_ms'] = df['Duration_ms'] / 60000
    df_cleaned = df.dropna(subset=[column])


    a, b = df_cleaned[column].min(), df_cleaned[column].max()
    a = int(a)
    b = math.ceil(b)
    print(a, b)
    plt.figure(figsize=(18, 8))
    
    bins = [i / 100 for i in range(0, 105, 5)]
    plt.hist(df_cleaned[column], bins=20, edgecolor='black', alpha=0.7, color='skyblue', density=True, zorder=50)
    df_cleaned[column].plot(kind='kde', color='red', xlim=(int(a), math.ceil(b)), zorder=100)
    
    plt.yscale('log')
    
    plt.title(f"Rozkład zmiennej {column}")
    plt.ylabel('Ilość/gęstość')
    plt.xlabel(column)
    plt.legend(['Gęstość prawdopodobieństwa', 'Histogram'])
    
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    
    # Zmiana formatu wyświetlanych wartości na osi Y
    plt.gca().yaxis.set_major_formatter(ScalarFormatter())
    plt.gca().yaxis.get_major_formatter().set_scientific(False)
    plt.gca().yaxis.get_major_formatter().set_useOffset(False)
    
    plt.grid(zorder=-1000)
    plt.savefig(f"Histogram_{column}_LOG_SCALAR.png")
    plt.show()

def HistMod(column, max):
    df['Duration_ms'] = df['Duration_ms'] / 60000
    df_cleaned = df.dropna(subset=[column])
    print(df_cleaned[column])
    a, b = df_cleaned[column].min(), df_cleaned[column].max()
    a = int(a)
    b = math.ceil(max)
    print(a, b)
    plt.figure(figsize = (18, 8))
    # print(df_cleaned.info())
    bins = [i/100 for i in range(0,105,5)]
    plt.hist(df_cleaned[df_cleaned[column] <= max][column], bins=20, edgecolor='black', alpha=0.7, color='skyblue',density=True,zorder = 50)
    df_cleaned[column].plot(kind = 'kde',color = 'red',xlim=(int(a),math.ceil(b)), zorder = 100)
    
    # y_major = MultipleLocator(base = 0.1)
    # x_major = MultipleLocator(base = 1)
    # plt.gca().yaxis.set_major_locator(y_major)
    # plt.gca().xaxis.set_major_locator(x_major)
    plt.locator_params(axis='y', nbins=20)
    plt.title(f"Rozklad zmiennej {column}")
    plt.ylabel('Ilosc/gestosc')
    plt.xlabel(column)
    plt.legend(['Gestosc prawdopodobienstwa','Histogram'])
    plt.grid(zorder = -1000)
    plt.savefig(f"Histogram_mod_{int(max)}_{column}.png")
    plt.show()

def HistCalk(column):
    
    df_cleaned = df.dropna(subset=[column])
    
    a, b = df_cleaned[column].min(), df_cleaned[column].max()
    # print(df_cleaned[column].unique())
    a = int(a)
    b = math.ceil(b)
    print(a, b)
    # print(df_cleaned.info())
    bins = [i - 0.5 for i in range(b+2)]
    plt.hist(df_cleaned[column], bins=bins, edgecolor='black', alpha=0.7, color='skyblue',density=True,zorder = 50)
    
    y_major = MultipleLocator(base = 0.1)
    x_major = MultipleLocator(base = 1)
    plt.gca().yaxis.set_major_locator(y_major)
    plt.gca().xaxis.set_major_locator(x_major)
    plt.ylabel('Ilosc/gestosc')
    plt.xlabel(column)
    plt.xticks(range(b+1))
    plt.grid(zorder = -1000)
    plt.savefig(f"Histogram_{column}.png")
    plt.show()

# print(df['Key'].unique())
# HistMod('Stream',1e9)
# Top10Genre()
Hist('Stream')

Top10Genre()
GatunkiWykres()