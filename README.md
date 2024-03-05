# akevision

## Commandes le service MySql

Commande pour vérifier le status de MySql:
```bash
sudo systemctl status mysqld.service
```


Commande pour démarrer le service MySql:

```bash
sudo systemctl start mysqld.service
```

##Commandes les dumps
Commande pour faire le dump de la base sous mysql
```bash
cd /home/akema/akevision/akevisionback/akevision_rest/migrations/mysql
mysqldump --user=root -p --databases akevision_rest > mysql_dump.sql
```
Commande pour récupérer le dump de la base sous mysql
```bash
cd /home/akema/akevision/akevisionback/akevision_rest/migrations/mysql
mysql --user=root -p  akevision_rest  < mysql_dump.sql
```
##install côté back
pip install à faire pour akevision
```bash
pip install djangorestframework
pip install django-cors-headers
pip install django-rest-authtoken
pip install django-filter
pip install httpie
```

## Npm limitation
J'ai atteint une limitation de fichier traité par npm sur mon environnement de dev.
J'ai augmenté la capacité avec :
```linux
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p
```

## Import Excel
La fonction **upload_select_file** permet d'importer toutes les données d'un fichier Excel sous la forme d'un OrderedDict où
le nom des feuilles fait office de clé de dictionnaire

## Mail
La fonction **create_email** permet la création et la mise en page du mail avant l'envoi, elle a 3 paramètres :
1. Choix du template de mail, les templates sont à ranger par défaut ici : *monProjetBack/monProjet_rest/templates/emails/monTypeDeMail*
   1. Le sujet du mail : 'emails/{0}/{0}-subject.txt'.format(template_prefix))
   2. Le corps du mail : 'emails/{0}/{0}-content.txt'.format(template_prefix))
   3. La mise en page du mail : 'emails/{0}/{0}-content.html' *(similaire au corps du mail)*
2. Données et variables que l'on souhaite utiliser dans le mail sous forme d'un dictionnaire
3. Array avec la liste des mails des destinataires

Pour définir l'email d'envoi, il faut modifier dans le fichier **configlocal.cfg** la ligne 
```
DEFAULT_FROM_EMAIL = config.get('email', 'DEFAULT_FROM_EMAIL')
```