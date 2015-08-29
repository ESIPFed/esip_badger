require('babel/polyfill');

import express from 'express';
import { json } from 'body-parser';
import { Server as http } from 'http';
import dom from 'vd';
import badge from './badge';
// import iframe from './iframe';
import log from './log';

export default function esip_badger({
	alias,
	repo
}){

	// app setup
	let app = express();
	let srv = http(app);
	let assets = __dirname + '/assets';

	var router = express.Router();

	// badge renderer
	app.use('/esip_badger.js', express.static(assets + '/badge.js'))

	// badge generator
	//
	router.get('/:badge.svg', (req, res) => {
		res.type('svg');
		res.set('Cache-Control', 'max-age=0, no-cache');
		res.set('Pragma', 'no-cache');
		res.send(badge(req.params.badge).toHTML());
	});

	app.use('/', router);

	return srv;
}