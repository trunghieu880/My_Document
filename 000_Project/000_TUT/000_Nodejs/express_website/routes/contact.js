var express = require('express');
var router = express.Router();
var nodemailer = require('nodemailer');

require('dotenv').config();

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('contact', { title: 'Contact' });
});

router.post('/send', function(req, res, next){
	var transporter = nodemailer.createTransport({
		service: 'gmail',
		auth: {
			user: process.env.EMAIL,
			pass: process.env.PASSWORD
		}
	});

	var mailOptions = {
		from: process.env.EMAIL,
		to: 'trunghieu8804@gmail.com',
		subject: 'Website Submission',
		text: 'You have a new submission with the flowing details... Name: ' + req.body.name + ' Email: ' + req.body.email + ' Message: ' + req.body.message,
		html: '<p>You have a new submission with the flowing details...</p><ul><li>Name: ' + req.body.name + '</li><li>Email: ' + req.body.email + '</li><li>Message: ' + req.body.message + '</ul>'
	}

	transporter.sendMail(mailOptions, function(error, info){
		if (error){
			console.log(error);
			res.redirect('/');
		} else{
			console.log('Message Sent: ' + info.response);
		}
	});
});

module.exports = router;
