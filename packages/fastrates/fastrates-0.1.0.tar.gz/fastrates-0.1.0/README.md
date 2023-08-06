<img src="https://github.com/ycd/fastrates/blob/master/fastrates/frontend/static/logo.png" width=500>

## Command line interface for [Fast Rates](https://github.com/ycd/fastrates)


# Installation :pushpin:

```python
pip install fastrates-cli


Successfully installed fastrates-cli-0.1.0

```

# How to use? :rocket:
```python
Options:
  --base TEXT             Base ticker for currency  [default: EUR]
  --latest / --no-latest  Get the latest foreign exchange reference rates
                          [default: False]

  --start-at TEXT         Get historical rates for any day since start_at
  --end-at TEXT           Get historical rates for any day till end_at
  --symbols TEXT          Compare specific exchange rates
  --date TEXT             Get historical date
  --help                  Show this message and exit.
```

* ## Example 
```python
fastrates-cli --latest
```
## Which will return
```JSON
{
    "rates":{
        "2020-07-31":{
            "AUD":1.6488,
            "BGN":1.9558,
            "BRL":6.1219,
            "CAD":1.5898,
            "CZK":26.175,
            "DKK":7.4442,
            "GBP":0.90053,
            "TRY":8.2595,
            "USD":1.1848,
        }
    },
    "base":"EUR"
}
```



## Release Notes :mega:

### Latest Changes

### 0.1.0

* Prototype of project
