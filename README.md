# GYM

### Description:
GYM is a sports application that 
allows you to design numerous sports 
exercises for different muscles group.
All exercises can be unionised in training.
Training consists of exercises, duration and difficulty.
All the application support authorization, firstly make user 
send username and password to `/users` after that make post request on
`auth/token` with the same credentials and use provided token for auth.
User can get training sending request on `/trains/{train_id}`, the train
will be added to the user history, use `/users/me/history` to get list of 
requested trainings. The application contains an admin panel 
that allows you easily to manipulate data.
At the moment, the application presents as API. 
To see full documentation, launch the [app](#run-app) and go 
to `http://0.0.0.0:8000/docs`

### Create venv:
    make venv

### Run app in docker
    make up-docker

### Run app locally
    make up

### Run admin locally
    make admin

### Run tests:
    make test

### Run linters:
    make lint

### Run formatters:
    make format
