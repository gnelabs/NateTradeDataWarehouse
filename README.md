# NateTradeDataWarehouse

## Description
Public data warehouse library used to consume data in the NateTrade database. Can be used for backtesting, charting, or strategy development.

## Building Docker Container
Requires docker-compose to be installed. Can alternatively be built directly with docker.
``` bash
docker-compose build
```

## Running Docker Container
Requires docker to be installed and running in the background. 
``` bash
docker run -t -i --env-file ./env.list natetradedatawarehouse_dw
```

## Credentials, Endpoints
Put credentials in env.list and they will be available as environment variables within the container.
If using this in production, migrate the credentials to a password safe of some sort.

# Examples

## Test