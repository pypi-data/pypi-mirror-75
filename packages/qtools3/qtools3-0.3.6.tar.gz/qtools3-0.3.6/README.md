# `qtools3` - Questionnaire Tools for ODK

This software `qtools3` provides tools and utilities for dealing with PMA 
questionnaires. It converts the XLSForms to XML and then does all appropriate 
edits. It also can be used as a simple XLSForm Offline converter.

The software `qtools3` is an upgrade from 
[`qtools2`][qtools2]. The primary purpose for this 
upgrade is to port the software from Python 2 to Python 3. This was made 
possible because the [community's PyXForm][pyxform]
added Python 3 support in 2018.

[qtools2]: https://github.com/jkpr/QTools2
[pyxform]: https://github.com/XLSForm/pyxform

## Pre-requisites

The software `qtools3` relies on Python 3 for core functionality and Java for
ODKValidate. The steps to install are

* Install the most recent version of the [Java JRE][jre].
* Install [Python 3.6][python] or higher.

Note: the author uses [Homebrew][brew] for Python installation on Mac.

[jre]: http://www.oracle.com/technetwork/java/javase/downloads/index.html
[python]: http://www.python.org/downloads/
[brew]: http://brew.sh/

## Windows-specific steps

Some difficulties arise if `python` and `pip` are not be added automatically 
to the `PATH` upon installation. For instructions on how to do this, consult
[this document][path].

[path]: https://www.dropbox.com/s/01uoge5pt7yz0ti/Python%20for%20Windows%20Users.docx?dl=0

Open `CMD` (click start menu, type `CMD`, press enter).

```
cd C:\Python36\Scripts
```

Continue with installation or upgrade...

## Installation

NOTE: Windows users start with the _**Windows-specifc steps**_ section.

On a terminal or CMD, run

```
python3 -m pip install qtools3
```

For the latest and greatest, install directly from github

```
python3 -m pip install https://github.com/PMA-2020/qtools3/zipball/master
```


## Command-line usage

Besides being the workhorse of `qtools3`, the module `qtools3.convert` also provides a command-line utility. New-style linking (with all instructions contained inside the XLSForm) is now the default. Old-style linking (line-by-line manual XML editing instructions) is removed. To see help files and usage, run in the terminal

```
python -m qtools3.convert --help
```

#### Quick-start guide

| Type of conversion | Command |
| ------------------ | ------- |
| PMA form conversion                                   | `python -m qtools3.convert FILENAME [FILENAME ...]`    |
| XLSForm-Offline equivalent, convert and validate      | `python -m qtools3.convert -ril FILENAME [FILENAME ...]`     |

#### Options
| Short Flag | Long Flag | Description |
| --- | --- | --- |
| -r | --regular | This flag indicates the program should convert to XForm and not try to enforce PMA-specific naming conventions or make linking checks for HQ and FQ. |
| -p | --preexisting | Include this flag to prevent overwriting pre-existing files. |
| -n | --novalidate | Do not validate XML output with ODK Validate. Do not perform extra checks on (1) data in undefined columns, (2) out of order variable references. |
| -i | --ignore_version | Ignore versioning in filename, form_id, form_title, and save_form. In other words, the default (without this flag) is to ensure version consistency. |
| -l | --linking_warn | Produce warnings for incorrect linking directives. Default is to raise an exception and halt the program. |
| -d | --debug | Show debug information. Helpful for squashing bugs. |
| -e | --extras | Perform extra checks on (1) data in undefined columns and (2) out of order variable references. |
| -s | --suffix | A suffix to add to the base file name. Cannot start with a hyphen ("-"). |

## Extras

### Translation Regex Mismatches
These `qtools3` conversion warning messages appear whenever there is a discrepancy between translations with respect to numbering, i.e. `'[0-9]+'`, and/or variables, i.e. `'${...}'`.

*Example - Numbering Mismatch*

In this example, the warning `'[0-9]+'` will appear, because "0" is not the same things as "zero". To fix this, please ensure that ALL languages use only arabic numerals (e.g. 1, 2, 3...), or only word-based numbering (e.g. one, two, three...).
  * English: Please enter 0.
  * Bad Pidgin English: Please enter zero.

*Example - Variable Mismatch*

ODK variables should never be translated. If the main language shows "${months}", all language translations should also show "${months}". Of course, what the user sees on the phone will still be translated.
  * English: Enter ${months}.
  * Bad French: Entrez ${mois}.

*Example - Variable Mismatch*

Translations should use all variables that the English uses.
  * English: There are ${hh_count} people in the household
  * Bad Pidgin English: There are (ODK will fill in a count) people in the household

## Updates

NOTE: Windows users start with the _**Windows-specifc steps**_ section. To install `qtools3` updates, use

```
python3 -m pip install qtools3 --upgrade
```

For the latest and greatest, replace `master` in the URLs above with `develop`.

Every once in a while, it will be necessary to update `pmaxform3`. To do this, use

```
python3 -m pip install pmaxform3 --upgrade
```

# Suggestions and Gotchas

- Check the version in the terminal to see if a program is installed.
- Check Java version with `javac -version`
- Check Python version with `python -V`.
- Check pip version with `pip -V`.
- Another executable for Python is `python3`.
- Another executable for `pip` is `pip3`.
- The most recent Java is not required, but successful tests have only been run with Java 1.6 through Java 1.8.
- A dependency of `pmaxform` is `lxml`, which can cause problems on Mac. If there are problems, the best guide is on [StackOverflow][8].
- During installation of `pmaxform` on Mac, the user may be prompted to install Xcode's Command Line Tools. This should be enough for `lxml`.
- `qtools3` may run without Java. Java is only needed for ODK Validate, which can be bypassed by using the "No validate" option.
- Xcode 9 presents issues with missing header files. If at all possible, install Xcode 8.

[8]: http://stackoverflow.com/questions/19548011/cannot-install-lxml-on-mac-os-x-10-9

---


# QTools2: Outils de questionnaire pour ODK

Qtools2 fournit des outils et des utilitaires permettant de traiter les questionnaires PMA2020. Il convertit les XLSForms en XML, puis effectue toutes les modifications appropriées. Il peut également être utilisé comme un convertisseur XLSForm Offline simple.

Le code est nécessairement écrit pour Python 2 car il dépend d'un embranchement du [PyXForm de la communauté] [1a] (l’embranchement s'appelle [pmaxform] [1b]) pour convertir les documents MS-Excel en XML. Nous devons juste apprendre à vivre avec cette contrariété.

[1a]: https://github.com/XLSForm/pyxform
[1b]: https://github.com/jkpr/pmaxform


## Conditions préalables

QTools2 repose sur Python 2 pour les fonctionnalités principales et Java pour ODKValidate. Les étapes pour installer sont

* Installez la version la plus récente de [Java] [2] (actuellement 1.8). ~~ Le JRE ou le JDK devrait fonctionner. ~ Seul le JDK fonctionnait lors du dernier test sur Mac (mars 2017).
* Installez [Python 2.7] [3].

Remarque: l'auteur utilise [Homebrew] [4] pour l'installation de Python sur Mac.

[2]: http://www.oracle.com/technetwork/java/javase/downloads/index.html
[3]: http://www.python.org/downloads/
[4]: http://brew.sh/


## Windows-specific steps 

Some difficulties arise if `python` and `pip` are not be added automatically to the `PATH` upon installation. Open `CMD` (click start menu, type `CMD`, press enter). Naviagate to your `pip` executable, probably here:

```
cd C:\Python27\Scripts
```

Continue with installation or upgrade...

## Installation 

NOTE: Windows users start with the _**Windows-specifc steps**_ section. This package uses a modified version of `pyxform` called `pmaxform` because the PyXForm project thus far has refused to accept this author's pull requests for some simple improvements. Therefore, installation requires *two* commands instead of *one*. Open CMD or Terminal and install relevant packages **separately**, and **in order**

First,
```
pip install https://github.com/jkpr/pmaxform/zipball/master
```
Second,
```
pip install https://github.com/jkpr/QTools2/zipball/master
```

For the latest and greatest, replace `master` in the URLs above with `develop`.


## étapes spécifiques à Windows

Certaines difficultés surviennent si `python` et` pip` ne sont pas ajoutés automatiquement au `PATH` lors de l'installation. Ouvrez `CMD` (cliquez sur le menu de démarrage, tapez` CMD`, appuyez sur Entrée). 

Accédez  à votre exécutable `pip`, probablement ici:

```
cd C: \ Python27 \ Scripts
```

Continuer l'installation ou la mise à niveau ...

## Installation

REMARQUE: les utilisateurs de Windows commencent par la section _**Etapes Spécifiques Windows**_. Ce package utilise une version modifiée de `pyxform` appelée` pmaxform` car le projet PyXForm a jusqu'à présent refusé d'accepter les demandes d'extraction de cet auteur pour certaines améliorations simples. Par conséquent, l'installation nécessite *deux* commandes au lieu d’ *une*. Ouvrez CMD ou Terminal et installez les packages pertinents **séparément** et **dans l'ordre**

Premièrement 
```
pip installer https://github.com/jkpr/pmaxform/zipball/master
```
Deuxièmement 
```
pip installer https://github.com/jkpr/QTools2/zipball/master
```

Pour les plus récents et les meilleurs, remplacez «master» dans les URL ci-dessus par «developer».



# Usage


Après l'installation, le code capable de convertir des  XLSForms est enregistré dans la bibliothèque de codes de Python. Cela signifie que n'importe où on peut accéder à Python, ains qu’a `qtools2`.

Pour utiliser `qtools2`, il y a deux manières principales. La méthode la plus simple consiste à pointer et à cliquer sur un fichier spécifique ([exemple de fichier spécifique] [5]) enregistré dans n’importe quel dossier, tel que Downloads, pour que Python puisse l’exécuter. L'autre façon consiste à utiliser la ligne de commande.

[5]: https://raw.githubusercontent.com/jkpr/QTools2/master/scripts/pma-convert.py

## Meilleure manière d'utiliser `qtools2` pour les formulaires PMA2020

Le moyen le plus simple d'utiliser `qtools2` est d'utiliser un fichier du dossier` scripts` [de ce référentiel] [6]. Pour télécharger un script, cliquez sur son lien, puis sur "Raw", puis enregistrez le contenu (dans le navigateur, File> Save). Le tableau ci-dessous explique ce qui est disponible.


| Nom du script | But |
| ------------- | --- |
| `xlsform-convert.py` | Convertir un ou plusieurs *types* de XLSForm avec une interface graphique. |

Windows associe généralement les fichiers `.py` à l'exécutable Python. Ainsi, un utilisateur Windows ne devrait avoir besoin que de double-clic sur l'icône du fichier de script. Cela démarre l’interprétre Python et lance le code.
 
Sur un Mac, faire un double-clic sur un fichier `.py` ouvre généralement un correcteur de texte. Pour exécuter le fichier en tant que code, faire un clic droit sur l'icône du fichier de script, puis sélectionnez "Ouvrir avec> Python Launcher (2.7.12)". Le numéro de version Python peut être différent.


### Alternative

Si ce qui précède est trop difficile, il est possible d’obtenir la même fonctionnalité d’une manière différente. Ouvrez une session interactive Python (peut-être ouvrir IDLE, peut-être ouvrir Terminal et taper `python`). Ensuite, copiez et collez le même texte qui se trouve dans le script souhaité dans l'interprète, appuyez sur "Enter", et le tour est joué.


[6]: https://github.com/jkpr/QTools2/tree/master/scripts
[7]: https://gumroad.com/l/xlsform-offline

## Utilisation de la ligne de commande

En plus d'être le bourreau du travail de `qtools2`, le module` qtools2.convert` fournit également un utilitaire de ligne de commande. La liaison de style nouveau (avec toutes les instructions contenues dans le XLSForm) est maintenant la valeur par défaut. La liaison de type ancien (instructions d’édition XML manuelle, ligne par ligne) est supprimée. Pour voir les fichiers d’aide et leur utilisation, exécutez-le dans le terminal.

```
python -m qtools2.convert --help
```

#### Guide de démarrage rapide

| Type de conversion | Commande |
| ------------------ | ------- |
| Conversion de formulaire PMA | `python -m qtools2.convert FILENAME [FILENAME ...]` |
| convertir et valider des équivalents de XLSForm-Offline, | `python -m qtools2.convert -ril FILENAME [FILENAME ...]` |

#### Options
| Drapeau court | Drapeau long | Description |
| ------------- | ------------ | ----------- |
| -r | --regular | Cet indicateur indique que le programme doit convertir en XForm et ne pas essayer d’apporter des modifications spécifiques à PMA2020. |
| -p | --preexisting | Incluez cet indicateur (drapeau) pour empêcher le remplacement de fichiers préexistants. |
| -n | --novalidate | Ne validez pas la sortie XML avec ODK Validate. N'effectuez pas de contrôles supplémentaires sur (1) les données de colonnes indéfinies, (2) les références de variables en désordre. |
| -i | --ignore_version | Ignorez le versioning dans filename, form_id, form_title et save_form. En d'autres termes, ceci permet  par défaut d'assurer la cohérence de la version. |
| -l | --linking_warn | Produire des avertissements pour les directives de liaison incorrectes. Par défaut, une exception est déclenchée et le programme est arrêté. |
| -d | --debug | Afficher les informations de déboggage. Utiliser pour écraser les bugs. |
| -e | --extras | Effectuez des vérifications supplémentaires sur (1) les données dans des colonnes non définies et (2) les références de variables en désordre. |
| -s | --suffix | Un suffixe à ajouter au nom du fichier de base. Impossible de commencer par un trait d'union ("-"). |


## Interface utilisateur graphique

Pour ceux qui souhaitent utiliser une interface graphique lancée à partir de la ligne de commande., Le pipeline QTools2 commence ainsi

```
python -m qtools2
```

et vérifiez l’utilisation en ajoutant l’indicateur `--help` à la commande ci-dessus.

NOTE: l'option `-v2` a été supprimée à partir de la version 0.2.3.

## Mises à jour

REMARQUE: les utilisateurs de Windows commencent par la section _ ** Etapes spécifiques Windows ** _. Pour installer les mises à jour `qtools2`, utilisez

```
pip installer https://github.com/jkpr/QTools2/zipball/master --upgrade
```

Pour les plus récentes et les meilleures, remplacez «master dans les URL ci-dessus par «developer».


### Suggestions et pièges

- Vérifiez la version dans le terminal pour voir si un programme est installé.
- Vérifier la version de Java avec `javac -version`
- Vérifiez la version de Python avec `python -V`.
- Vérifiez la version de pip avec `pip -V`.
- Un autre exécutable pour Python est `python2`.
- Un autre exécutable pour `pip` est` pip2`.
- La version la plus récente de Java n'est pas requise, mais les tests réussis ont uniquement été exécutés avec Java 1.6 à Java 1.8.
- Une dépendance de `pmaxform` est` lxml`, ce qui peut poser problème sur Mac. S'il y a des problèmes, le meilleur guide est sur [StackOverflow] [8].
- Lors de l'installation de `pmaxform` sur Mac, l'utilisateur peut être invité à installer les outils de ligne de commande de Xcode. Cela devrait suffire pour `lxml`.
- Qtools2 peut fonctionner sans Java. Java n’est nécessaire que pour ODK Validate, qui peut être contourné en utilisant l’option "No validate".

[8]: http://stackoverflow.com/questions/19548011/cannot-install-lxml-on-mac-os-x-10-9

### Bugs

Soumettez les rapports de bugs à James Pringle à l'adresse `jpringleBEAR @ jhu.edu`.
