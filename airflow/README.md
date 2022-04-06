## Run on Airflow

### Deploy input and plugin to shared storage

```
$ export MY_BUCKET=s3://av8-mapreduce-jobs
$ aws s3 cp README.md $MY_BUCKET
$ aws s3 cp dist/index.js $MY_BUCKET
```

### Trigger mapreduce DockerOperataor

```console
$ airflow dags trigger -c "{
  \"map\": \"WordCountMapper\",
  \"reduce\": \"SumCountsReducer\",
  \"input_paths\": \"$MY_BUCKET/README.md\",
  \"output_path\": \"$MY_BUCKET/wordCounts.jsonl\",
  \"shuffle_directory\": \"$MY_BUCKET/\",
  \"config\": \"--inputFormat txt --combine SumCountsReducer --plugins $MY_BUCKET/index.js -D valueProperty=value\"
}" mapreduce1_docker 
```

### Check output

```console
$ aws s3 cp $MY_BUCKET/wordCounts.jsonl -
```
