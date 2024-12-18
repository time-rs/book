# Arithmetic

Let's suppose you have an ecommerce and you want to show your users the date of arrival of their purchases.

In order to know the arrival date, you would get the today's date and add the amount of time that the delivering process takes. That's sounds possible, but a little verbose for you to write it yourself. Fortunately, the `time` crate has you covered. Let's jump into that!

First, we'll need to import the `OffsetDateTime` struct that has a implementation called `now_utc()` that we can use for discover the current date of our user purchase.

```rust
use time::{OffsetDateTime, Date};

fn get_arrival_date() {

    let current_date: Date = OffsetDateTime::now_utc().date();

}
```

The `OffsetDateTime::now_utc()` returns a `OffsetDateTime` value like this one: `2024-04-06 13:26:19.8381466 +00:00:00`. As we are more interested in the date itself, we use the `.date()` method to get a `Date` struct that we have to import as well. So now our `current date` variable is like this: `2024-04-06`.

Now let's add our estimated time to deliver to that current date. We'll use a method from the `Date` struct called `.checked_add()`. It receives a value of the `Duration` struct measured in seconds and adds to our current date. Let's calculate our a deliver time using the `Duration` struct from `time` first:

```rust

use time::Duration;

let time_to_deliver: Duration  = 45*(Duration::DAY);


```

Considering that we take 45 days to deliver the product(not a very efficient service, I know) we can use the `Duration::DAY` constant that will give the amount of seconds of a day. This helps us to avoid calculting the amount of seconds for ourselves and make our code clear to others as well.

As we take 45 days to deliver, we multiply the amount of seconds returned by 45. Now the `time_to_deliver` variable is a `Duration` that represents our delivering service. Excactly what we need to use the `.checked_add()` method!

```rust

let date_of_arrival:Date = current_date.checked_add(time_to_deliver).expect("Something went wrong");


```

Finally, we use the `.checked_add()` method from our `current_date` variable passing the `time_to_deliver` as a parameter. As this return an `Option<T>` enum, we use `.expect()` to handle when the value returned is `None`. If you are not familiar with the `Option` enum, here is a [link from the Rust Book](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html?highlight=optio#the-option-enum-and-its-advantages-over-null-values) where you can learn more about it!

```rust

use time::{Duration, OffsetDateTime, Date};

fn main() {

    let current_date = OffsetDateTime::now_utc().date();

    let time_to_deliver: Duration  = 48*(Duration::DAY);

    let date_of_arrival:Date = current_date.checked_add(time_to_deliver).expect("Something went wrong");


    println!("Your package will arrive in {}!", date_of_arrival);
}

```

And now our user know when the package will arrive :)
