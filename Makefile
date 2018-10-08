.PHONY: clean singularity

help:
	@echo "clean - remove all build and test artifacts"
	@echo "singularity - Creates singularity 2.3.4 image"

clean:
	rm -fr /home/vagrant/build/

bdist_wheel:
	python setup.py build
	python setup.py bdist_wheel

singularity: clean bdist_wheel
	@echo 'Creating Singularity v23 image'
	mkdir -p /home/vagrant/build
	imgfile='/home/vagrant/build/d3rglide.img' ; \
	sudo singularity create -s 12048 $$imgfile ; \
	sudo singularity bootstrap $$imgfile singularity.def; \
	echo 'Singularity image created. Copying $$imgfile to build/' ;\
	mv $$imgfile build/. ;\
	echo 'Image file can be found under build/'
