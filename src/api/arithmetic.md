# Arithmetic

Let's suppose you are creating an finance app for people who are above 18 years old. Normally, instead of asking the age itself, you would ask for the birthdate to track the age evolution, rigth?

In order to know the user age, you would get the today's date and subtract the user birthdate. That's sounds possible, but a little verbose for you to write it yourself. Fortunately, the `time` crate has you covered. Let's jump into that!

First, let's consider the user input being `"2000-30-10"`. This input need to be parsed to the `Date` type. The parsing feature needs to be explicited stated in your `Cargo.toml` file, otherwise it won`t work. Here is an example:

```rust
//Cargo.toml file

[dependencies]
time = { version = "0.3", features = ["parsing"] }
```

Now we can import the `Date` with the parsing feature. We'll need a parsing type as well and we're going to use `Iso8601` in this one. Do not feel attached to the formatting now, you can change it later and this will be stated later in this book!

And, finally, we will use the OffsetDateTime to get the current date. Here we go then:

```rust
use time::{Date, OffsetDateTime};
use time::format_description::well_known::Iso8601;

fn get_age() {

    let current_date = OffsetDateTime::now_utc().date();
    let user_birthdate = Date::parse("2000-10-30", &Iso8601::DATE).unwrap();

}
```

Let's recap. In this code we are `OffsetDateTime::now_utc()` to get the current date with the timestamp and using the method `.date()` to select only the date itself in order to get the same format as our user input.

Now we have to take the `user_birthdate` from the `current_date` in order to know the age gap between these two dates. Here is how we are going to do that:

```rust
let gap_seconds = (current_date - user_birthdate).whole_seconds();
```

When we do `current_date - user_birthdate` we get an `Duration` type. You can take out the `.whole_seconds` method and see the output in the terminal:

```console
Finished dev [unoptimized + debuginfo] target(s) in 0.73s
     Running `target\debug\rust_test.exe`

Duration {
    seconds: 739411200,
    nanoseconds: 0,
}
```

And then we use the `.whole_seconds` to get the gap between the dates in seconds. Now we just have to convert this in years. That`s the easy part! We just have to calculate how many seconds there are in a year and divide the gap we found by this number of seconds.

```rust

const SECONDS_PER_YEAR: i64 = 365*24*60*60;

let years = gap_seconds/SECONDS_PER_YEAR;

```

Knowing how many years our user has, we can use the a simple `if else` clause to tell him if he can open an account in our app:

```rust

if years >= 18{
        println!("You're {years} years old and able to open an account :)");
    }
    else{
        println!("You're only {years} years old. To open an account, you have to have at least 18 years old");
    }


```

Here is the complete code :)

```rust

use time::{Date, OffsetDateTime};
use time::format_description::well_known::Iso8601;

fn get_age() {
    const SECONDS_PER_YEAR: i64 = 365 * 24 * 60 * 60;

    let user_birthdate = Date::parse("2000-10-30", &Iso8601::DATE).unwrap();
    let current_date = OffsetDateTime::now_utc().date();

    let gap_seconds = (current_date - user_birthdate).whole_seconds();

    let years = gap_seconds / SECONDS_PER_YEAR;

    if years >= 18 {
        println!("You're {} years old and able to open an account :)", years);
    } else {
        println!("You're only {} years old. To open an account, you have to be at least 18 years old", years);
    }
}

fn main() {
    get_age();
}



```
