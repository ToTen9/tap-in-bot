# tap-in-bot
Un bot qui récupére tout les tweets d'un utilisateur afin de les comparer entre eux, et de remonter les tweets redondons.
Pour faire appel à ce bot il suffit de le mentionner d'un commentaire @Tap-in-bot

# Configuration du bot en local
1. Installation de Python
2. Installation de la librairie *Tweepy*  
 $ pip instal tweepy
3. Installation de la librairie *configparser*  
 $ pip instal configparser
4. Installation *Pandas*  
 $ pip instal pandas
5. Créer votre dossier  
  $ mkdir tweepy-bots  
  $ cd tweepy-bots  
  $ python3 -m venv venv
6. Activation:   
  $ source ./venv/bin/activate    
  $ pip install tweepy     
7. Création d'un fichier qui contient les dépendences   
  $ pip freeze > requirements.txt  
8. Mettez en place un fichier de configuration: config.ini  
avec ces différents variables: 
[twitter]  
api_key =   
api_key_secret =   
access_token =   
access_token_secret =   

