<style>
@media not print {
  .ayu img[src$='#rr'], .navy img[src$='#rr'], .coal img[src$='#rr'] {
    filter: invert(0.8) hue-rotate(180deg);
  }
}

@media (prefers-color-scheme: dark) {
  .light.no-js img[src$='#rr'] {
    filter: invert(0.8) hue-rotate(180deg);
  }
}
</style>

# Format description

A format description is the manner in which the time crate knows how a value should be formatted and
parsed. However, a format description is not a single type; it is instead represented by two
internal traits (one for formatting and one for parsing) that are implemented by a number of types.
Currently, all types that implement one trait also implement the other, but this is not guaranteed.

The following types currently implement both the `Formattable` and `Parsable` traits:

- `FormatItem<'_>`
- `[FormatItem<'_>]`
- `T where <T as Deref>::Target: Formattable` (or `Parsable`)
- All [well known formats](./well-known-format-descriptions.md)

While it is possible to construct a value manually, this is generally not recommended, as it is more
tedious and less readable than the alternative. Unless you are constructing a `FormatItem` manually,
you will likely never need to know anything about it other than that it is produced by the
`format_description!` macro or `format_description::parse` method.

If the format description is statically known, you should use the `format_description!` macro. This
is identical to the `format_description::parse` method, but runs at compile-time, throwing an error
if the format description is invalid. If you do not know the desired format statically (such as if
you are using one provided by the user), you should use the `format_description::parse` method,
which is fallible.

Format descriptions have **components** and **literals**. Literals are formatted and parsed as-is.
Components are the mechanism by which values (such as a `Time` or `Date`) are dynamically formatted
and parsed. They have significant flexibility, allowing for differences in padding, variable widths
for subsecond values, numerical or textual representations, and more.

The syntax for the method and the macro is identical.

![syntax for full format description](../diagrams/abbreviated.svg#rr)

Either a literal or a component may be present at the start of the format description. It is valid
to have both consecutive literals and consecutive components. Components must be fully contained
between brackets with optional whitespace. If a literal `[` is desired, it must be escaped with a
second bracket. A closing bracket need not be escaped if alone.

## Examples

Time format descriptions can be created at compile-time using `time::macros::format_description!`;
code will not compile if parsing of the format fails. Alternately,

To parse an `OffsetDateTime` from a string like `Thu, 06 Jan 2022 02:53:35 00:00`, we can use the
following format description:

```rust
use time::macros::format_description;

static EXPIRES_TIME_FORMAT: &[FormatItem<'_>] = format_description!(
    "[weekday repr:short], [day padding:zero] [month repr:short] [year repr:full] \
        [hour repr:24 padding:zero]:[minute padding:zero]:[second padding:zero] \
        [offset_hour padding:zero]:[offset_minute padding:zero]"
);
```

And we can parse a datetime like so:

```rust
use time::OffsetDateTime;

fn parse() -> OffsetDateTime {
    OffsetDateTime::parse("Thu, 06 Jan 2022 02:53:35 00:00", EXPIRES_TIME_FORMAT).unwrap()
}
```

## Components

What follows is the syntax for all components. Any of the following may be used where _component_
is present in the above diagram.

- **Day of month**: `day`

  ![syntax for day component](../diagrams/day.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **Clock hour**: `hour`

  ![syntax for hour component](../diagrams/hour.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spacing, or having
  no padding at all. The default is to pad the value with zeroes.

  Users have the option to choose between two representations. One is the 12-hour clock, frequently
  used in the Anglosphere, while the alternative (the 24-hour clock) is frequently used elsewhere.
  The 12-hour clock is typically used in conjunction with AM/PM.

- **Minute within the clock hour**: `minute`

  ![syntax for minute component](../diagrams/minute.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **Month**: `month`

  ![syntax for month component](../diagrams/month.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users have the option to choose between three representations. The default is numerical.
  Alternatives are _long_ and _short_, both of which are textual formats and have no padding. The
  long format is the full English name of the month, while the short format is the first three
  letters of it.

  When parsing, there is the option to consume text-based formats case-insensitively.

- **Whole hours offset from UTC**: `offset_hour`

  ![syntax for offset hour component](../diagrams/offset_hour.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users have the option to choose whether the sign is _automatic_ (the default) or _mandatory_.
  If the sign is automatic, it will only be present when the value is negative. If mandatory, it
  will always be present.

- **Minutes within the hour offset from UTC**: `offset_minute`

  ![syntax for offset minute component](../diagrams/offset_minute.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  This value is always positive. As such, it has no sign.

- **Seconds within the minute offset from UTC**: `offset_second`

  ![syntax for offset second component](../diagrams/offset_second.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  This value is always positive. As such, it has no sign.

- **Day of year**: `ordinal`

  ![syntax for ordinal component](../diagrams/ordinal.svg#rr)

  The padded value has a width of 3. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **AM/PM**: `period`

  ![syntax for period component](../diagrams/period.svg#rr)

  Users have the option to choose whether the value is uppercase or lowercase. This component is
  typically used in conjunction with the hour of the day with `repr:12`.

  When parsing, there is the option to consume text-based formats case-insensitively.

- **Second within the clock minute**: `second`

  ![syntax for second component](../diagrams/second.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **Subsecond within the clock second**: `subsecond`

  ![syntax for subsecond component](../diagrams/subsecond.svg#rr)

  Users have the choice of how many digits should be displayed or parsed. By default, this is
  one or more, where the minimum number of digits will be used when formatting and any nonzero
  number of digits are accepted by the parser (though digits after the ninth will be discarded).
  There is the option to require a fixed number of digits between one and nine. When formatting, the
  value is not rounded if more digits would otherwise be present.

- **Week of the year**: `week_number`

  ![syntax for week number component](../diagrams/week_number.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users can choose between three representations: _iso_ (the default), _sunday_, and _monday_. ISO
  week numbers are in between 1 and 53, while others are between 0 and 53. ISO week one is the
  Monday-to-Sunday week that contains January 4. Week one of other representations begins on the
  first instance of that day in the calendar year (e.g. Sunday-based week numbering has week one
  start on the first Sunday of the year).

- **Day of the week**: `weekday`

  ![syntax for weekday component](../diagrams/weekday.svg#rr)

  Users can choose between a number of representations for the day of the week. There are _long_
  (the default) and _short_, both of which are textual representations; the long representation is
  the weekday's full name in English, while the short is the first three letters. There are also
  _sunday_ and _monday_ representations, which are numerical. These formats are either zero to six
  or one to seven (depending on whether `one_indexed` is false or true, respectively), with the
  named day being at the start of that range.

  When parsing, there is the option to consume text-based formats case-insensitively.

- **Year**: `year`

  ![syntax for year component](../diagrams/year.svg#rr)

  The padded value has a width of 4. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users can choose between two representations: the full year (the default) and the last two digits
  of the year. This should be relatively straightforward. Note that when parsing, if only the last
  two digits of the year are present, the value returned may not be what was expected — if the
  return is successful at all (it's not guaranteed).

  There are two bases for the year: _calendar_ and _iso\_week_. The former is what you want if using
  the month, day, ordinal, or similar. You likely only want to use `iso_week` if you are using the
  week number with `repr:iso`. [Don't be like Twitter](twitter-bug); know which should be used when.

  Users have the option to choose whether the sign is _automatic_ (the default) or _mandatory_.
  If the sign is automatic, it will only be present when the value is negative _or_ if the
  `large-dates` feature is enabled and the value contains more than four digits. If mandatory, it
  will always be present.

  When the `large-dates` feature is enabled, ambiguities may exist when parsing. For example, if a
  year is immediately followed by the week number, the parser will eagerly consume six digits even
  if the year should only be four and the week number the remaining two.

  [twitter-bug]: https://www.theguardian.com/technology/2014/dec/29/twitter-2015-date-bug
