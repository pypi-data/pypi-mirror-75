

[![CircleCI](https://circleci.com/gh/athanikos/cryptodataaccess.svg?style=shield&circle-token=ecfbd9ba1187e20c781c6e467683e29e5418f915)](https://app.circleci.com/pipelines/github/athanikos/cryptodataaccess)



### Crypto data access  
Repositories for cryptomodel 
1. UsersRepository (user settings, notifications)
2. TransactionRepository (buy,sell,deposit) 
3. RatesRepository (exchange rates & symbol rates )




##### unit testing setup 
> import keyring
> keyring.set_password("cryptodataaccess","USERNAME","cryptoAdmin")
> keyring.set_password("cryptodataaccess","USERNAME","test")
> keyring.set_password("cryptodataaccess","test","test")

#####
start mongo 
> sudo service mongod start 