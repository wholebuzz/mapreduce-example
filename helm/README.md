# [Helm](https://helm.sh/) @wholebuzz/mapreduce examples

## Deploy input and plugin to shared storage

```
$ export MY_BUCKET=gs://mapreduce-jobs
$ gsutil cp README.md $MY_BUCKET
$ gsutil cp dist/index.js $MY_BUCKET
```

## Count words in README

```console
$ kubectl delete job mapreduce-wordcount
$ helm template mapreduce-job . --set args="--inputFormat txt --inputPaths $MY_BUCKET/README.md --outputPath $MY_BUCKET/wordCounts.jsonl --shuffleDirectory $MY_BUCKET/mapreduce/ --map WordCountMapper --reduce SumCountsReducer --combine SumCountsReducer --plugins $MY_BUCKET/index.js -D valueProperty=value" | kubectl apply -f -
```

## Check output

```console
$ gsutil cp $MY_BUCKET/wordCounts.jsonl -
```
