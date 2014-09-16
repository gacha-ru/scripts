AWS = require("aws-sdk")
credentials = new AWS.SharedIniFileCredentials(profile: "default")
AWS.config.credentials = credentials

# 東京リージョンにセット
AWS.config.update region: "ap-northeast-1"
s3 = new AWS.S3()
s3.listBuckets (err, data) ->
  for index of data.Buckets
    bucket = data.Buckets[index]
    console.log "Bucket: ", bucket.Name, " : ", bucket.CreationDate
  return

