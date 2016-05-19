
ps -ef | grep 'php monitor_main.php' | awk '{print $2}' | xargs kill -9

nohup php monitor_main.php 1>log1.txt 2>log2.txt &
