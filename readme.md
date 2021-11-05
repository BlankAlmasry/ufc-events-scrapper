# ufc events scrapper

It will scrape all ufc fights into csv file

the data it will scrape is  `fighter1` `fighter2` `result1` `result2` `date`
Will fetch around 6500 Fights in 1 minute

It's Multi-Threaded

```
py -m pip install -r requirement.txt
py main.py
```

I scrape cached json files, and I don't loop through non ufc ones, and I loop through them in a multithreading way

That's by far the best way to scrape ufc data, and it's very fast.

I don't think the methods could bee improved, but the code probably could be, feel free to contribute if you have any
ideas

