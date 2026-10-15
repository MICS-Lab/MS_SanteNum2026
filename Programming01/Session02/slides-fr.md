---
title: |
  Séance 2\
  Conditions, boucles et classes
subtitle: "Santé numérique, Mastère Spécialisé · 2026"
author: "Paul Dubois"
date: "Semaine 1, cours"
---

# 1. Prendre des décisions

## `if` / `elif` / `else`

```python
temp = 38.4

if temp >= 39:
    print("high fever")
elif temp >= 38:
    print("fever")
else:
    print("no fever")
```

::: notes
La session 1 a donné les valeurs ; cette session donne le contrôle : exécutez ce code seulement de temps en temps,
exécutez ce code plusieurs fois et donnez un nom à un bloc de code.
Trois éléments de syntaxe, et ils sont les mêmes pour chaque bloc en Python : une fin de ligne
avec deux points, puis un bloc en retrait. Quatre espaces, toujours les mêmes. L'indentation est
pas la décoration, c'est la syntaxe : c'est ce qui indique à Python où le bloc s'arrête.
`if` prend tout ce qui est vrai ou faux, y compris la véracité de la session 1
(`if heart_rates:`). La comparaison `>=` produit un booléen ; `=` serait une mission et
une erreur de syntaxe ici.
:::

## Ordre des tests

![](img/branching.png)

::: notes
Avec `elif`, Python teste de haut en bas et s'arrête au premier vrai test : le reste
n’est jamais évalué. Ainsi, chaque `elif` signifie silencieusement "et aucun des tests ci-dessus ne correspond",
c'est exactement pourquoi `sbp < 120` n'a pas besoin de répéter `and sbp >= 90`.
Le bug classique est à droite : un test plus large placé en premier avale les plus étroits,
et chaque patient en dessous de 130 en sort « élevé ». Rien ne plante, les chiffres sont juste
faux, ce qui est un type de bug dangereux.
La règle : pour les seuils, allez du plus étroit au plus large, et laissez `else` attraper quoi
est laissé.
:::

# 2. Répéter le travail

## `for` boucle

![](img/for_anatomy.png)

::: notes
Lisez-le tel que la phrase anglaise est la suivante : "pour chaque fréquence cardiaque dans les fréquences cardiaques, faites ceci".
Le nom de gauche est créé par la boucle et prend une nouvelle valeur à chaque tour ; il n'y a pas
compteur à initialiser et aucune longueur pour réussir.
Pointez sur le bloc en retrait : il s'exécute une fois par élément, cinq fois ici, et ce qui ne l'est pas
indented s'exécute une fois, après la boucle. Le bug débutant le plus courant de la session est une ligne
qui entre ou sort accidentellement du corps.
Venant d'une autre langue, ils voudront `for i in range(len(xs)): xs[i]`. Montre-leur
la forme directe une fois et ils y reviennent rarement.
:::

## `range` et `enumerate`

![](img/loop_helpers_a.png)

::: notes
`range(stop)`, `range(start, stop)`, `range(start, stop, step)` : la boucle comptée, utilisée
lorsque le nombre de tours est important et que les objets ne le sont pas. Notez que `range(5)` s'arrête à 4,
comme une tranche, et ce `range` ne construit rien : il distribue les nombres un à un,
c'est pourquoi `range(10_000_000)` est instantané et ne coûte aucune mémoire.
`enumerate` quand on a besoin de la position ainsi que de la valeur : ça donne une paire à chaque tour,
décomposé en deux noms exactement comme `a, b = 1, 2` dans la session 1. Commencez ailleurs avec
`enumerate(hrs, start=1)` quand on veut compter à partir de 1 pour un lecteur humain.
S'ils se retrouvent à écrire `for i in range(len(hrs))` puis `hrs[i]`, `enumerate`
c'est ce qu'ils voulaient.
:::

## `zip` et `.items()`

![](img/loop_helpers_b.png)

::: notes
`zip` parcourt deux (ou plus) séquences pas à pas : identifiants et températures, tailles et poids,
mesuré et prédit. Encore une paire par tour, décomposée en deux noms.
Un piège qui mérite d'être dit à voix haute : `zip` s'arrête à la séquence la plus courte, en silence. Si les identifiants
et les températures n'ont pas la même longueur, les températures supplémentaires tombent sans
mot, alors vérifiez d'abord `len` lorsque les deux proviennent de fichiers différents.
`.items()` fait la même chose pour un dictionnaire, en donnant la clé et la valeur ; `.keys()` et
`.values()` existent lorsqu'un seul d'entre eux est nécessaire. Itérer un dict donne directement le
clés seules, ce qui est une surprise courante.
Ces quatre assistants couvrent presque toutes les boucles qu’ils écriront cette année.
:::

## Accumuler un résultat

```python
total = 0
for hr in heart_rates:
    total = total + hr

mean = total / len(heart_rates)
```

::: notes
Le modèle d'accumulateur : une variable créée *avant* la boucle, mise à jour *à l'intérieur* de celle-ci, utilisée
*après* ça. Somme, décompte, maximum, une liste en construction : ils ont tous cette forme.
Créez-le avant la boucle, sinon le nom n'existe pas encore ; `total = 0` pour une somme,
`best = values[0]` pour un maximum (et non 0, qui casse sur des valeurs négatives).
Ils le feront à la main dans le cahier, puis rencontreront `sum`, `max` et `np.mean`, qui font
la même chose plus rapidement et avec moins de marge d’erreur. L'écrire une fois à la main est ce qui fait
le raccourci lisible par la suite.
:::

## `while` : nombre d'itérations inconnu

![](img/while_loop.png)

::: notes
Une boucle `for` parcourt une collection finie ; une boucle `while` pose une question avant chaque tour
et s'arrête lorsque la réponse est Faux. Utilisez-le lorsque le nombre de tours dépend du
calcul lui-même : une demi-vie tombant sous un seuil, un solveur convergeant, une lecture
jusqu'à la fin d'un flux.
Chaque boucle while a besoin de trois choses, et oublier la troisième est l'infini classique
boucle : un état initial, une condition qui le mentionne, et un corps qui le modifie.
Le bouton d'interruption ( ■ ) est leur porte de sortie ; mentionnez-le avant d’en avoir besoin.
:::

## `break` et `continue`

![](img/break_continue.png)

::: notes
`break` quitte immédiatement la boucle : la recherche est terminée, les éléments restants ne sont jamais
regardé. C'est ainsi que vous trouvez la première valeur anormale sans analyser le reste.
`continue` abandonne uniquement le tour en cours et passe au suivant : l'idiome pour sauter
valeurs manquantes, ce qui représente l'essentiel du travail dans les exportations réelles.
Les deux fonctionnent en `for` et en `while`. Conservez-les pour les cas qui se lisent comme « stop » ou « saut » :
imbriqués dans trois niveaux de `if`, ils deviennent illisibles.
:::

## Compréhensions

![](img/comprehension.png)

::: notes
Une compréhension est la même boucle écrite comme une seule expression : quoi garder, d'où cela vient
de, et éventuellement lesquels. Python le lit dans cet ordre, et il devrait en être de même.
C'est la manière idiomatique de transformer une liste en une autre liste, et elle apparaît constamment
en code réel, ils doivent donc être capables d'en lire un même s'ils préfèrent écrire des boucles.
La limite : une compréhension construit une collection. Une boucle qui imprime, écrit un fichier ou
les appels à un service restent une boucle. Et une compréhension avec deux `for` et trois `if` devrait aller
redevenu une boucle.
:::

## Fonctions

![](img/function_anatomy.png)

::: notes
`def` crée une fonction ; l'appeler exécute le corps avec les arguments liés au
paramètres, et `return` renvoie une valeur à l'appelant.
Insistez sur la différence entre imprimer et renvoyer : `print` montre une valeur à un humain
et ne donne rien en retour, `return` produit une valeur que le reste du programme peut utiliser. Un
la fonction qui imprime son résultat ne peut pas être réutilisée.
Les arguments par défaut (`skip_none=True`) donnent une option sans forcer chaque appelant à réfléchir
à ce sujet. Les arguments de mots clés sur le site d'appel (`mean(values, skip_none=False)`) valent
les caractères supplémentaires : dans six mois, cette ligne dit toujours ce qu'elle fait.
Portée en une phrase : les noms créés à l'intérieur de la fonction disparaissent à son retour.
:::

# 3. Objets et classes

## Une classe est un plan

![](img/class_anatomy.png)

::: notes
Ils utilisent des objets depuis la séance 1 sans le mot : un `str` a `.upper()`, un
la liste a `.append()`. Une classe est la façon dont vous définissez votre propre type, pour les données qui voyagent
ensemble.
`__init__` s'exécute à la création et stocke les attributs sur `self` ; `self` est simplement le
objet sur lequel la méthode a été appelée, et c'est le premier paramètre de chaque méthode. `p.bmi()`
est juste `Patient.bmi(p)`.
Les noms avec des traits de soulignement doubles sont des hooks que Python appelle pour vous : `__init__` à la création,
`__repr__` lorsque l'objet est affiché, `__len__` pour `len(obj)`. Définir `__repr__`
au début, cela transforme un `<object at 0x7f...>` illisible en quelque chose avec lequel ils peuvent déboguer.
Deux objets de la même classe sont indépendants : changer `q.weight` laisse `p` intact.
:::

## Dictionnaire ou classe ?

```python
# dict: data only
p = {"id": "P001", "age": 54}
p["age"]


# class: data + behaviour
class Patient:
    def bmi(self): ...
p.bmi()
```

::: notes
Réponse honnête : pour une poignée de champs lus une fois à partir d'un CSV, un dict suffit, et c'est
ce que les pandas leur donneront de toute façon.
Une classe gagne sa place lorsque le comportement appartient aux données (un IMC calculé à partir de la
propres champs du patient), lorsque la même forme est créée plusieurs fois, ou lorsque vous souhaitez une
garantir que chaque objet a les mêmes attributs, qu'un dict ne vous donne jamais : un
une faute de frappe dans une clé crée une nouvelle clé au lieu d'une erreur.
:::

## Héritage

![](img/inheritance.png)

::: notes
`class InPatient(Patient)` signifie « un patient hospitalisé est un patient plus une chambre ». La classe en
brackets est le parent (classe de base, superclasse) ; le nouveau est l'enfant ou la sous-classe.
Tout ce qui est défini sur `Patient` est disponible sur un `InPatient` sans être écrit
encore une fois : les attributs définis dans `__init__`, `bmi()`, `add_heart_rate()`, `__repr__`.
`super().__init__(id, age, weight, height)` appelle le constructeur du parent, donc le partage
les attributs sont définis en un seul endroit, par la classe qui les possède. Oublier cet appel est le
erreur classique : l'objet est créé, puis `i.bmi()` échoue avec
`AttributeError: 'InPatient' object has no attribute 'weight'`, parce que personne n'a jamais réglé
ça.
`isinstance(i, Patient)` est vrai, et c'est là tout l'intérêt : code écrit pour les patients
fonctionne inchangé sur les patients hospitalisés. L’inverse est faux ; un `InPatient` est un cas particulier de
`Patient`, et non l'inverse. Préférez `isinstance(x, Patient)` à
`type(x) == Patient`, qui répond False pour chaque sous-classe et brise tranquillement l'idée.
Un avertissement : l’héritage est tentant et souvent erroné. Utilisez-le lorsque la phrase « X est un Y » est
littéralement vrai; lorsque X *a* simplement un Y, stockez-le plutôt comme attribut.
:::

## Classe parentale

```python
class Patient():
    def __init__(self, id, age, weight, height):
        self.id = id
        self.age = age
        self.weight = weight
        self.height = height

    def __repr__(self):
        return f"Patient {self.id}"

i = Patient("P003", 71, 95.2, 1.70)
i.bmi() # -> computes 95.2^2 / 1.70
```

## Classe enfant

```python
class InPatient(Patient):
    def __init__(self, id, age, weight, height, room):
        super().__init__(id, age, weight, height)
        self.room = room

    def __repr__(self):
        return f"InPatient {self.id}, room {self.room}"

i = InPatient("P003", 71, 95.2, 1.70, room=12)
i.bmi()      # not on InPatient -> found on Patient
i            # InPatient('P003', room 12)
```

::: notes
La règle est une ligne : Python recherche d'abord le nom dans la propre classe de l'objet, puis dans
son parent, puis sur *son* parent, jusqu'à `object` ; le premier trouvé gagne.
`i.bmi()` n'est pas défini sur `InPatient`, donc Python arrive et exécute celui sur `Patient`.
`repr(i)` est défini sur les deux, donc la version de l'enfant l'emporte : c'est *prédominant*.
Une méthode surchargée peut toujours réutiliser celle qu'elle a remplacée : `super().__repr__()` à l'intérieur du
child appelle la version du parent, c'est ainsi que vous étendez le comportement au lieu de le copier.
Même idée que `super().__init__`, qui n'est rien de plus qu'un `__init__` remplacé
appelant l'original.
Le gain est le *polymorphisme* : une boucle sur une liste mixte de `Patient` et `InPatient`
les objets appellent `p.bmi()` sur chacun, et chaque objet exécute la bonne version. Aucun test sur le
tapez n'importe où, ce qui est exactement l'échelle `if` qui pourrit lorsqu'un nouveau cas apparaît.
Habitude de débogage : lorsqu'une méthode ne fait pas ce qu'elle attend, demandez de quelle classe elle provient.
`type(i).__mro__` imprime l'ordre de recherche, `help(InPatient)` montre ce qui a été hérité et
ce qui a été redéfini.
:::

<!--
## Les méthodes que Python appelle pour vous

| Méthode | Appelé par | Utilisation typique |
|---|---|---|
| `__init__(self, ...)` | `Patient("P001", 54)` | stocker les attributs |
| `__repr__(self)` | l'objet affiché, `print` | un `Patient('P001', 54 y)` lisible |
| `__len__(self)` | `len(ward)` | combien de patients |
| `__eq__(self, other)` | `a == b` | même identifiant de patient |
| `__getitem__(self, k)` | `ward[0]` | le rendre indexable |

::: notes
Les noms à double trait de soulignement ("dunder") ne sont pas une syntaxe magique : ce sont des méthodes ordinaires
que Python appelle en votre nom lorsqu'un opérateur ou un élément intégré est utilisé. Les définir est
comment votre classe se comporte comme un type intégré.
`__repr__` est celui qu'il faut écrire à chaque fois, dès le premier jour. Sans cela, le carnet affiche
`<__main__.Patient object at 0x7f3c...>`, qui ne leur dit rien ; avec lui, déboguer un
la liste des objets devient lisible. Mettez-y les champs d'identification, pas tout.
`__len__` doit renvoyer un entier, et il décide également de la véracité : avec `__len__` défini,
une salle vide est fausse, donc `if ward:` fonctionne (session 1 à nouveau).
`__eq__` mérite une mise en garde dans les données de santé : deux mesures du même patient
ne sont pas le même objet, et l'égalité sur les floats est toujours une mauvaise idée. Comparez les identifiants.
Il ne leur est pas demandé de mémoriser la liste, mais seulement d'en reconnaître le modèle : si un
devraient travailler sur leur objet, il y a un problème pour cela.
::: -->
