//a placer à la racine du projet
#!/bin/sh
echo "looking for gunicorn process id"
ps -Al | grep gunicorn | wc -l                                            //on récupère les process gunicorn
if [ $? != 0]                                                             //si le nombre de process est différent de 0 alors on les tue
    ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill
then 
    /usr/bin/gunicorn_start.bash . &                                      //on relance gunicorn avec le script gunicorn_start
fi
echo "done gunicorn running 2 workers"
