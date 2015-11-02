var casper = require('casper').create(); 

casper.start('http://www.huirendai.com/index.php?user&q=action/login', function () {   
	this.fill('form#userlogin_form', {
		'keywords' : '18211085003',
		'password' : 'csujk4236238'
	}, true);
	this.echo("split huirendai_1.png ...");
	//this.capture("huirendai_1.png");
});

casper.then(function () {
	this.click('button[id="btnSubmit"]');
});

casper.then(function () {
	this.echo(this.getTitle());
	this.echo("split huirendai_2.png ...");
	//this.capture("huirendai_2.png");
}); 

casper.run(); 
