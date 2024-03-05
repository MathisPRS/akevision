# subprocess est utilisé pour pouvoir lancer des commandes bash via python
import subprocess
import datetime
import os

# Commande git à utiliser pour avoir le nom du dernier tag
get_last_tag_command = 'git describe --tags --abbrev=0'

# subprocess.call() lance une commande bash, et .stdout.read.decode() lis le retour et le transforme en str, ici on
# enlève le dernier caractère car c'est un '\n'
last_tag_name = subprocess.Popen(get_last_tag_command.split(), stdout=subprocess.PIPE).stdout.read().decode()[:-1]

# Incrémente le N° de version
new_tag_name = last_tag_name[:-1] + str(int(last_tag_name[-1])+1)
new_tag_creation_command = 'git tag -a ' + new_tag_name + ' -m "Tag généré par le script make_changelog.py"'
new_tag_creation_output = subprocess.Popen(new_tag_creation_command.split(), stderr=subprocess.PIPE)
creation_error = new_tag_creation_output.stderr.read().decode()
if len(creation_error) > 0:
    print('Impossible de créer le nouveau tag')
    print(creation_error)
else:
    print('Nouveau tag créé')

push_tag_command = 'git push origin ' + new_tag_name
push_tag_output = subprocess.Popen(push_tag_command.split(), stderr=subprocess.PIPE)
push_tag_error = push_tag_output.stderr.read().decode()
if len(push_tag_error) > 0:
    print('Impossible de pousser le nouveau tag')
    print(push_tag_error)
else:
    print('Nouveau tag poussé')

# On récupère la date de création du dernier tag
get_second_last_tag_date_command = 'git log -1 --format=%ai ' + last_tag_name

last_tag_date = subprocess.Popen(get_second_last_tag_date_command.split(), stdout=subprocess.PIPE).stdout.read().decode()[:20]

# Variable pour éviter un bug d'ambiguité
date_filter = "--since='" + last_tag_date + "'"

# On récupère la liste des commits selon le format souhaité
log_since_last_tag = subprocess.Popen(["git", "log", "--no-merges", date_filter,  "--date=format:%d-%m-%Y", "--pretty=format:* %ad - %s"], stdout=subprocess.PIPE).stdout.read().decode()

# Si le fichier changelog.md existe on le supprime
if os.path.exists('changelog.md'):
    os.remove('changelog.md')

# On écrit dans le fichier
changelog_file = open("changelog.md", "a")
changelog_file.write(new_tag_name + ' ( ' + datetime.date.today().strftime("%d-%m-%Y") + ' ) ' + '( ' + str(log_since_last_tag.count('\n')-1) + ' commits ) \n')
changelog_file.write('------------------------------------------ \n')
changelog_file.write(log_since_last_tag)

print("Changelog success !")
