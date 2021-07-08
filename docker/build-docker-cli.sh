pushd ..
docker build -t bert-summarizer-cli . -f docker/Dockerfile
docker images | grep bert-summarizer-cli
popd
