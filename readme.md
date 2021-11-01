# ufc events scrapper
It will scrape all ufc fights into csv file

the data it will scrape is  `fighter1` `fighter2` `result1` `result2` `date`
Will fetch around 6500 Fights in 5 minutes 

It's not multi-threaded for now

```
py -m pip install -r requirement.txt
py main.py
```

Note: I didn't put much effort into multithreading it, because I didn't need to at the time, feel free to contribute if you want