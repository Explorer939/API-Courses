# API de Cours Gratuits - Documentation Rapide

## Endpoints Disponibles

### 1. Obtenir tous les cours
**Requête :**

GET /courses


### 2. Filtrer par type de produit d'apprentissage
**Requête :**

GET /courses/product_type/{product_type}


**Paramètres :**
- product_type (str) : Type de produit d'apprentissage (SPECIALIZATION, PROFESSIONAL CERTIFICATE, COURSE)

**Exemple :**

GET /courses/product_type/COURSE



### 3. Filtrer par niveau de difficulté
**Requête :**

GET /courses/difficulty/{difficulty}


**Paramètres :**
- difficulty (str) : Niveau de difficulté (Beginner, Intermediate, Mixed, Advanced)

**Exemple :**

GET /courses/difficulty/Beginner



### 4. Filtrer par type de produit et niveau de difficulté
**Requête :**

GET /courses/filter/


**Paramètres :**
- product_type (str) : Type de produit d'apprentissage
- difficulty (str) : Niveau de difficulté
- skip (int) : Pagination (départ)
- limit (int) : Pagination (limite)
- sort_by (str) : Tri (enrolled Student Count, Course rating)
- sort_order (str) : Ordre de tri (asc, desc)

**Exemple :**

GET /courses/filter/?product_type=COURSE&Rating=Advanced&sort_by=Course rating&sort_order=desc



## Conseils d'utilisation
- **Pagination** : Utilise skip et limit pour naviguer dans les résultats sans surcharger la réponse.
- **Tri** : Trie les résultats selon les préférences d'affichage.
- **Mise à jour automatique** : Les données se mettent à jour toutes les minutes sans redémarrer l'API.
