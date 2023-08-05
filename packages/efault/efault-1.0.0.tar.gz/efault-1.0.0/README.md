
## For developers

Create a docker container (do it once)
$ make create

Start the container and log in
$ make shell

Create a python virtual environment (do it once)
$ python3 -m venv env

Activate the virtual environment
$ source env/bin/activate

Install efault and any build dependency
$ pip install -e .
