# aiohttp_training
Test project to learn how to work with aiohttp framework

**How to get the code:**

git clone https://github.com/ArtyomKozyrev8/aiohttp_react_test.git

docker build -t aio_re_serv .

**How to run as a standalone application on local PC without Docker:**

python -m aiohttp.web -H 0.0.0.0 -P 8090 app:init_func

**How to run with Gunicorn (not work in Windows)**

gunicorn app:init_func_gunicorn --bind 0.0.0.0:8090 --worker-class aiohttp.GunicornWebWorker

**Run as independent app in Docker without Nginx:**

docker run -d --name aio_re_serv -p 8090:8090 aio_re_serv

**Run with Nginx:** 

docker run --network=aio_re_net -d --name aio_re_serv aio_re_serv

