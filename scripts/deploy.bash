#!/bin/bash

TEST_FILE=/home/erem/dreamhost/beatwrit.com
source_path=/home/erem/beatwrit
dest_path=/home/erem/dreamhost/beatwrit.com

if [ ! -e "$TEST_FILE" ]
	then
		echo "Remote directory not mounted.  $TEST_FILE"
		sshfs eremgumas@melekeok.dreamhost.com:/home/eremgumas/ /home/erem/dreamhost
		echo "Tried mounting."
fi

if [ ! -e "$TEST_FILE" ]
	then
		echo "Remote directory not mounted.  $TEST_FILE"
		sshfs eremgumas@melekeok.dreamhost.com:/home/eremgumas/ /home/erem/dreamhost

	else
		#these two files shouldn't be changed
		touch $dest_path/beatwrit/sitesettings.py
		touch $dest_path/templates/mainwrap.html

		cp --update --verbose /home/erem/beatwrit.com/templates/*.* $dest_path/templates/

		cp --update --verbose /home/erem/beatwrit.com/files/*.* $dest_path/public/files/

		cp --update --verbose $source_path/*.py $dest_path/beatwrit/
		cp --update --verbose $source_path/*.txt $dest_path/beatwrit/

		cp --update --verbose $source_path/main/*.py $dest_path/beatwrit/main/
		cp --update --verbose $source_path/main/pagecontexts/*.py $dest_path/beatwrit/main/pagecontexts/
		cp --update --verbose $source_path/main/email/*.py $dest_path/beatwrit/main/email/
		cp --update --verbose $source_path/main/templatetags/*.py $dest_path/beatwrit/main/templatetags/
		cp -R --update --verbose $source_path/lib  $dest_path/beatwrit
        touch $dest_path/tmp/restart.txt
fi





