# horse
horserace website parse with scrappy.

To generate csv file with parsed data run in your shell: 

cd PATH_TO_PROJECT/horse

pip install -r requirements.txt

scrapy crawl races -o file.csv -t csv
