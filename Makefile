run
	gunicorn run




run-docker-db

	docker run -d \
	--name db_blog \
	-e POSTGRES_USER=blog_user \
	-e POSTGRES_PASSWORD=local_pass_123 \
	-e POSTGRES_DB=blog_db \
	-p 5432:5432 \
	postgres:15

