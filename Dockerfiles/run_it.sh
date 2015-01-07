docker run -d -v /home/vlad/dev/Dockerfile/pysymo/mongo_data/:/data/db --name pysymo_mongo mongo
docker run -d --name pysymo_web --link pysymo_mongo:db pysymo:web
docker run --rm -it --link pysymo_mongo:db pysymo:init
docker run --rm -it --link pysymo_mongo:db pysymo:fill_db 100000
docker run --rm -it --link pysymo_mongo:db pysymo:refresh_cache
docker run --rm -it --link pysymo_mongo:db pysymo:refresh_charts
