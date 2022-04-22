# @wholebuzz/mapreduce-example

## Example project for [@wholebuzz/mapreduce](https://www.npmjs.com/package/@wholebuzz/mapreduce)

This project illustrates running a custom Mapper and Reducer in various scheduling scenarios:

- [airflow](airflow): Various [Apache Airflow](https://airflow.apache.org/) operators and examples.
- [docker](docker): Examples of running the tasks in local Docker containers.
- [helm](helm): Example running on [Kubernetes](https://kubernetes.io/) with [Helm](https://helm.sh/).
- [gce](gce): Example starting directly on [Google Compute Engine](https://cloud.google.com/compute).
- [local](local): Examples of running the tasks locally.

For example tasks, we'll:

- Count the words in this [README.md](README.md)
- Count the words in the `title` property of records in the test dataset
- Sort the test dataset by `date`, `guid` and `id`
- Join two separate datasets, each sorted (and sharded) by `guid` 

The [supplied test dataset](https://github.com/wholebuzz/mapreduce/tree/main/test) consists of
a collection of 10,000 headlines of the form:

```json
{
  "id": 28,
  "date": "2021-10-17T08:52:05.000Z",
  "guid": "https://metro.co.uk/?p=15435904",
  "link": "https://metro.co.uk/2021/10/17/mum-of-six-creates-hallway-tribute-to-her-kids-for-less-than-80-15435904/",
  "feed": "https://metro.co.uk/feed/",
  "props": {
    "title": "Mum-of-six creates sweet hallway tribute to her kids – for less than £80",
    "summary": "'It proves you don’t need to spend lots of money to transform your home.'",
    "imageUrl": "https://wholenews-images.storage.googleapis.com/261d2f38dfd584f5e83130fe504934fb.png"
  },
  "tags": {
    "topic": "PARENTS",
    "locale": "en-GB",
    "topics": [
      "Interiors",
      "DIY"
    ],
    "category": "national",
    "classifiedCategory": "national"
  }
}
```
