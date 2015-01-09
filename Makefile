NAME = pysymo
VERSION = 0.1
REPO = localhost:5000

# DOCKER_BUILD_OPTS = --pull
DOCKER_BUILD_OPTS = 

.PHONY: all build test tag_latest release ssh

all: build

build: build_web build_init build_refresh_cache build_refresh_charts

build_init:
	docker build --rm $(DOCKER_BUILD_OPTS) -t $(NAME)_init:$(VERSION) Dockerfiles/init

build_web:
	docker build --rm $(DOCKER_BUILD_OPTS) -t $(NAME)_web:$(VERSION) Dockerfiles/web

build_fill_db:
	docker build --rm $(DOCKER_BUILD_OPTS) -t $(NAME)_fill_db:$(VERSION) Dockerfiles/fill_db
build_refresh_cache:
	docker build --rm $(DOCKER_BUILD_OPTS) -t $(NAME)_refresh_cache:$(VERSION) Dockerfiles/refresh_cache
build_refresh_charts:
	docker build --rm $(DOCKER_BUILD_OPTS) -t $(NAME)_refresh_charts:$(VERSION) Dockerfiles/refresh_charts
build_dev:
	docker build --rm $(DOCKER_BUILD_OPTS) -t $(NAME)_dev:$(VERSION) Dockerfiles/dev

tag_latest:
	# docker tag $(NAME)_dev:$(VERSION) $(NAME)_dev:latest
	docker tag -f $(NAME)_web:$(VERSION) $(REPO)/$(NAME)_web:latest
	docker tag -f $(NAME)_init:$(VERSION) $(REPO)/$(NAME)_init:latest
	docker tag -f $(NAME)_fill_db:$(VERSION) $(REPO)/$(NAME)_fill_db:latest
	docker tag -f $(NAME)_refresh_charts:$(VERSION) $(REPO)/$(NAME)_refresh_charts:latest
	docker tag -f $(NAME)_refresh_cache:$(VERSION) $(REPO)/$(NAME)_refresh_cache:latest
	@echo "*** Don't forget to create a tag. git tag rel-$(VERSION) && git push origin rel-$(VERSION)"
upload:
	docker push $(REPO)/$(NAME)_web:latest
	docker push $(REPO)/$(NAME)_init:latest
	docker push $(REPO)/$(NAME)_fill_db:latest
	docker push $(REPO)/$(NAME)_refresh_charts:latest
	docker push $(REPO)/$(NAME)_refresh_cache:latest

run: build build_fill_db
	docker run -d --name pysymo_mongo_test mongo && sleep 10
	docker run -d --name pysymo_web_test --link pysymo_mongo_test:db pysymo_web:$(VERSION)
	docker run --rm -it --link pysymo_mongo_test:db pysymo_init:$(VERSION)
	docker run --rm -it --link pysymo_mongo_test:db pysymo_fill_db:$(VERSION) 10000
	docker run --rm -it --link pysymo_mongo_test:db pysymo_refresh_cache:$(VERSION)
	docker run --rm -it --link pysymo_mongo_test:db pysymo_refresh_charts:$(VERSION)
