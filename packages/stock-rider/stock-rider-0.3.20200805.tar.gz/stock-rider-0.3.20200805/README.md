## Stocks Rider

Find anomalies in Stock market based on Volume.

![](docs/stockridertips-banner.png)

### Examples

*Populate data*

```bash
# selected stocks
populate-data --stock KODK,JFK,MSFT --start 2020-01-01 --end 2020-07-31 --interval 1d

# all stocks
populate-data --start 2020-01-01 --end 2020-07-31 --interval 1d
```

*Run analysis*

```bash
# Selected stocks
volume-analysis --period 200 --stocks AAPL,KODK

# All stocks
volume-analysis --period 200
```

### License

[MIT](https://choosealicense.com/licenses/mit/)
