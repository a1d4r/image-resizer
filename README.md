# Image resizer web application

Web service providing API for resizing images. A user can create task
with an image to compress. Eventually, it will be executed and become available 
in original resolution, 64x64 and 32x32.

## Description:

App is running on port `80`
Documentation (swagger): `http://127.0.0.1/docs`

## Run app
    make up

## Run tests:
    make test

## Create venv:
    make venv

## Run linters:
    make lint

## Run formatters:
    make format
