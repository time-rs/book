# Introduction

`time` is a date and time library for Rust. It is:

- **Easy and safe**. `time` has a
[straightforward API](https://time-rs.github.io/api/time/struct.OffsetDateTime.html) without
footguns.
- **space optimal and efficient**. `time` provides support for dates in the ±9999 year range, with
nanosecond precision; ranges up to ±999,999 are supported with the `large-dates` feature.
- **`serde` ready**. Supports ISO8601, RFC2822 and RFC3339 with the `serde-well-known` feature.
Not in the list? [Make your format](./api/format-description.md).
- **`const` ready**. A majority of the API is `const`, making it ready for resource-constrained
applications, with optional [macros](https://time-rs.github.io/api/time/macros/index.html) for easy
date creation.
- **`no-std` support** with `alloc` and `std` features.
- **numeric traits**. Use durations easily: `2.seconds()`.
- Supports Windows, Linux, macOS,
[WebAssembly](https://developer.mozilla.org/fr/docs/WebAssembly) targets among others.
- Six-month
[minimum supported Rust version](https://rust-lang.github.io/rfcs/2495-min-rust-version.html)
guarantee.

And more...

## Getting started

This short tutorial describes basic usage of `time`, to get operational quickly.

1. **Install `time`**.  Add it to your `Cargo.toml`. We'll enable `macros`:
```toml
[dependencies]
time = { version = "0.3", features = ["macros"] }
```

2. **Create dates and times.** We can create dates
([`Date`](https://docs.rs/time/latest/time/struct.Date.html)),
dates with times
([`PrimitiveDateTime`](https://docs.rs/time/latest/time/struct.PrimitiveDateTime.html))
and date times with an UTC offset
([`OffsetDateTime`](https://docs.rs/time/latest/time/struct.OffsetDateTime.html)).
A simple [`Time`](https://docs.rs/time/latest/time/struct.Time.html) is also available.

```rust
use time::{Date, PrimitiveDateTime, OffsetDateTime, UtcOffset};
use time::Weekday::Wednesday;

let date = Date::from_iso_week_date(2022, 1, Wednesday).unwrap();
let datetime = date.with_hms(13, 0, 55).unwrap();
let datetime_off = datetime.assume_offset(UtcOffset::from_hms(1, 2, 3).unwrap());

println!("{date}, {datetime}, {datetime_off}");
// 2022-01-01, 2022-01-01 13:00:55.0, 2022-01-01 13:00:55.0 +01:02:03
```

With the `macros` feature:

```rust
use time::macros::{date, datetime};

let date = date!(2022-01-01);
let datetime = datetime!(2022-01-01 13:00:55);
let datetime_off = datetime!(2022-01-01 13:00:55 +1:02:03);

println!("{date}, {datetime}, {datetime_off}");
// 2022-01-01, 2022-01-01 13:00:55.0, 2022-01-01 13:00:55.0 +01:02:03
```

3. **Manipulate dates and use
[`Duration`s](https://time-rs.github.io/api/time/struct.Duration.html)**:
```rust
use time::Duration;
use time::macros::{datetime};

let a = datetime!(2022-01-01 10:00:55);
let b = datetime!(2022-01-01 13:00:00);

let duration: Duration = b - a;

println!("{}", b - a);
// 2h59m5s
```

## `time` vs `chrono`

time 0.1 was originally a thin wrapper around libc time functions. Because it was relatively
barebones, [`chrono`](https://docs.rs/chrono/0.4.19/chrono/) was developed as a richer API on top
of time 0.1.

Around 2019, the time crate, which was unmaintained since August 2016, was picked up for maintenance
again. `time` has since been rewritten as of time 0.2, and is incompatible with the 0.1 version.

Today:
- `time` has been rewritten from 0.1,and is actively developed.
- `chrono` depends on time 0.1, an old version unrelated with current `time`, and is actively
developed as well.

Since they are incompatible with each other, please choose the library that fits your needs.
