### IA : Prediction encombrement d'un restaurant universitaire
____
Il s'agit d'un **ANN** (**A**rtificial **N**eural **N**etwork) permettant de prédire si le restaurant universitaire sera complet ou non en utilisant simplement un _timestamp_.
____

##### Etape 1: Les données
Afin d’entraîner l'IA, il est nécessaire de disposer d'un grand nombre de données. Pour celà, nous avons créé un générateur de données nommé **generate_data.py** qui produit un fichier **data.csv** avec les colonnes suivantes :

|  Hour   |        Minute        |  Day  | Température |                     Nb                     | Venir  |
| :-----: | :------------------: | :---: | :---------: | :----------------------------------------: | :----: |
| 10 à 13 | 0 à 50 par pas de 10 | 0 à 6 |    en °C    | nombre de personnes <br> (inconnu de l'IA) | 0 ou 1 |
____

##### Etape 2: L'entrainement
L'entrainement de l'IA se lance après avoir généré le fichier **data.csv**, en exécutant le fichier **train_AI.py**.
Cet entrainement va générer 2 fichiers :
- **trained_model.sav**, le réseau de neurones entrainé.
- **preprocess_model.sav**, le préprocesseur des données pour préparer les données pour le réseau.
____

##### Etape 3: La prediction
La prédiction est obtenue en exécutant **predict_AI.py**, avec un argument timestamp.(exemple avec le 25/12/2019 à 12:10:00)
```bash
python predict_AI.py 1577275800
```
____

#### Remarques :

**Attention !** Les scripts mis à disposition fonctionnent correctement avec **Python 3.7**. Assurez-vous de ne pas utiliser **Python 3.8** car la librairie **TensorFlow** n'est pas compatible.

Il est nécessaire d'installer quelques librairies en exécutant la commande suivante :
```bash
sudo pip install -r requirements.txt
```
**Pour les flemmards, voici la liste des commandes à exécuter  :**
```bash
sudo pip install -r requirements.txt
python generate_data.py 
python train_AI.py
python predict_AI.py 1577275800
```

