pushd ..
#python3 -m pytest
docker build -t bert-summarizer . -f docker/Dockerfile.service
docker images | grep bert-summarizer
popd
