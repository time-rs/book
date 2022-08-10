# Parse dates

`time` has can parse datetimes from strings, in any given format.

## Parse a date from a string

1. Enable [feature `parsing`][feature-parsing].

2. Using the common ISO 8601 format, via the [`Iso8601`][Iso8601] format description:

```rust
use time::format_description::well_known::Iso8601;
use time::PrimitiveDateTime;

let date = PrimitiveDateTime::parse("2022-01-02T11:12:13", &Iso8601::DEFAULT)
    .unwrap();
```

## Parsing custom formats

`time` supports a few common formats, that we call [well-known formats][well-known]. We support 
arbitrary formats as well.

1. Enable [feature `macros` and `parsing`](https://docs.rs/time/latest/time/#feature-flags). 
   `macros` are used to call `format_description!`, but you can also call 
   [the equivalent function](https://docs.rs/time/latest/time/format_description/fn.parse.html).

2. Create a format and parse:

```rust
use time::macros::format_description;
use time::Time;

let my_format = format_description!("h=[hour],m=[minute],s=[second]");
let time = Time::parse("h=11,m=12,s=13", &my_format).unwrap();
```

[Reference for format descriptions can be found here](../api/format-description.md).

## Parsing into structs with serde

For convenience, you can use Serde with `time`.

1. Enable [feature `serde-well-known`][serde-well-known].

2. Create a struct and parse from a format, eg. JSON using [`serde-json`][serde-json]:

```rust
use time::macros::format_description;
use time::{OffsetDateTime, Time};
use serde::{Deserialize};

#[derive(Deserialize)]
struct Notification {
    message: String,
    #[serde(with = "time::serde::iso8601")]
    timestamp: OffsetDateTime,
}

fn main() {
    let input = r#"{
      "message": "foo",
      "timestamp": "2022-01-02T11:12:13Z"
    }"#;

    let notification: Notification = serde_json::from_str(input).unwrap();
    println!("{:?}", notification.timestamp);
}
```

[feature-parsing]: https://docs.rs/time/latest/time/#feature-flags
[Iso8601]: https://docs.rs/time/latest/time/format_description/well_known/struct.Iso8601.html
[well-known]: https://docs.rs/time/latest/time/format_description/well_known/index.html
[feature-serde-well-known]: https://docs.rs/time/latest/time/#feature-flags
[serde-json]: https://docs.rs/serde_json/latest/serde_json/