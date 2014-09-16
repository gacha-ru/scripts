var AWS = require('aws-sdk');

var credentials = new AWS.SharedIniFileCredentials({profile: 'default'});
AWS.config.credentials = credentials;
// 東京リージョンにセット
AWS.config.update({region: 'ap-northeast-1'});

var s3 = new AWS.S3();

s3.listBuckets(function(err, data) {
  for (var index in data.Buckets) {
    var bucket = data.Buckets[index];
    console.log("Bucket: ", bucket.Name, ' : ', bucket.CreationDate);
  }
});
