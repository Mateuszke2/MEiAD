import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

colors = ['blue', 'green', 'red', 'purple', 'orange', 'yellow', 'brown', 'gray', 'cyan', 'magenta']

df = pd.read_csv(r"D:\Users\User\Desktop\Studia\MGR\SEM 2\MEIAD\muzyczka_z_gatunkami.csv")

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
    ax = gatunki_ilosc[0:10].plot(kind = 'bar', rot = 0, color=colors)
    ax.set_xticklabels(gatunki_ilosc.index[0:10], fontweight = 'bold')
    for p in ax.patches:
        ax.annotate(int(p.get_height()), (p.get_x() + 0.25, p.get_height() + 1), ha = 'center', va = 'bottom', color = 'black')
    # plt.grid()
    plt.title("")
    plt.xlabel("Gatunek")
    plt.ylabel("Ilosc wystapien")
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
    plt.title("Top 10 gatunków wg sumy odtworzen na Spotify i YT")
    plt.xlabel("Gatunek")
    plt.ylabel("Ilosc wyswietlen [mld]")
    plt.show()

def HistSumaWysw():
    return 0

Top10Genre()

