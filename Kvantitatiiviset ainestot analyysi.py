import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from pandas import crosstab


#Luetaan csv tiedosto (tietuekehikko)

df = pd.read_csv(path + 'eduskunta.csv', sep = ',')


# Selvitetään käyttäjien iän tiedot (nuorin, vanhin, keskiarvo, mediaani)

print(df['age'].describe())


# Listataan Vote sarakkeet

vote_cols = ['Vote 1', 'Vote 2', 'Vote 3', 'Vote 4',
       'Vote 5', 'Vote 6', 'Vote 7', 'Vote 8', 'Vote 9', 'Vote 10', 'Vote 11',
       'Vote 12', 'Vote 13', 'Vote 14', 'Vote 15', 'Vote 16', 'Vote 17',
       'Vote 18', 'Vote 19', 'Vote 20', 'Vote 21', 'Vote 22', 'Vote 23',
       'Vote 24', 'Vote 25', 'Vote 26', 'Vote 27', 'Vote 28', 'Vote 29',
       'Vote 30', 'Vote 31', 'Vote 32', 'Vote 33', 'Vote 34', 'Vote 35',
       'Vote 36', 'Vote 37', 'Vote 38', 'Vote 39', 'Vote 40', 'Vote 41',
       'Vote 42', 'Vote 43', 'Vote 44', 'Vote 45', 'Vote 46', 'Vote 47',
       'Vote 48', 'Vote 49', 'Vote 50', 'Vote 51', 'Vote 52'] 

# Äänestysten äänimäärät -> valitaan äänestykset

df.info(verbose = True)

# Poistetaan kaikki käyttäjät, jotka eivät ole antaneet yhtään ääntä

df = df.dropna(axis = 0, subset = vote_cols, how = 'all')

# Ryhmitellään käyttäjät ikäryhmiin

conditions = [
       (df['age'] >= 18) & (df['age'] <= 35) , 
       (df['age'] >= 36) & (df['age'] <=100)
]

age_groups = ['nuoret' , 'vanhat']

df['age_group'] = np.select(conditions , age_groups)

# Poistetaan mahdolliset alaikäisten äänet

df = df[df['age_group'] != '0'] 

# Poistetaan tyhjää äänestäneet

df = df[df['Vote 28'] != 'tyhja'] 

df = df[df['Vote 38'] != 'tyhja'] 

# Tarkastetaan määrät

frequency_vote = df['residence'].value_counts()

frequency_age = df['age'].value_counts()

# Äänimäärät äänestyksissä

print(df['Vote 28'].value_counts())

print(df['Vote 38'].value_counts())

# Suoritetaan ristiintaulukointi

taulukko_1 = pd.crosstab(df['age_group'], df['Vote 38']) 

taulukko_1_percentage = pd.crosstab(df['age_group'], df['Vote 38'], normalize='index') 

taulukko_2 = pd.crosstab(df['age_group'], df['Vote 28']) 

taulukko_2_percentage = pd.crosstab(df['age_group'], df['Vote 28'], normalize='index') 

# Khiin neliötesti ja p-arvo

chi2, p, dof, expected = chi2_contingency(taulukko_1)

print(p)

chi2, p, dof, expected = chi2_contingency(taulukko_2)

print(p) 


# Tehdään taulukoista bar chartit

taulukko_1.plot(kind = 'barh')

taulukko_2.plot(kind = 'barh')


# Tallennetaan riistiintaulukoinnit Exceliin

writer = taulukko_1.to_excel(path + 'taulukko_1.xls', index = False)

writer = taulukko_2.to_excel(path + 'taulukko_2.xls', index = False)

writer = taulukko_1_percentage.to_excel(path + 'taulukko_1_percentage.xls', index = False)

writer = taulukko_2_percentage.to_excel(path + 'taulukko_2_percentage.xls', index = False)


# Ideksoitiin frequence age plottausta varten


frequency_age = df['age'].value_counts().sort_index(ascending=False)

frequency_age = frequency_age.reset_index()


# Käyttäjien ikäjakauma

import matplotlib.pyplot as plt
plt.figure()

plt.figure(figsize=(6,5)) 


x = frequency_age['age']
y = frequency_age['index']

xmin = plt.xlim(0,40)
ymin = plt.ylim(18,80)
plt.xlabel('määrä')
plt.ylabel('ikä')
plt.barh(y, x, height = 0.1)

plt.show()



# Kaupunkien käyttäjämäärät

frequency_age = df['residence'].value_counts().sort_index(ascending=False)

frequency_age = frequency_age.reset_index()

import matplotlib.pyplot as plt
plt.figure()

plt.figure(figsize=(7,20)) 


x = frequency_age['residence']
y = frequency_age['index']


plt.xlabel('määrä')
plt.ylabel('ikä')
plt.barh(y, x, height = 0.1)

plt.show()

