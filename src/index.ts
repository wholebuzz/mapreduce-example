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

// Run with -D valueProperty=value
export class SumCountsReducer implements Reducer<string, number> {
  async setup(context: Context<string, number>) {
    // Using number[] for values type requires a valueProperty to dereference the underlying object
    if (!context.valueProperty)
      throw new Error(`SumCountsReducer requires valueProperty ${JSON.stringify(context)}`)
  }

  reduce(key: string, values: number[], context: Context<string, number>) {
    // console.log('SumCountsReducer', key, values)
    context.write(
      key,
      values.reduce((sum, x) => sum + x, 0)
    )
  }
}

// Don't run with -D valueProperty=value. Optionally run with -D myValueProperty=value
export class SumCounts2Reducer implements Reducer<string, Record<string, any>> {
  reduce(
    key: string,
    underlyingObjects: Array<Record<string, any>>,
    context: Context<string, number>
  ) {
    const values = underlyingObjects.map((x) => x[context.configuration.myValueProperty || 'value'])
    // console.log('SumCounts2Reducer', key, underlyingObjects, values)
    context.write(
      key,
      values.reduce((sum, x) => sum + x, 0)
    )
  }
}
