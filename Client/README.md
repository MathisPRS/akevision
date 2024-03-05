# DevOps 1 

Ce Document est un ensemble de ressources utiles pour: 

 - La configuration des serveurs nginx et gunicorn
 - le debug d'un projet en production
 - le lancement des services en production (reprise de service)

# Nginx et gunicorn

Rappel: 
Nginx est un serveur web. En production nous l'utilisont pour rendre disponible aux clients le frontend, et les fonctions du backend grâce à sa fonction de reverse proxy. 
*

> un reverse proxy permet d'accèder à un serveur interne depuis l'exterieur, ici , gunicorn.

Gunicorn est un serveur HTTP wsgi, il permet donc l'utilisation de django à une plus grand échelle que le serveur intégré à django. 

## la configuration nginx

Voici le fichier de configuration se trouvant dans /etc/nginx/conf.d/nomduprojet.conf

    server {
    
    server_name nom_du_server et/ou ip;

    keepalive_timeout 5;

    # path vers angular après build cf partie suivante
    root /home/dev/projet/projetfront/dist/projetfront;
        index index.html;

     location ~ \.css {
            add_header  Content-Type    text/css;
        }

        location ~ \.js {
            add_header  Content-Type    application/x-javascript;
        }

        location / {

            try_files $uri /index.html;
        }

        location /static {
                  root /home/dev/projet/projetfront/dist/projetfront/static;
        }



    location ~ ^/(projet_rest|admin|projet)/ {
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_pass http://app_server; 
    }
  }

    proxy_pass http://app_server; 
    
correspond à la définition d'un path préconfiguré sur nginx vers la socket gunicorn

Pour verifier que le serveur nginx tourne: 

    systemctl status nginx

s'il ne tourne pas: 

    systemctl start nginx

s'il ne tourne toujours pas, on vérifie les logs avec: 
`journalctl -xe` ou dans le répértoire /var/log/nginx/latest.log




## Gunicorn

Pour gunicorn, nous avons un script et un service créé sur le serveur, voici le script situé dans /usr/bin: 


       #!/bin/bash
    
    NAME="octi"                                  # Name of the application
    DJANGODIR=/home/dev/projet/projetback             # Django project directory
    SOCKFILE=/home/dev/run/gunicorn.sock  # we will communicte using this unix socket
    USER=dev                                        # the user to run as
    GROUP=dev                                    # the group to run as
    NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn
    DJANGO_SETTINGS_MODULE=octi.settings             # which settings file should Django use
    DJANGO_WSGI_MODULE=octi.wsgi                     # WSGI module name
    
    echo "Starting $NAME as `whoami`"
    
     Activate the virtual environment
    cd $DJANGODIR
    source /home/dev/venv/bin/activate
    export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
    export PYTHONPATH=$DJANGODIR:$PYTHONPATH
    
    #Create the run directory if it doesn't exist
    RUNDIR=$(dirname $SOCKFILE)
    test -d $RUNDIR || mkdir -p $RUNDIR
    
     Start your Django Unicorn
     Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
    exec /home/dev/venv/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
      --name $NAME \
      --workers $NUM_WORKERS \
      --user=$USER --group=$GROUP \
      --bind=unix:$SOCKFILE \
      --log-file=/home/dev/gunicorn.log


pour vérifier que le service tourne: 

    service projetback status

pour lancer le service:

    service projetback start

les logs sont dans le dossier racine du projet. 

## les différence entre le code en production et celui sur votre poste local

Le fichier settings.py a des champs avec des informations différentes: 
Le champs base de donnée, le champs allowed_host comprend les ip et nom de domaine du serveur en production de même pour les cores_origin_whitelist. 

Les fichiers front utilisés par le serveur nginx sont dans le dossier créé après compilation (ng build --prod), le dossier dist et non src. 


# deploiement continu

Le deploiement continu permet de deployer sur un ou plusieurs serveurs, un projet après l'avoir **build** dans un container appelé **runner**. Chaque **runner** est définit par un **tag**. À Akema nous utilisons le **tag** **Docker**. Celui-ci correspond au **runner** 1&1 sur la machine Queen. Ces runners possèdent un environnement docker. Donc chaque **runner** lance un container dans lequel est executé une suite d'action definie dans le block **build** du fichier .gitlab-ci.yml.
Chaque étape du .gitlab-ci.yml est décrite ici.

1 Before script
2 build
3 test
4 deploy


## Before Script

Cette partie s'execute dans le container du runner avant la copie du contenu de la branche.
Elle permet d'installer les paquets indispensables au projet, comme node, un client ssh par exemple. Mais aussi d'échanger les clés ssh pour le déploiement.
En effet la clé ssh privé (id_rsa) doit être ajoutée au projet.
>dans setting-->ci/cd-->variables

## build
le build comprend toutes les actions à réaliser pour lancer le projet. Pour un projet python, par exemple le build doit:
Créer l'environnement virutel, installer les requirement.txt, lancer le build du front.
Enfin le build compresse le front et le back dans deux archives distinctes.

## deploy
comme son nom l'indique, le deploy permet d'envoyer les archives créées sur les serveurs cible.
La connexion se fait par ssh. La machine cible doit donc être configurée pour que:
- un utilisateur non-root ait le droit sans mot de passe de relancer le service nginx
- la connexion ssh doit etre uniquement par clé privée
- les deux scripts pour le serveur de backend gunicorn doivent être sur la machine cible.
>les indications pour placer les script sont en commentaire dans les dits scripts.
