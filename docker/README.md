# Docker @wholebuzz/mapreduce examples

## Count words in README

```console
$ export MY_JOB_ID=`yarn --silent mapreduce job --new | tail -1 | jq -r ".jobid"`
$ docker run \
  -v $PWD:/mnt-cwd \
  --rm -it wholebuzz/mapreduce \
  --jobid $MY_JOB_ID \
  --map WordCountMapper \
  --reduce SumCountsReducer \
  --combine SumCountsReducer \
  --plugins /mnt-cwd/dist/index.js \
  --inputFormat txt \
  --inputPaths /mnt-cwd/README.md  \
  --outputPath /mnt-cwd/wordCounts.jsonl \
  --shuffleDirectory /mnt-cwd/ \
  -D valueProperty=value
```

## Count `title` words in the [supplied test data](https://github.com/wholebuzz/mapreduce/tree/main/test)

```console
$ export MY_JOB_CONFIG=`yarn --silent mapreduce job --new \
  --map WordCountMapper \
  --reduce SumCountsReducer \
  --combine SumCountsReducer \
  --inputPaths /test/test-SSSS-of-NNNN.json.gz \
  --outputPath /mnt-cwd/wordCounts.jsonl \
  --plugins /mnt-cwd/dist/index.js \
  --shuffleDirectory /mnt-cwd/ \
  --numWorkers 3 \
  -D inputValueProperty=props.title \
  -D valueProperty=value \
  | tail -1`
$ for ((i = 0; i < 3; i++)); do
    docker run \
      -v $PWD:/mnt-cwd \
      -v ~/mapreduce/test:/test \
      --rm -d -it wholebuzz/mapreduce --jobConfig "$MY_JOB_CONFIG" --workerIndex $i
  done
```
