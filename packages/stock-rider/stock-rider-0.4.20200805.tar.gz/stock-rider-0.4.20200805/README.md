## Stocks Rider

Find anomalies in Stock market based on Volume.

![](docs/stockridertips-banner.png)

A live version of this is running as a bot on [StockRiderTips](https://www.reddit.com/r/StockRiderTips) sub-reddit.

### Installation

```bash
pip install stock-rider
```

### Using Stocks Rider

*Populate data*

```bash
stock-rider populate-data --period 6mo --interval 1d
```

*Run analysis*

```bash
# High Volume analysis
stock-rider volume-analysis --period 200
```

### License

[MIT](https://choosealicense.com/licenses/mit/)
