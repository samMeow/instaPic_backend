# InstaPic-backend
Hosted: http://sammeow-instapic-backend.herokuapp.com/

## Documentation
http://sammeow-instapic-backend.herokuapp.com/docs/

## Getting started
### Requirement
`docker-compose` and `pip`

### Start App
Server will be serving at `localhost:5000`
```sh
docker-compose up -d
make db-up
# or only db
docker-compose up -d instapic-db
make db-up
make install
make run
```

### others
```sh
#lint
make lint
# test
make tests
```