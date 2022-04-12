## Local setup

```console
$ yarn && yarn build
```

## Count words in README locally

```console
$ yarn mapreduce -v \
  --inputFormat txt \
  --inputPaths ./README.md \
  --outputPath ./wordCounts.jsonl \
  --map WordCountMapper \
  --reduce SumCountsReducer \
  --combine SumCountsReducer \
  --plugins ./dist/index.js \
  -D valueProperty=value
```

## Count `title` words in the [supplied test data](https://github.com/wholebuzz/mapreduce/tree/main/test) locally

```console
$ yarn mapreduce -v \
  --inputPaths ~/mapreduce/test/test-SSSS-of-NNNN.json.gz \
  --outputPath ./wordCounts.jsonl \
  --map WordCountMapper \
  --reduce SumCountsReducer \
  --combine SumCountsReducer \
  --plugins ./dist/index.js \
  -D inputValueProperty=props.title \
  -D valueProperty=value
```

