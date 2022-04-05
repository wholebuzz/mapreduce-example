# [@wholebuzz/mapreduce](https://www.npmjs.com/package/@wholebuzz/mapreduce) Example Project

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
  --plugins ./dist/index.js \
  --map WordCountMapper \
  --reduce SumCountsReducer \
  --combine SumCountsReducer \
  --plugins ./dist/index.js \
  -D valueProperty=value
```
