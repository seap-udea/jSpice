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
	@echo "Scanning ports and killing remaining sessions..."
	@-python bin/jspice.scan kill
	@echo "Removing sessions temporal file..."
	@-rm -r sessions/* &> /dev/null
	@echo "Resetting sessions database..."
	@-python bin/jspice.sql action=reset
	@echo "Resetting log files..."
	@-rm log/* &> /dev/null
	@echo "Stopping purging process..."
	@kill $(shell cat .purging)

commit:
	@echo "Commiting..."
	@-git commit -am "Commit"
	@-git push origin master

pull:
	@-git reset --hard HEAD
	@-git pull

