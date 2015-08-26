require('babel/polyfill');

import express from 'express';
import { json } from 'body-parser';
import { Server as http } from 'http';
import dom from 'vd';

// app setup
let app = express();
let srv = http(app);
