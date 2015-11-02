var casper = require('casper').create();

var fs = require('fs'); 

casper.start('http://mp3.sogou.com/music.so?query=%D5%D4%B4%F3%B8%F1', function() {
	var url = 'http://mp3.sogou.com/music.so?query=%D5%D4%B4%F3%B8%F1';
	this.download(url, 'mp3.html');
	fs.write('sogou_mp3.html', this.getHTML(), 'w'); 
});

casper.run(function() {
	this.echo('Done.').exit();
});
