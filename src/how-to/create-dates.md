# Create dates and times

`time` provides a [`const`][const]-ready API. All functions here are `const`: values can be computed
at compile-time if you pass constants, with no difference if used at runtime.

For convenience, macros are provided with [feature `macros`][feature-macros]. They let us restrict
parameters further, avoiding the need to `unwrap()` at the cost of compilation time.

## Creating [`Date`][Date]s

From a constant value, with [feature `macros`][feature-macros]:

```rust
use time::macros::date;

let _ = date!(2022-01-02);
```

From a calendar date:
```rust
use time::{Date, Month};

let _ = Date::from_calendar_date(2022, Month::January, 2).unwrap();
```

## Creating [`PrimitiveDateTime`][PrimitiveDateTime]s

A `PrimitiveDateTime` is both a date and a time. We can create them directly:

```rust
use time::macros::datetime;

let _ = datetime!(2022-01-02 11:12:13.123_456_789);
```

or use an existing `Date`:

```rust
use time::macros::{date, time};
use time::Time;

let date = date!(2022-01-02);

// A date with 00:00:00 time
let _ = date.midnight();
// You can also provide a desired time...
let _ = date.with_hms(11, 12, 13).unwrap();
// or pass an existing `Time`
let _ = date.with_time(Time::from_hms_nano(11, 12, 13, 123_456_789).unwrap());
// with macros:
let _ = date.with_time(time!(11:12:13.123_456_789));
```

## Creating [`OffsetDateTime`][OffsetDateTime]s

An `OffsetDateTime` is a date, time and [UTC offset][UTC offset, Wikipedia]
. Use it if you deal with timezones:

```rust
use time::macros::datetime;

// When we pass an offset at the end to `datetime!`, it will return an 
// `OffsetDateTime` instead of an `PrimitiveDateTime`
let _ = datetime!(2022-01-02 11:12:13 UTC);
// With a positive offset:
let _ = datetime!(2022-01-02 11:12:13 +1);
// and a negative offset:
let _ = datetime!(2022-01-02 11:12:13.123_456_789 -2:34:56);
```

or, using an existing `PrimitiveDateTime`, with 
[`UtcOffset`][UtcOffset]:

```rust
use time::macros::{datetime, offset};
use time::UtcOffset;

let dt = datetime!(2022-01-02 11:12:13);

// With UTC:
let _ = dt.assume_utc();
// or with another offset:
let _ = dt.assume_offset(UtcOffset::from_hms(1, 2, 3));
// with macros:
let _ = dt.assume_offset(offset!(-11));
```

[const]: https://doc.rust-lang.org/std/keyword.const.html
[feature-macros]: https://docs.rs/time/latest/time/#feature-flags
[Date]: https://docs.rs/time/latest/time/struct.Date.html
[PrimitiveDateTime]: https://docs.rs/time/latest/time/struct.PrimitiveDateTime.html
[OffsetDateTime]: https://docs.rs/time/latest/time/struct.OffsetDateTime.html
[UTC offset, Wikipedia]: https://en.wikipedia.org/wiki/UTC_offset
[UtcOffset]: https://docs.rs/time/latest/time/struct.UtcOffset.html