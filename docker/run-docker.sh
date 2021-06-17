docker run -v "$(pwd)":/srv/data/  --env THREADS="2" -it --rm -p 8900:8900 bert-summarizer 
