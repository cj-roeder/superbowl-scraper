# superbowl-scraper

Scrapes Wikipedia's List of Super Bowl champions to find every Super Bowl page,
then visits each game's page concurrently to collect its MVP.

## How to use

```
pip install requests
chmod +x scraper.py
./scraper.py
```

The scraper runs 3 times with 1, 8, and 14 workers, prints how long each run took, then lists each Super Bowl's MVP.


## Performance impacts

These results use the first 10 games (set by the `urls = urls[:10]` line in the scraper). Delete that line to scrape all ~60 games.

| workers | seconds | speedup (x) |
|---|---|---|
| 1 | 1.346 | 1.0 |
| 8 | 0.242 | 5.6 |
| 14 | 0.142 | 9.5 |

concurrent.futures: Most of the time is spent waiting on Wikipedia, so running multiple threads lets those waits overlap. The gain flattens out at higher worker counts because of bottlenecks like the network.

functional programming: scrape() is a self-contained function with no shared state, so executor.map() can safely run copies of it at the same time. Functional style doesn't speed things up by itself, but it's what makes the parallel version safe and easy. I also used map() with a lambda to build the list of URLs.
