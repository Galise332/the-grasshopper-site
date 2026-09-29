# The Grasshopper : refonte du site (démonstration)

Proposition de refonte du site du magasin de jouets The Grasshopper (Bruxelles et Louvain).

- Site en ligne : https://galise332.github.io/the-grasshopper-site/
- Rapport des améliorations (PDF) : [docs/The-Grasshopper-ameliorations.pdf](docs/The-Grasshopper-ameliorations.pdf)

## Source des informations

Tous les textes, coordonnées, horaires, prix et conditions viennent de
https://www.thegrasshopper.be/fr (relevé du 29/09/2026). Rien n'a été inventé.
Les images appartiennent à The Grasshopper.

## Générer le site

```
python build.py
```

Le script écrit les pages HTML, `sitemap.xml`, `robots.txt` et `site.webmanifest` à la racine.

## Mise en ligne réelle

La démonstration est en `noindex` pour ne pas dupliquer le site officiel dans Google.
Avant la mise en ligne, dans `build.py` :

1. passer `DEMO = False` ;
2. remplacer `BASE_URL` par le vrai nom de domaine ;
3. relancer `python build.py`.
