import { Chart } from "chart.js";
const request = require("request");
import NextCors from 'nextjs-cors';


export default function handler(req, res) {

    NextCors(req, res, {
        // Options
        methods: ['GET', 'HEAD', 'PUT', 'PATCH', 'POST', 'DELETE'],
        origin: '*',
        optionsSuccessStatus: 200, // some legacy browsers (IE11, various SmartTVs) choke on 204
    });

    // const body = {
    //     "projects" : ["project 1", "project 2", "project 3", "project 4", "project 5", "project 6", "project 7"],
    //     "ers" : [120, 100, 40, 50, 60, 80, 200],
    //     "macs" : [40, 100, -10, 10, 15, 25, 30]
    // }

    const body = {
        projects: [ '5 diesel', 'Passenger', 'TJHbj','ewdwe','vfgvf'],
        ers: [ 751, 10751, 233,443,43],
        macs: [ 10, 100,434,54,43 ]
    }

    const options = {
        method: 'POST',
        url: `http://localhost:8000/mac/`,
        json: true,
        body: body
    };

    request(options, (error, response, body) => {
        if (error) {
            res.send(error);
        } else {
            const _body = body;

            if (_body.error) {
                res.send(_body.error);
            } else if (_body) {
                return res.send({data: _body});
            }
        }
    });


}