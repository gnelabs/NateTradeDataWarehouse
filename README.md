# NateTradeDataWarehouse

## Description
Public data warehouse library used to consume data in the NateTrade database. Can be used for backtesting, charting, or strategy development.

## Building Docker Container
``` bash
docker-compose build
```

## Running Docker Container
Requires docker to be installed and running in the background. 
``` bash
docker run -t -i --env-file ./env.list natetradedatawarehouse_dw
```