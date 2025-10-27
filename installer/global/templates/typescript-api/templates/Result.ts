// src/common/types/result.type.ts

/**
 * Result type for explicit error handling
 * Represents either a successful result (Ok) or an error (Err)
 */
export type Result<T, E = Error> = Ok<T> | Err<E>;

export class Ok<T> {
  readonly ok = true;
  readonly err = false;

  constructor(readonly val: T) {}

  map<U>(fn: (value: T) => U): Result<U, never> {
    return new Ok(fn(this.val));
  }

  flatMap<U, E>(fn: (value: T) => Result<U, E>): Result<U, E> {
    return fn(this.val);
  }

  match<U>(onOk: (value: T) => U, onErr: (error: never) => U): U {
    return onOk(this.val);
  }

  unwrap(): T {
    return this.val;
  }

  unwrapOr(_defaultValue: T): T {
    return this.val;
  }

  isOk(): this is Ok<T> {
    return true;
  }

  isErr(): this is never {
    return false;
  }
}

export class Err<E> {
  readonly ok = false;
  readonly err = true;

  constructor(readonly val: E) {}

  map<U>(_fn: (value: never) => U): Result<U, E> {
    return new Err(this.val);
  }

  flatMap<U>(_fn: (value: never) => Result<U, E>): Result<U, E> {
    return new Err(this.val);
  }

  match<U>(onOk: (value: never) => U, onErr: (error: E) => U): U {
    return onErr(this.val);
  }

  unwrap(): never {
    throw new Error(`Called unwrap on an Err value: ${this.val}`);
  }

  unwrapOr<T>(defaultValue: T): T {
    return defaultValue;
  }

  isOk(): this is never {
    return false;
  }

  isErr(): this is Err<E> {
    return true;
  }
}

// Result utility functions
export const Ok = <T>(value: T): Result<T, never> => new Ok(value);
export const Err = <E>(error: E): Result<never, E> => new Err(error);

/**
 * Combine multiple results into a single result
 * Returns Ok with tuple of values if all are Ok, otherwise returns first Err
 */
export function combineResults<T1, T2, E>(
  result1: Result<T1, E>,
  result2: Result<T2, E>
): Result<[T1, T2], E> {
  if (result1.err) return result1;
  if (result2.err) return result2;
  return Ok([result1.val, result2.val]);
}

/**
 * Combine three results into a single result
 */
export function combineResults3<T1, T2, T3, E>(
  result1: Result<T1, E>,
  result2: Result<T2, E>,
  result3: Result<T3, E>
): Result<[T1, T2, T3], E> {
  if (result1.err) return result1;
  if (result2.err) return result2;
  if (result3.err) return result3;
  return Ok([result1.val, result2.val, result3.val]);
}

/**
 * Map over array of results, collecting all values or returning first error
 */
export function collectResults<T, E>(results: Result<T, E>[]): Result<T[], E> {
  const values: T[] = [];

  for (const result of results) {
    if (result.err) {
      return result;
    }
    values.push(result.val);
  }

  return Ok(values);
}

/**
 * Transform async function to return Result instead of throwing
 */
export async function tryCatch<T, E = Error>(
  fn: () => Promise<T>,
  errorMapper?: (error: unknown) => E
): Promise<Result<T, E>> {
  try {
    const result = await fn();
    return Ok(result);
  } catch (error) {
    const mappedError = errorMapper ? errorMapper(error) : (error as E);
    return Err(mappedError);
  }
}

/**
 * Transform sync function to return Result instead of throwing
 */
export function tryCatchSync<T, E = Error>(
  fn: () => T,
  errorMapper?: (error: unknown) => E
): Result<T, E> {
  try {
    const result = fn();
    return Ok(result);
  } catch (error) {
    const mappedError = errorMapper ? errorMapper(error) : (error as E);
    return Err(mappedError);
  }
}

/**
 * Type guard to check if result is Ok
 */
export function isOk<T, E>(result: Result<T, E>): result is Ok<T> {
  return result.ok;
}

/**
 * Type guard to check if result is Err
 */
export function isErr<T, E>(result: Result<T, E>): result is Err<E> {
  return result.err;
}