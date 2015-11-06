start "" "C:\Program Files (x86)\Internet Explorer\iexplore.exe"
ping -n 3 1270.0.0.1>nul

start "" "%cd%\yourong.js"
ping -n 60 127.0.0.1>nul

start "" "%cd%\huirendai.js"
ping -n 60 127.0.0.1>nul

start "" "%cd%\minxindai.js"
ping -n 60 127.0.0.1>nul

start "" "%cd%\huirendai_huodong.js"
ping -n 120 127.0.0.1>nul

start "" "%cd%\minxindai_huodong.js"
exit