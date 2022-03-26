# mapreduce-example

## Count words in README

```console
$ yarn mapreduce \
  --inputPaths ./README.md \
  --outputPath ./wordCounts.jsonl \
  --plugins ./dist/index.js \
  --map WordCountMapper \
  --reduce IdentityReducer 
```
