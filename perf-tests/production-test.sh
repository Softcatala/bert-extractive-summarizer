URL='https://api.softcatala.org/summarization-service/v1/summarize_by_sentence'

echo "** Summary (5 req, 1 at the time)"
ab -n 5 -c 1 -p  text.form -T application/x-www-form-urlencoded $URL  | grep '95%'
