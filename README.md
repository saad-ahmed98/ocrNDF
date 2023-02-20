# NDFocr 

**Backend en python qui effectue la reconnaissance des données à partir d'une image.**. 
 
Endpoint pour effectuer une analyse: ``/ocr``  
Cet endpoint accèpte que des POST, il faudra lui envoyer une image dans le body sous forme de form-data.

## Preréquis

Avant de lancer l'application, il faudra d'abord avoir installé Python sur sa propre machine.  
**Il est impératif que la version utilisée soit comprise entre la 3.7 et la 3.9 ou le projet ne marchera pas!!**

Ensuite, créer un environnement python où on installera les bibliothéques necessaires :

```
python -m venv env
```

Une fois ``env`` crée, le lancer. (Il faudra le lancer avant chaque lancement de l'appli) de la façon suivante : 
```
env/Scripts/activate 
``` 

Installer maintenant toutes les dependances necessaires avec ``pip install [library]`` où ``[library]`` sera:

*  ``django``
*  ``easyocr``
*  ``torch torchvision torchaudio``
*  ``unidecode``


## Comment utiliser

Lancer l'application avec : 
```
python manage.py runserver  
```

## Auteurs

* AHMED Saad El Din

