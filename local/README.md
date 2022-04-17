# Local @wholebuzz/mapreduce examples

## Setup

```console
$ yarn && yarn build
```

## Count words in README

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

## Count `title` words in the [supplied test data](https://github.com/wholebuzz/mapreduce/tree/main/test)

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

With SumCounts2Reducer no "-D valueProperty" is required:

```console
$ yarn mapreduce -v \
  --inputPaths ~/mapreduce/test/test-SSSS-of-NNNN.json.gz \
  --outputPath ./wordCounts.jsonl \
  --map WordCountMapper \
  --reduce SumCounts2Reducer \
  --combine SumCounts2Reducer \
  --plugins ./dist/index.js \
  -D inputValueProperty=props.title
```

