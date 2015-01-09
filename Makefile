NAME = pysymo
VERSION = 0.1

.PHONY: all build test tag_latest release ssh

all: build

build: build_web build_init build_refresh_cache build_refresh_charts

build_init:
	docker build --rm --pull -t $(NAME)_init:$(VERSION) Dockerfiles/init

build_web:
	docker build --rm --pull -t $(NAME)_web:$(VERSION) Dockerfiles/web

build_fill_db:
	docker build --rm --pull -t $(NAME)_fill_db:$(VERSION) Dockerfiles/fill_db
build_refresh_cache:
	docker build --rm --pull -t $(NAME)_refresh_cache:$(VERSION) Dockerfiles/refresh_cache
build_refresh_charts:
	docker build --rm --pull -t $(NAME)_refresh_charts:$(VERSION) Dockerfiles/refresh_charts
build_dev:
	docker build --rm --pull -t $(NAME)_dev:$(VERSION) Dockerfiles/dev

tag_latest:
	# docker tag $(NAME)_dev:$(VERSION) $(NAME)_dev:latest
	docker tag $(NAME)_web:$(VERSION) $(NAME)_web:latest
	docker tag $(NAME)_init:$(VERSION) $(NAME)_init:latest
	docker tag $(NAME)_fill_db:$(VERSION) $(NAME)_fill_db:latest
	docker tag $(NAME)_refresh_charts:$(VERSION) $(NAME)_refresh_charts:latest
	docker tag $(NAME)_refresh_cache:$(VERSION) $(NAME)_refresh_cache:latest
	@echo "*** Don't forget to create a tag. git tag rel-$(VERSION) && git push origin rel-$(VERSION)"

run: build build_fill_db
	docker run -d --rm --name pysymo_mongo_test mongo
	docker run -d --name pysymo_web_test --link pysymo_mongo_test:db pysymo_web:$(VERSION)
	docker run --rm -it --link pysymo_mongo_test:db pysymo_init:$(VERSION)
	docker run --rm -it --link pysymo_mongo_test:db pysymo_fill_db:$(VERSION) 10000
	docker run --rm -it --link pysymo_mongo_test:db pysymo_refresh_cache:$(VERSION)
	docker run --rm -it --link pysymo_mongo_test:db pysymo_refresh_charts:$(VERSION)
