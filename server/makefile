cleancrap:
	@echo "Cleaning crap..."
	@find . -name "*~" -exec rm -rf {} \;
	@find . -name "#" -exec rm -rf {} \;

clean:cleancrap
	@echo "Cleaning all..."
	@rm -rf *.png *.dat

commit:
	@echo "Commiting..."
	@-git commit -am "Commit"
	@-git push origin master

pull:
	@-git reset --hard HEAD
	@-git pull

unpack:
	@echo "Unpacking large kernels..."
	@cat util/kernels/de430bsp/* > util/kernels/de430.bsp
	@echo "Done."
