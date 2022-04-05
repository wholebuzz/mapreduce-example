import type { Context, Mapper, Reducer } from '@wholebuzz/mapreduce/dist/types'
import { tokenizeForHistogram } from '@wholebuzz/search/lib/tokens'

export class WordCountMapper<Key, Value extends { toString: () => string }>
  implements Mapper<Key, Value>
{
  map(_key: Key, value: Value, context: Context<Key, Value>) {
    // console.log('WordCountMapper', value)
    let tokens: any = value.toString()
    tokenizeForHistogram.forEach((tf: (x: any) => any) => (tokens = tf(tokens)))
    for (const token of tokens) context.write(token, 1)
  }
}

export class SumCountsReducer implements Reducer<string, number> {
  reduce(key: string, values: number[], context: Context<string, number>) {
    // console.log('SumCountsReducer', key, values)
    context.write(
      key,
      values.reduce((sum, x) => sum + x, 0)
    )
  }
}
