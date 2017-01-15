cleancrap:
	@echo "Cleaning crap..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "#" -exec rm -rf {} \;

cleancode:
	@echo "Cleaning code..."
	@find . -name "*.pyc" -exec rm -rf {} \;

clean:cleancrap cleancode

perms:
	@echo "Setting permissions..."
	@chown -R www-data.www-data .

reset:
	@echo "Resetting server & proxy..."
	@-python bin/jspice.scan kill
	@echo "Removing sessions temporal file..."
	@-rm -r sessions/*
	@echo "Resetting sessions database..."
	@-python bin/jspice.sql
	@echo "Resetting log files..."
	@-rm log/*

commit:
	@echo "Commiting..."
	@-git commit -am "Commit"
	@-git push origin master

pull:
	@-git reset --hard HEAD
	@-git pull

