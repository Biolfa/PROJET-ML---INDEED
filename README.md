# Projet Indeed #


## Contexte ##

Je suis CEO d’une boite qui s’occupe de faire des statistiques sur l’emploi dans le secteur du développement informatique et de la data à Paris, Lyon, Toulouse, Nantes et Bordeaux.  
Je m’intéresse tout particulièrement aux différences de salaires entre ces métiers + villes.

Je vous mandate afin de me fournir une étude sur ce marché à présenter sous forme de Dashboard.

**Rendu** : Votre lien Github + Présentation client avec PowerPoint.

**Deadline** : 28 octobre


## Mission ##

1. Faire un script de scraping sur [Indeed](https://www.indeed.fr/)  qui permette à l’utilisateur de spécifier :
   * le type d’annonces qu’il souhaite récupérer :
   <br/><br/>
     * Métier (développeur, data scientist, ...)
     * Type de contrat recherché (CDI, CDD, freelance, ...)
     * Lieu de recherche (Paris, Toulouse, ...)
<br/><br/>
   * les infos à scraper :
   <br/><br/>
     * Titre
     * Nom de la boite
     * Adresse
     * Salaire
     * Descriptif du poste
     * Date de publication de l’annonce

   Vous pouvez vous concentrer sur les annonces :
     * Métiers : développeur, data scientist, data analyst, business intelligence
     * Localisation : Paris, Lyon, Toulouse, Nantes et Bordeaux
     * Type de contrat : tous
<br/><br/>
2. Prévoir un script qui permette de stocker automatiquement les infos scrapées dans une base de données MongoDB (le script devra prendre en compte le fait de remplacer ou de ne pas tenir compte d’une annonce si cette dernière est déjà dans la BDD)
<br/><br/>
3. Récupérer les annonces pour lesquelles on a un salaire. (Il faudra un peu cleaner…)  
   Sur ces annonces l’objectif est de prédire le salaire en fonction des features à votre disposition (à vous de tester ce qui est pertinent)  
   Exemple de modèles à tester : Random Forest, Logistic Regression, Kernel RBF, Gradient Boosting Classifier, XGBClassifier, ...
<br/><br/>
4. Sur les annonces pour lesquels il n’y a pas de salaire, déduire et compléter ce champ en fonction des résultats de 3/
<br/><br/>
5. Créer un dashboard avec Flask. A vous de voir ce qui est pertinent de montrer au client

### Bonus ###

1. Faire un script qui permette d’actualiser automatiquement vos résultats chaque semaine
<br/><br/>
2. Dockeriser
<br/><br/>
3. Pour chacune des entreprises scrapées, créer un script qui permette de récupérer sur LinkedIn toutes les infos disponibles sur ces dernières (taille de l’entreprise, spécialité, adresse mail, site, description, nombre d’employés etc.).  
   Ajouter ces informations dans la BDD.  
   <span style="color:red">Attention de ne pas vous faire ban votre compte !</span>  
   *Astuce :* Avec Selenium, chercher l’entreprise dans les suggestions et non sur la page de résultat
<br/><br/>
4. Avec le nom de l’entreprise (ou l’url du site récupéré via profil LinkedIn), rechercher sur le site web de l’entreprise le mail générique ainsi que leurs potentiels recherche de poste (onglet « On recrute », « Nous rejoindre » etc..). Compléter la BDD MongoDB avec ces informations

#### A vous de jouer !! ####