var parser = require('osu-mania-parser');
const fs = require('fs');

var beatmap = parser.parseFileSync('./map.osu');

fs.writeFileSync(`./beatmap.json`, JSON.stringify(beatmap, null, 4))