# BurnTheGraph
*********************
# Description
Le Burning number est une notion d'informatique récente qui cherche à schématiser la propagation d'une information dans un réseau. <br/>
Dans le cadre d'un stage de fin d'année, en licence informatique à l'Université d'Orléans, j'ai implémenté différent heuristiques <br/>
pour obtenir le burning number et développé un visuel pour voir en temps réel l'évolution de la brûlure d'un graphe. <br/>
Plus d'informations dans le rapport de stage.
# Contenu & Utilisation
Le fichier "initGraph" contient des fonctions qui permettent d'initialiser un graphe à partir d'un fichier. <br/>
Le fichier "nfm_sparse" permet d'obtenir la node predominance du graphe. <br/>
Le fichier "visuel" permet de lancer une application web qui permet de visualiser la brûlure étape par étape. <br/>
Le fichier "visuel_meta" permet la même chose mais sur le métagraphe du graphe. <br/>
Les autres fichiers contiennent des heuristiques pour brûler des graphes. <br/>
Le dossier data contient des graphes avec leurs fichiers textes.<br/>
# Librairies
numpy , scipy, matplotlib, pandas, networkx, numba, dash
