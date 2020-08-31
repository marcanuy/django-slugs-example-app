pip-freeze:
	pip freeze > requirements.txt
generate-uml:
	./manage.py graph_models -a -o models.png
show-urls:
	./manage.py show_urls
