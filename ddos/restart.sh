ps -ef | grep 'python ddos.py' | awk '{print $2}' | xargs kill -9
nohup python ddos.py 1>log.txt 2>err.txt &
