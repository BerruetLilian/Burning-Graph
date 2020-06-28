# Bruning-Graph
*********************
# Description
Le Burning number est une notion d'informatique récente qui cherche à schématiser la propagation d'une information dans un réseau. <br/>
Dans le cadre d'un stage de fin d'année, en licence informatique à l'Université d'Orléans, j'ai implémenté différentes heuristiques
pour obtenir le burning number et développé un visuel afin de voir en temps réel l'évolution de la brûlure d'un graphe. 
Plus d'informations dans le fichier pdf qui explique les notions et précise les différentes heuristiques. <br/>
Ce git existe dans un but d'exemple sur l'utilisation de la librairie dash, il a été réalisé par un étudiant de 3e année, des erreurs d'implémentation ou d'optimation
peuvent exister, veuillez donc avoir un regard critique sur le travail réaliser.
# Contenu & Utilisation
Le fichier "initGraph" contient des fonctions qui permettent d'initialiser un graphe à partir d'un fichier. <br/>
Le fichier "visual" permet de lancer une application web qui permet de visualiser la brûlure étape par étape. <br/>
Le fichier "visual_meta" permet la même chose mais sur le métagraphe du graphe. <br/>
Les autres fichiers contiennent des heuristiques pour brûler des graphes. <br/>
Le dossier data contient des graphes avec leurs fichiers textes.<br/>
Le fichier "example" contient également un exemple d'utilisation.<br/>
Le dossier assets contient le fichier css et le fond utilisé dans le visuel.
# Librairies
numpy , scipy, matplotlib, pandas, networkx, numba, dash
