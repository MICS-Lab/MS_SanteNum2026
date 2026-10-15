---
title: |
  Séance 3\
  La ligne de commande
subtitle: "Santé numérique, Mastère Spécialisé · 2026"
author: "Paul Dubois"
date: "Semaine 1, cours"
---

# 1. Pourquoi utiliser un terminal ?

## La plupart des ordinateurs n'ont pas d'écran

![](img/datacenter.jpg)

::: notes
Des rangées de machines, et pas un seul clavier, souris ou moniteur dans la pièce. C'est la NASA
Supercalculateur Columbia, mais c'est aussi chaque salle de serveurs d'hôpital, chaque instance cloud,
et chaque cluster de calcul auquel vous enverrez une tâche.
Personne n’entre et ne clique. Vous atteignez ces machines via le réseau (`ssh`), et quoi
vous répond est une invite de texte. L'interface graphique est l'exception, disponible sur votre
ordinateur portable et presque nulle part ailleurs.
La question n’est donc pas de savoir si la ligne de commande est agréable. C'est la seule interface
ces machines en disposent, et c’est là que résident les données et la puissance de calcul.
Demandez à la salle : à votre avis, où se trouvent réellement les archives d’imagerie d’un hôpital ?
:::

## Terminal, shell, programme, noyau
![](img/terminal_shell.png)

::: notes
Quatre mots que les étudiants utilisent comme synonymes pendant une quinzaine de jours. Résoudre ce problème rapidement permet d'économiser beaucoup
confusion plus tard : "le terminal s'est écrasé" et "le shell est bash" et "ls est un programme"
sont trois déclarations différentes.
Insistez sur la ligne de clôture. Tout ce qui suit (variables, boucles, conditions,
fonctions) est disponible *car* le shell est un langage. L'invite est un REPL.
:::

## L'anatomie d'une commande
![](img/anatomy.png)

::: notes
C'est la diapositive de grammaire ; chaque commande du cahier y obéit.
Deux pièges à nommer maintenant, car les deux mordront dans les exercices :
(1) un espace sépare les arguments, donc un nom de fichier avec un espace contient deux arguments, sauf si
  c'est cité. Les exports de données de santé regorgent de `Patient Records 2024.csv`.
(2) les drapeaux sont sensibles à la casse et ne sont pas universels : `-h` est "l'aide" dans certains outils et
  "lisible par l'homme" chez d'autres. Il n'y a pas de comité.
:::

# 2. Se déplacer et déplacer des données

## Le système de fichiers est un seul arbre
![](img/filesystem.png)

::: notes
Deux idées : il n'y a qu'une seule racine (pas de lecteur `C:`), et tout fichier a deux noms
(absolu et relatif) qui pointent vers la même chose.
Règle générale pour leurs futurs scripts : chemins absolus pour les données qui résident quelque part
chemins fixes et relatifs pour tout ce qui se trouve à l'intérieur du projet, afin que le projet puisse être déplacé,
partagé ou exécuté sur le cluster sans modification.
:::

## Cinq commandes les plus utiles
```bash
# where am I
$ pwd
# go there  (cd .. to parent directory)
$ cd data/ecg
# list files
$ ls -lh
# create a folder
$ mkdir -p results/2026
# copy
$ cp a.csv backup_a.csv
# move / rename
$ mv a.csv new_a.csv
# delete
$ rm new_a.csv
```

::: notes
Tapez-les en direct, lentement, dans un dossier de travail. Laissez-les voir le changement rapide avec
`cd`.
Donnez à l'avertissement `rm` son propre rythme. Ensuite, donnez-leur l'habitude qui les protège réellement.
eux : exécutez d'abord la chose dangereuse comme `ls` (`ls *.tmp`), regardez ce qui correspond, puis
échangez `ls` contre `rm`. Ne faites jamais confiance à un globe que vous n'avez pas imprimé.
:::

## Texte entrant, texte sortant
![](img/pipeline.png)

::: notes
C'est le noyau intellectuel de toute la session, et la raison pour laquelle les outils sont tous
petit. Chaque programme effectue une tâche et parle la même devise : des lignes de texte. Le
le tuyau est ce qui les fait composer.
Construisez l'exemple une étape à la fois à l'écran, affichant le résultat intermédiaire
après chaque `|`. Les élèves se souviennent de la forme une fois qu’ils l’ont vue se rétrécir.
Mentionnez qu'il s'agit exactement du `pandas` chaînage, dix ans de plus et sur les fichiers ce n'est jamais
doit se charger en mémoire.
:::

## Plus de commandes
| Commande | Est-ce que |
|---|---|
| `cat` / `head` / `tail` | imprimer un fichier, ses premières, ses dernières lignes |
| `wc -l` | compter les lignes (lignes dans un CSV) |
| `grep 'ICU'` | garder les lignes qui correspondent |
| `cut -d, -f2` | garder une colonne |
| `sort` / `uniq -c` | commander et compter les répétitions |
| `find . -name '*.csv'` | lister les fichiers correspondant à un modèle, de manière récursive |

::: notes
N'essayez pas de les enseigner de manière exhaustive (le cahier fait cela). Ici, établissez simplement
que la boîte à outils est petite et que chacun est un verbe que vous pouvez rechercher.
`sort | uniq -c` est le `value_counts()` du shell ; dis ça à voix haute, ça convertit
tous ceux qui connaissent déjà les pandas.
:::

# 3. Contrôle de version

## Quel fichier est le dernier ?

![](img/git_why.png)

::: notes
Tout le monde dans la pièce a un dossier comme celui de gauche. Il échoue exactement quand il
compte : un critique demande quelle version du script a produit le tableau 2, et personne ne le sait.
git remplace les copies par un fichier et un historique. Chaque changement est enregistré avec qui a fait
il, quand et un message qui explique pourquoi. Dans un cadre réglementé (une étude clinique, un
Appareil marqué CE), cette traçabilité n'est pas une commodité : c'est ce que demande un audit.
git est un programme en ligne de commande : tout ce qui figure dans les deux premières sections s'applique.
:::

## Création d'un instantané

![](img/git_areas.png)

::: notes
Le seul modèle mental pour réussir. Vous modifiez les fichiers dans le dossier de travail comme d'habitude.
`git add` choisit les modifications qui seront apportées à l'instantané suivant (la zone de préparation). `git commit`
enregistre cet instantané dans le référentiel, le dossier caché `.git/`.
Pourquoi l'étape intermédiaire : vous avez modifié trois fichiers mais seulement deux appartiennent au même correctif. Scène
ces deux-là, validez, puis mettez en scène et validez le troisième avec son propre message.
`git status` est la commande à taper en cas de perte : elle indique ce qu'il y a dans chaque zone, et
suggère généralement la commande suivante.
:::

## Boucle quotidienne

```bash
$ git init
$ git status
$ git diff
$ git add clean.py
$ git commit -m "Drop rows without age"
$ git log
```

::: notes
Démo live dans un dossier scratch : `git init`, créer un fichier, `status`, `add`, `status`,
`commit`, modifier, `diff`, valider à nouveau, `log`.
La première fois, git vous demande qui vous êtes : `git config --global user.name "..."` et
`user.email`. Chaque commit porte ce nom.
Un bon message complète la phrase "ce commit va..." : "Supprimer les lignes sans âge",
pas "mettre à jour" ou "réparer". Un changement logique par commit.
:::

## Histoire et succursales

![](img/git_history.png)

::: notes
Chaque commit possède un identifiant (un hachage, raccourci à 7 caractères) et pointe vers le
s'engager avant lui : l'histoire est une chaîne.
Une branche n'est qu'un nom sur une validation, qui avance au fur et à mesure de votre validation. `git switch -c new-plot`
en commence un : essayer une idée sans toucher au `main`. Si cela fonctionne, `git merge new-plot` apporte
il revient; sinon, supprimez la branche et `main` ne l'a jamais su.
`git switch` / `git checkout <hash>` déplace HEAD et les fichiers du dossier deviennent
correspondre à cet instantané. Rien n'est perdu : chaque commit est toujours là.
:::

## Local et distant

![](img/git_remote.png)

::: notes
git fonctionne entièrement sur votre machine : commit dans un train, sans réseau. Une télécommande est
une autre copie du référentiel, généralement sur GitHub (ou GitLab, ou sur le propre de l'hôpital)
serveur). `git clone` fait votre copie une fois ; `git push` envoie vos nouveaux commits ;
`git pull` récupère les commits des autres et les fusionne dans les vôtres.
GitHub ajoute ce que git n'a pas : une page web pour le projet, des tickets pour suivre les bugs,
demandes d'extraction pour examiner une modification avant sa fusion. Le matériel de cours y réside.
Deux personnes éditant les mêmes lignes produisent un conflit : git marque les deux versions dans le
fichier, vous choisissez, puis validez. C'est un événement normal, pas une erreur.
:::

## Travailler avec GitHub

```bash
$ git clone https://github.com/org/repo
$ cd repo

# ... edit, add, commit ...

# get the others' work
$ git pull
# publish yours
$ git push
```

::: notes
La boucle de collaboration quotidienne : tirez avant de commencer, poussez lorsque vous avez terminé.
Authentification : GitHub n'accepte plus votre mot de passe sur la ligne de commande. Utiliser un SSH
key (`ssh-keygen`, puis collez la clé publique dans les paramètres GitHub) ou `gh auth login`.
C'est un bon exercice en soi, et il réutilise `ssh` de la première section.
Pour un nouveau projet : créez le dépôt vide sur GitHub, puis `git remote add origin
<url>` and `git push -u origin main` depuis votre dossier existant.
:::

## Ce qu'il faut ignorer

```bash
# .gitignore
data/          # patient data
*.csv
.env           # passwords, API keys
.venv/         # re-created by uv sync
__pycache__/
```

::: notes
La règle des données de santé de cette session. Un commit est éternel : supprimer un fichier ultérieurement
commit le laisse dans l’historique, lisible par quiconque clone. Un dossier patient poussé vers
un référentiel GitHub public constitue une violation de données au sens du RGPD et doit être signalé.
`.gitignore` répertorie les modèles que git ne doit jamais suivre : données, secrets, fichiers générés.
Écrivez-le en premier, avant le premier `git add .`.
Le référentiel contient le code qui lit les données et un fichier README indiquant où se trouvent les données.
vies et qui peut y accéder. Les données elles-mêmes restent sur le serveur sécurisé.
:::

# 4. Garder le code lisible : ruff

## Un style, décidé par un outil

```bash
$ uv venv
# create .venv
$ source .venv/bin/activate # unix
> .venv\Scripts\activate # windows

$ uv pip install ruff
# or: uv add --dev ruff

$ ruff --version
```

::: notes
`ruff` est un formateur *et* un linter pour Python, des mêmes personnes que `uv`, donc il
s'installe de la même manière et s'exécute tout aussi rapidement (un projet entier en moins d'une seconde).
Deux métiers, qui méritent d'être séparés dans leur tête :
(1) le formateur réécrit la disposition de votre code : indentation, guillemets, sauts de ligne,
  espaces autour des opérateurs. Cela ne change jamais ce que fait le code.
(2) le linter lit le code et signale les erreurs : un import inutilisé, une variable
  attribué et jamais lu, un nom qui n'existe pas.
Pourquoi s’embêter dans un projet de données de santé ? Parce qu'une différence devrait montrer ce que vous avez modifié, pas
qui l'a reformaté. Avec un formateur, `git diff` ne contient que de vrais changements, et le code
la critique cesse d'être un argument sur les espaces.
Remarque `uv add --dev ruff` : il s'agit d'un outil de développement, pas d'une dépendance de l'analyse, donc
il appartient au groupe de développement de `pyproject.toml`.
Si `ruff` n'est pas sur le chemin, exécutez-le via uv : `uv run ruff --version`.
:::

## Formatez et vérifiez

```bash
# format one file
$ ruff format clean.py
# format everything, recursively
$ ruff format .

# report, but change nothing
$ ruff format --check .
# lint: find likely mistakes
$ ruff check .
# lint, and fix what is safe
$ ruff check --fix .
```

::: notes
Trois commandes à retenir, et la différence entre elles est tout l'intérêt.
`ruff format <path>` réécrit le fichier sur place et imprime `1 file reformatted`. Un
le répertoire (`.` est celui actuel) signifie chaque `.py` fichier en dessous ; fichiers répertoriés dans
`.gitignore` sont ignorés, donc `.venv/` n'est pas touché.
`--check` est la version en lecture seule : elle répertorie les fichiers qui *seraient* modifiés et se termine avec
un statut non nul s'il y en a. C'est exactement ce que vous mettez dans une vérification pull-request
ou un git hook : il échoue la construction au lieu de modifier silencieusement le code de l'auteur.
`ruff check` est le linter, une commande différente de `format` ; `--fix` s'applique uniquement au
les services correctionnels que Ruff considère comme sûrs.
Conseil pratique : lancez `ruff format .` une fois au début d'un projet, validez-le comme
"format avec collerette" seul, et à partir de là, chaque différence reste petite. Le faire dans le
au milieu d'une branche de fonctionnalité produit un commit de 400 lignes qui cache la seule ligne qui
compte.
Démonstration en direct le `clean.py` depuis le notebook : `ruff format --check clean.py`, puis
`ruff format clean.py`, puis `git diff`.
:::

## Un contrôle des peluches, sûr et dangereux

```python
import os
# F401 unused import   -> safe fix
import pandas as pd

def mean_hr(path):
    df = pd.read_csv(path)
    n = len(df)
    # F841 unused variable -> unsafe fix
    return df["hr"].mean()

```

```bash

$ ruff check vitals.py
# Found 2 errors:
# * 1 fixable with `--fix`
# * 1 unsafe fix available with `--fix --unsafe-fixes`
```

::: notes
Deux vraies découvertes sur sept lignes, et elles ne sont pas également sûres à réparer.
`F401 os imported but unused` : l'import ne fait rien, donc la suppression de la ligne ne peut pas
changer le résultat. Marques de collerette qui corrigent **safe** et `ruff check --fix vitals.py`
le supprime pour vous (et trie les importations restantes, `I001`).
`F841 local variable n is assigned to but never used` : ici, la solution de Ruff consiste à laisser tomber le
`n =` et gardez l'appel, `len(df)`. Cela le marque **dangereux**, car le côté droit
pourrait faire quelque chose : `n = log_access(patient_id)` serait toujours appelé, mais
`n = df.pop("hr")` modifie `df`, et supprimer toute la ligne modifierait le résultat.
Ruff refuse de deviner. Donc `--fix` le laisse tranquille et vous dit qu'un `--unsafe-fixes` est
disponible; vous ne l'obtenez qu'avec `ruff check --fix --unsafe-fixes .`, et puis vous lisez
le diff avant de s'engager.
La règle pour la salle : `--fix` peut fonctionner sans surveillance, même dans un crochet. `--unsafe-fixes` est
quelque chose que vous exécutez vous-même, sur un arbre de travail propre, et vérifiez avec `git diff`.
Notez également que F841 est souvent un vrai bug, pas un désordre : la variable que vous avez calculée et oubliée
pour revenir, ou une faute de frappe où vous avez attribué `mena` et utilisé `mean`. Ne supprimez pas automatiquement le
preuve, lisez-la.
:::
