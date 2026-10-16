---
title: |
  Séance 4\
  Tableaux avec pandas, tracés avec Matplotlib
subtitle: "Santé numérique, Mastère Spécialisé · 2026"
author: "Paul Dubois"
date: "Semaine 1, cours"
---

## Données

![](img/dataframe.png)

::: notes
Avant tout figure, il y a un tableau : un export du système d'information hospitalier, un
feuille de calcul d'un collègue, les résultats d'une requête. pandas est la bibliothèque qui le lit
et vous donne un objet, le DataFrame.
Vocabulaire, que chaque message d'erreur utilise. Le DataFrame est la table entière. Chaque colonne
a un nom et un type (`df.dtypes`) ; une seule colonne est une Series. Chaque ligne a une étiquette,
l'index, qui par défaut est juste sa position.
La colonne âge se lit comme `float64` et non comme un entier en raison de la valeur manquante :
`NaN` n'existe que pour les flottants, donc une cellule vide fait flotter toute la colonne. C'est le
première surprise de toute véritable exportation.
`df.head()`, `df.shape`, `df.info()` : les trois commandes à exécuter sur n'importe quelle table que vous recevez,
avant toute autre chose.
:::

## Table ou tableau ?

![](img/table_vs_array.png)

::: notes
Un tableau numpy (session 3) contient un type et des positions. `a[:, 1]` est la deuxième colonne, et
rien dans le tableau ne dit ce qu'était la deuxième colonne : vous la gardez dans votre tête, ou dans un
commentez, et un jour vous vous trompez.
Un DataFrame conserve les noms et autorise un type par colonne, donc le texte (`ward`, `outcome`) et
les nombres vivent dans le même tableau. `clean["age"]` ne peut pas être la mauvaise colonne.
La règle de ce cours : des pandas à charger, nettoyer et sélectionner ; numpy à l'intérieur, pour le
calcul; matplotlib à la fin, pour la figure. Une colonne est un tableau numpy en dessous,
donc `ax.plot(df["age"], df["los_days"])` fonctionne.
:::

## Chargement d'une table

```python
import pandas as pd

df = pd.read_csv("../data/patients.csv")
df.head()
df.shape      # (240, 7)
df.dtypes     # one type per column
df.info()     # types and the number of values present
```

::: notes
`pd.read_csv` est une ligne pour ce qui a nécessité une boucle `csv.DictReader`, une liste de dictés et un
conversion manuelle de chaque champ. Il lit également Excel (`read_excel`), JSON, SQL et autres,
avec la même forme d'appel.
Arguments utiles lorsque l'export ne coopère pas : `sep=";"` (la valeur par défaut d'Excel français),
`decimal=","`, `na_values=["", "NA", "NR"]`, `parse_dates=["admission"]`,
`encoding="latin-1"`.
`df.info()` est celui qui vous indique combien de valeurs sont réellement présentes par colonne, donc
combien en manquent.
:::

## Valeurs et types manquants

```python
df.isna().sum()                  # how many NaN per column

clean = df.dropna()              # keep only the complete rows
len(df), len(clean)              # 240, 232

clean["age"] = clean["age"].astype("int64")
clean["ward"] = clean["ward"].astype("category")
clean["admission"] = pd.to_datetime(clean["admission"])
```

::: notes
`isna()` donne un tableau de Vrai/Faux, et `.sum()` compte les Vrai par colonne : les manquants
rapport de la valeur de l'export, sur une seule ligne.
`dropna()` supprime chaque ligne avec au moins une valeur manquante. C'est le choix le plus simple,
pas toujours la bonne : ici cela coûte 8 patients sur 240. `dropna(subset=["age"])`
tombe uniquement sur la colonne qui compte, et `fillna(value)` remplace au lieu de supprimer.
Quoi que vous choisissiez, dites-le dans la section méthodes.
Une fois les NaN partis, `astype("int64")` redonne un âge réel entier. `"category"` est pour
une colonne avec peu de valeurs distinctes (la salle, le résultat) : moins de mémoire, et elle dit que
ce sont des groupes. `pd.to_datetime` transforme le texte d'admission en dates réelles, qui peuvent être
soustrait et trié.
:::

## Sélection

```python
clean["age"]                     # one column, a Series
clean["age"].mean()              # 50.9
clean["ward"].value_counts()     # how many patients per ward

summary = clean[["patient_id", "age"]]  # a smaller DataFrame

type(clean["age"])               # Series
type(clean[["age"]])             # DataFrame, one column
```

::: notes
Un nom entre crochets donne une Series, qui porte les statistiques habituelles comme méthodes :
`mean`, `median`, `std`, `min`, `max`, `describe`.
`value_counts()` est celui que vous utiliserez en permanence sur les colonnes catégorielles : le nombre
de patients par service, par résultat, par sexe, triés, en un seul appel.
Une liste de noms entre crochets donne un DataFrame avec ces colonnes, dans cet ordre. D'où
les doubles parenthèses : les extérieures sont la sélection, les intérieures sont la liste.
La sélection de lignes au lieu de colonnes est une condition : `clean[clean["ward"] == "ICU"]`, exactement
les masques booléens de la Session 3, appliqués à un tableau.
:::

## Une nouvelle colonne avec .apply

```python
def stay_length(days):
    if days < 3:
        return "short"
    if days > 10:
        return "long"
    return "medium"

summary["stay"] = summary["los_days"].apply(stay_length)
```

::: notes
ajouter `summary["age_group"] = summary["age"].apply(lambda a: "minor" if a < 18 else "adult")` ?

`.apply(f)` appelle `f` sur chaque valeur de la colonne et renvoie une nouvelle colonne de résultats. Le
est une fonction Python ordinaire (Session 2), donc n'importe quelle règle que vous pouvez écrire, vous pouvez
appliquer : un seuil clinique, un recodage, une analyse d'un champ de texte libre.
L'attribution à `summary["stay"]` avec un nom qui n'existe pas encore crée la colonne.
Pour l'arithmétique, n'utilisez pas `apply` : `clean["weight"] / clean["height"] ** 2` fonctionne sur l'ensemble
colonnes à la fois, et est beaucoup plus rapide car numpy fait la boucle. Gardez `apply` pour quoi
ne peut pas être écrit sous forme de formule.
:::

## Enregistrer une table

```python
summary.to_csv("patients_summary.csv", index=False)

back = pd.read_csv("patients_summary.csv")
back.shape        # (232, 6)
```

::: notes
`to_csv` réécrit la table sur le disque et `index=False` conserve les étiquettes de ligne hors du
fichier. Sans cela, vous obtenez une première colonne sans nom de 0, 1, 2, que le prochain lecteur (souvent
vous, le mois prochain) doit faire le ménage à nouveau.
Autres formats, même appel : `to_excel` lorsqu'un collègue le demande, `to_parquet` pour un grand
table qui reste à l'intérieur du projet (plus petite et plus rapide, et elle conserve les types).
N'économisez jamais sur l'exportation brute. Le fichier brut reste intact, le script reconstruit tout
sinon : c’est ce qui rend l’analyse reproductible.
:::

## Flux de travail complet

![](img/pandas_flow.png)

::: notes
C'est la forme de presque tous les scripts d'analyse : charger, nettoyer, sélectionner, calculer, enregistrer et
puis tracez.
Chaque étape renvoie une nouvelle table au lieu de changer l'ancienne, donc les noms des variables
(`df`, `clean`, `summary`) enregistrez l'état des données à chaque étape et réexécutez une cellule
ne peut pas corrompre ce qui a précédé.
La suite de cette session est la dernière flèche, les figures, avec matplotlib. Les colonnes que vous
vous venez de sélectionner ce que vous êtes sur le point de tracer.
:::

## Comprendre avec un graphique

![](img/anscombe.png)

::: notes
Le quatuor d'Anscombe (1973). Quatre ensembles de données de 11 points : même moyenne, même variance, même
corrélation, même droite de régression, à deux décimales. Un tableau de statistiques récapitulatives indique qu'ils
sont identiques.
Les tracés indiquent : une relation linéaire bruyante, une courbe, une ligne parfaite avec une valeur aberrante, et non
relation du tout sauf un point extrême.
L'habitude à prendre : tracer les données brutes avant toute statistique. Dans les données cliniques, le tracé est
où vous trouvez les âges impossibles, l'unité change (kg vs lb), les lignes dupliquées et
l'appareil qui a été débranché.
:::

## Anatomie d'une figure

![](img/anatomy.png)

::: notes
Vocabulaire Matplotlib, utilisé par chaque message d'erreur et chaque réponse Stack Overflow.
La Figure est le canevas : le fichier que vous enregistrez. Un Axes (avec un e, Axes pluriel) est un graphique
zone avec ses propres coordonnées : une figure peut en contenir plusieurs. Tout le reste (ligne, titre,
étiquettes, graduations, légende) appartient à un axe et est défini par une méthode de cet axe.
Ne confondez pas les axes (la zone de tracé) avec les axes (la règle x ou y d'un axe).
:::

## Premier figure

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(t, temp, label="temperature")
ax.axhline(38, ls="--", label="fever")
ax.set_xlabel("time (h)")
ax.set_ylabel("temperature (°C)")
ax.set_title("Patient P0001")
ax.legend()
fig.savefig("temp.png", dpi=200)
```

::: notes
Le patron de chaque figure de ce cours : créer la figure et ses axes, dessiner sur le
axes, étiquetez les axes, enregistrez la figure.
`plt.subplots()` renvoie deux choses, décompressées dans `fig` et `ax` (décompression de tuple, de
Séance 1).
Vous verrez également le style court `plt.plot(...)`, `plt.xlabel(...)` : il s'appuie sur "le
axes actuels". C'est bien pour un aperçu rapide, mais dès qu'il y a deux graphiques, cela devient
ambigu. Utilisez `fig, ax` partout et vous n'aurez jamais à vous poser de questions.
Dans un cahier, le figure est affiché à la fin de la cellule ; dans un script, appelez
`plt.show()` ou enregistrez-le simplement.
:::

## Plusieurs tracés dans une seule figure

![](img/subplots_grid.png)

::: notes
`plt.subplots(2, 3)` renvoie un tableau numpy d'axes, de forme `(2, 3)`, indexé exactement comme
les tableaux de la session 1 : `axes[1, 2]` est celui en bas à droite.
Avec une seule ligne ou colonne, le tableau est 1D : `axes[0]`, `axes[1]`.
`axes.flat` parcourt chacun d'entre eux, pour appliquer le même paramètre partout.
`sharex=True` donne à tous les tracés le même axe x (essentiel pour les signes vitaux au fil du temps).
`fig.tight_layout()` corrige les étiquettes qui se chevauchent : appelez-le juste avant de sauvegarder.
:::

## Quelle graphique ?

![](img/plot_types.png)

::: notes
Choisissez le tracé à partir de la question, pas à partir des données.
Comment évolue une valeur : `plot`, une ligne, x est le temps. Deux mesures sont-elles liées :
`scatter`, un point par patient. Comment est distribuée une mesure : `hist`. Combien
patients dans chaque groupe : `bar`. Comment une mesure se compare-t-elle entre les groupes : `boxplot`.
À quoi ressemble un tableau 2D : `imshow`.
Chacun d'entre eux est une méthode de `ax`, et chacun prend des tableaux numpy.
:::

## Tracés linéaires : évolution

![](img/line.png)

::: notes
Les lignes correspondent aux valeurs x ordonnées : temps, dose, âge. Si les valeurs x ne sont pas ordonnées (patients),
une ligne entre eux ne veut rien dire : utilisez un scatter.
Deux mesures avec des unités différentes obtiennent deux axes partageant x, pas un seul axe avec deux
échelles mélangées.
`marker` indique où se trouvent les mesures réelles : avec une valeur par heure, la ligne entre
deux points sont une interpolation, pas des données.
`ax.axhline(38)` et `ax.fill_between(t, 36.5, 37.5, alpha=0.15)` mettent la référence clinique (seuil, plage normale) sur le
graphique, afin que le lecteur n’ait pas à s’en souvenir.
:::

## Nuages de points : relations

![](img/scatter.png)

::: notes
Un point par patient, deux mesures comme coordonnées.
Une troisième variable peut aller dans la couleur. Une catégorie : un `scatter` appel par groupe, chacun avec
un `label` et `ax.legend()`. Un numéro : `c=values` avec une carte de couleurs, et `fig.colorbar` pour
relisez-le.
Avec des milliers de points, réduisez `s` (taille) et ajoutez `alpha` (transparence) pour que le
les régions deviennent visibles au lieu d’une tache uniforme.
:::

## Histogrammes : distributions

![](img/hist_bins.png)

::: notes
Un histogramme compte les valeurs dans les bacs. Le nombre de bacs change la donne : trop peu cachent le
forme, trop d’entre eux ne montrent que du bruit. Essayez-en plusieurs et dites lequel vous avez gardé.
`bins` accepte également les bords eux-mêmes, par ex. `bins=np.arange(10, 45, 1)` : une barre par IMC
unité, comparable entre les figures.
`density=True` divise par le total, pour comparer des groupes de tailles différentes.
:::

## Barres et box : groupes

![](img/bar_box.png)

::: notes
Une barre est pour un décompte ou un total par groupe : sa hauteur est l'information, donc l'axe y
doit commencer à 0.
Pour comparer une mesure entre groupes, une barre de moyenne cache tout ; une boîte à moustaches
montre la médiane (ligne), les 50 % du milieu (encadré), la plage (moustaches) et les valeurs aberrantes
(cercles).
La durée du séjour est la variable asymétrique classique : la plupart des séjours sont courts, quelques-uns sont très longs.
C'est eux qui tireraient la moyenne ; le boxplot le montre immédiatement.
:::

## Images : tableaux 2D

![](img/imshow.png)

::: notes
`imshow` transforme chaque valeur d'un tableau 2D en pixel, via une carte de couleurs. Une coupe CT est
juste un ensemble numpy d'unités Hounsfield : -1000 correspond à l'air, 0 à l'eau, environ 40 aux tissus mous, plusieurs
cent pour l'os.
`vmin` et `vmax` choisissent les valeurs qui couvrent la carte des couleurs : c'est la « fenêtre » des radiologues
changer toute la journée. Le même tableau montre les poumons ou les tissus mous selon la fenêtre.
Découper le tableau recadre l'image : tout ce qui concerne la session 1 s'applique aux images.
Ajoutez toujours une barre de couleurs avec l'unité : sans elle, les niveaux de gris ne veulent rien dire.
:::

## Cartes de couleurs

![](img/colormaps.png)

::: notes
Une carte de couleurs code un nombre ; l'œil doit le lire comme un nombre.
Les cartes séquentielles (viridis, la valeur par défaut ou grise) passent du foncé au clair : la luminosité augmente
avec la valeur, même imprimée en noir et blanc, et pour les lecteurs daltoniens (environ 1 homme
en 12).
Les cartes divergentes (RdBu) concernent les données avec un centre significatif : changement par rapport à la ligne de base,
corrélation. Réglez `vmin=-v, vmax=v` pour que le centre soit blanc.
jet (arc-en-ciel) crée des bandes qui ne sont pas dans les données, et sa luminosité augmente et diminue :
il figure encore dans de nombreux logiciels médicaux et ne devrait pas figurer dans vos figures.
:::

## Cartes de couleurs

![](img/colormap_choice.png)

::: notes
Un champ lisse (pensez à une carte de perfusion, mL/100 g/min), une fenêtre
(`vmin=0, vmax=80`) : tout ce qui change entre ces huit panneaux c'est la couleur
carte, tout comme tout ce que le lecteur voit. Les données n’ont aucun avantage nulle part ; chaque sonnerie et
chaque bande ci-dessous a été ajoutée par la carte des couleurs.
le gris est la convention pour la tomodensitométrie, l'IRM et les rayons X : les radiologues lisent les niveaux de gris et un
la tranche colorée ne leur semble pas bonne. l'os est la même idée avec une teinte froide.
viridis et magma sont les choix par défaut pour une quantité mesurée (perfusion, dose,
activation, une matrice de corrélation) : la luminosité augmente avec la valeur, donc ils survivent
impression en noir et blanc et daltonisme.
RdBu_r et coolwarm font la différence : post moins pré, patient moins atlas, a
corrélation. Ils ont besoin de `vmin=-v, vmax=v` pour que le blanc soit exactement 0. Sur les données brutes, où
aucune valeur n'est spéciale, ils inventent un centre qui n'existe pas, c'est ce que vous voyez ici.
jet et nipy_spectral placent des bandes et des points lumineux là où les données sont fluides. Ils sont encore
la valeur par défaut dans de nombreux logiciels médicaux ; changez-les.
Règle générale : une quantité croissante, séquentielle (gris, viridis) ; une différence signée,
divergent centré sur 0 ; catégories (étiquettes de segmentation), une carte qualitative telle que
tab10 avec `imshow` et pas de barre de couleurs.
:::

## Sauvegarde

```python
fig.tight_layout()
fig.savefig("fig1.png", dpi=300)
fig.savefig("fig1.pdf")
fig.savefig("fig1.svg")

plt.close(fig)    # in loops
```

::: notes
Le format est choisi par l'extension. PNG est une image : choisissez un `dpi` assez haut pour le
taille finale (300 pour l'impression). PDF et SVG sont des formats vectoriels : les lignes et le texte restent nets
n'importe quel zoom, et les journaux les demandent.
Sauver du code, jamais avec une capture d'écran : la figure est alors reproductible, et régénérante
après une correction des données, c'est une commande.
Dans une boucle qui fait un figure par patient, `plt.close(fig)` libère la mémoire ; sinon
matplotlib les conserve tous et prévient après 20.
:::
