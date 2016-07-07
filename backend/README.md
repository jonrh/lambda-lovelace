# Backend
This folder contains our backend code: Python Flask web service and recommender system.

## Docker
Here is how to build our Docker backend image and name it *lovelace*. This assumes we are in a terminal located in the root *lambda-lovelace/* folder.

```
cd backend/
docker build -t lovelace .
```

To run our *lovelace* image (assuming we're in the *backend/* folder):

```
docker run -it -p 5000:5000 lovelace
```

## Setup instructions on OSX
Homebrew:
gcc -> includes a gfortran compiler. Required for pip to be able to install scipy.

