import type {
  Context,
  Key,
  Mapper,
  MapReduceJobConfig,
  Value,
} from '@wholebuzz/mapreduce/dist/types'

export class WordCountMapper implements Mapper {
  valueProperty = ''

  configure(args: MapReduceJobConfig) {
    this.valueProperty = args.configuration?.valueProperty || 'value'
  }

  map(key: Key, value: Value, context: Context) {
    context.write(key, value)
  }
}
