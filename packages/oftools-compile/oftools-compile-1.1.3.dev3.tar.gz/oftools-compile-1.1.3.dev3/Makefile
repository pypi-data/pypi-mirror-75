init:
	pip3 install -r requirements.txt

uninstall:
	pip3 uninstall oftools-compile
	rm dist build oftools_compile.egg-info -r

install:
	python3 setup.py sdist bdist_wheel
	pip3 install dist/*.tar.gz --user

upload:
	python3 setup.py sdist upload -r pypi

test_upload:
	python3 setup.py sdist upload -r testpypi

remove:
	echo "curl --form ":action=remove_pkg" --form "name=oftools_compile" --form "version=0.0.1" URL -u id:pass"

yapf:
	yapf3 --style='{ based_on_style: google }' *.py -ir

html:
	cd docs
	grip README.md --title=oftools_compile --export
	cd -

test:
	coverage run --source oftools_compile -m py.test -v -s
	coverage report
