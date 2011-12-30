#!/bin/bash

gnome-terminal --full-screen --hide-menubar --tab --working-directory=/home/erem/beatwrit/ --command="./scripts/edit_beatwrit"  --tab --working-directory=/home/erem/beatwrit.com/templates/ --command="./edit_templates" --tab --working-directory=/home/erem/beatwrit/ --command="python manage.py shell"  --tab --working-directory=/home/erem/beatwrit/ --command="python manage.py runserver"

