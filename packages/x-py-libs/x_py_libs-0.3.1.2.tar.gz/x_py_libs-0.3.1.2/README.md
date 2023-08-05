py setup.py sdist
twine upload dist/*


pipreqs ./ --encoding=utf8 --force

pip install -r requirements.txt
