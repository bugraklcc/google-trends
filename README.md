# docker build

docker build -t google-trends-app -f Dockerfile .

# docker run

YOUR_DIR=`pwd`

docker run -it -p 8081:8081 -v ${YOUR_DIR}:/app google-trends-app bash

python3.9 src/main.py
python3.9 src/trends.py
python3.9 src/plotting.py


