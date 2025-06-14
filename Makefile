livehtml:
	hatch run all:$(MAKE) -C docs livehtml

html:
	hatch run all:$(MAKE) -C docs html

pdf:
	hatch run all:$(MAKE) -C docs latexpdf
	
doc: html

install:
	python3 -m pip install --user . --break-system-packages

build:
	hatch build

test:
	rm -f .coverage coverage.xml
	hatch run all:pytest --cov=pyfeyn2 --cov-config=.coveragerc --cov-append --cov-report=term --cov-report=xml

commit: 
	-git add .
	-git commit

push: commit
	git push

pull: commit
	git pull

clean: 
	rm -r docs/build docs/source/_autosummary
	rm -r .eggs .pytest_cache *.egg-info dist build


release: push html
	git tag $(shell git describe --tags --abbrev=0 | perl -lpe 'BEGIN { sub inc { my ($$num) = @_; ++$$num } } s/(\d+\.\d+\.)(\d+)/$$1 . (inc($$2))/eg')
	git push --tags
