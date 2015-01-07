cat Dockerfile.init | docker build -t pysymo:init -
cat Dockerfile.dev  | docker build -t pysymo:dev  -
cat Dockerfile.prod | docker build -t pysymo:prod -
cat Dockerfile.refresh_cache | docker build -t pysymo:refresh_cache -
