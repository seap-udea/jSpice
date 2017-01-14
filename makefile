cleancrap:
	@echo "Cleaning crap..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "#" -exec rm -rf {} \;

cleancode:
	@echo "Cleaning code..."
	@find . -name "*.pyc" -exec rm -rf {} \;

clean:cleancrap cleancode

perms:
	chown -R www-data.www-data .

commit:
	@echo "Commiting..."
	@-git commit -am "Commit"
	@-git push origin master

pull:
	@-git reset --hard HEAD
	@-git pull

