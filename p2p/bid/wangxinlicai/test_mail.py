import os

mail_title = 'firstp2p is not all finished'
mail_content = ''
mail_box = '82213802@qq.com'

os.system('echo ' + mail_content + ' | mail -s "' + mail_title + '" ' + mail_box)
