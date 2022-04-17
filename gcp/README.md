# GCP @wholebuzz/mapreduce examples

## Deploy input, plugin, and startup.sh to shared storage

```
$ export MY_BUCKET=gs://mapreduce-jobs
$ gsutil cp README.md $MY_BUCKET
$ gsutil cp dist/index.js $MY_BUCKET
$ gsutil cp gcp/startup.sh $MY_BUCKET
```

## Count words in README

```console
$ gcloud compute instances create mapreduce-wordcount \
--zone us-west2-b \
--metadata=image_name=wholebuzz/mapreduce,\
container_param="--inputFormat txt --inputPaths $MY_BUCKET/README.md --outputPath $MY_BUCKET/wordCount.jsonl --map WordCountMapper --reduce SumCountsReducer --combine SumCountsReducer --plugins $MY_BUCKET/index.js -D valueProperty=value",\
startup-script-url=https://$MY_BUCKET.storage.googleapis.com/startup.sh \
--scopes=https://www.googleapis.com/auth/cloud-platform --image-family=cos-stable \
--image-project=cos-cloud \
--boot-disk-size "50GB" \
--preemptible
```

## Check output

```console
$ gsutil cp $MY_BUCKET/wordCounts.jsonl -
```
