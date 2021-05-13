# Extension traits

The time crate contains two extension traits: `time::ext::NumericalDuration` and
`time::ext::NumericalStdDuration`. These traits exist to make writing code involving durations (both
from the time crate and the standard library) cleaner to read. Rather than writing
`Duration::seconds(5)`, it is possible to write `5.seconds()`. It is possible to use floating point
literals such that `1.5.weeks()` is equivalent to `3.days() + 12.hours()`.

`NumericalDuration` provides the following methods that return a `time::Duration`:

- `.nanoseconds()`
- `.microseconds()`
- `.milliseconds()`
- `.seconds()`
- `.minutes()`
- `.hours()`
- `.days()`
- `.weeks()`

`NumericalStdDuration` provides the following methods that return a `core::time::Duration`:

- `.std_nanoseconds()`
- `.std_microseconds()`
- `.std_milliseconds()`
- `.std_seconds()`
- `.std_minutes()`
- `.std_hours()`
- `.std_days()`
- `.std_weeks()`

The `NumericalDuration` trait is implemented for `i64` and `f64`, such that both integer and float
literals are able to use the methods. The `NumericalStdDuration` trait is implemented for `u64` and
`f64` for the same reasons, though the latter will perform a runtime check ensuring the value is
non-negative.

While it is possible to use these extension methods on non-literals, such usage is discouraged for
ease of reading.
