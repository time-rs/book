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

While it is possible to construct a format description manually, this is generally not recommended,
as it is more tedious and less readable than the alternative. Unless you are doing this, you will
likely never need to know anything about `FormatItem` other than that it is produced by the
`format_description!` macro or any of the various parsing methods.

If the format description is statically known, you should use the `format_description!` macro. This
is identical to the `format_description::parse` method, but runs at compile-time, throwing an error
if the format description is invalid. If you do not know the desired format statically (such as if
you are using one provided by the user), you should use the `format_description::parse_owned` method
(or similar method in the `format_description` module), which is fallible.

Format descriptions have **components** and **literals**. Literals are formatted and parsed as-is.
Components are the mechanism by which values (such as a `Time` or `Date`) are dynamically formatted
and parsed. They have significant flexibility, allowing for differences in padding, variable widths
for subsecond values, numerical or textual representations, and more.

Either a literal or a component may be present at the start of the format description. It is valid
to have both consecutive literals and consecutive components. Components must be fully contained
between brackets with optional whitespace. Escaping behavior varies by version, and is described
below.

## Versioning

There are multiple versions of the format description syntax in `time`. Similar to Rust editions,
all versions are and will remain supported indefinitely. Some features may only be available in
newer versions for technical reasons.

In most cases, you do not need to worry about the version of the format description. However,
there are some differences.

### Differences

| Literal | Version 1 | Version 2 |
| ------- | --------- | --------- |
| `[`     | `[[`      | `\[`      |
| `]`     | `]`       | `\]`      |
| `\`     | `\`       | `\\`      |

`[first]` and `[optional]` are supported in both version 1 and version 2, but individual methods may
prevent their use. This is because some methods return a format description that is entirely
borrowed. However, when parsing `[first]` and `[optional]`, the generated sequence is necessarily
owned. For this reason, you will need to use the `format_description::parse_owned` method or the
`format_description!` macro to use these components.

### Version used

[`format_description::parse`] uses version 1 unconditionally. This is the only method that has a
non-configurable version. [`format_description::parse_borrowed`] and
[`format_description::parse_owned`] require the user to specify the version. If the version is not
valid, compilation will fail. [`format_description!`] defaults to version 1, but can be configured
to use a different version.

[`format_description::parse`]: https://time-rs.github.io/api/time/format_description/fn.parse.html
[`format_description::parse_owned`]: https://time-rs.github.io/api/time/format_description/fn.parse_owned.html
[`format_description::parse_borrowed`]: https://time-rs.github.io/api/time/format_description/fn.parse_borrowed.html
[`format_description!`]: https://time-rs.github.io/api/time/macros/macro.format_description.html

#### Configuring [`format_description!`]

For backwards-compatibility reasons, the `format_description!` macro defaults to version 1. If you
want to use a different version, you can do so by setting the `version` parameter to `2`. Note that
this is only necessary if you are relying on a difference in behavior between the versions.

```rust,no_run
use time::macros::format_description;
let _ = format_description!("[hour]:[minute]:[second]"); // Version 1 is implied.
let _ = format_description!(version = 1, "[hour]:[minute]:[second]");
let _ = format_description!(version = 2, "[hour]:[minute]:[second]");
```

Attempting to provide an invalid version will result in a compile-time error.

```rust,compile_fail
use time::macros::format_description;
// 0 is not a valid version, so compilation will fail.
let _ = format_description!(version = 0, "[hour]:[minute]:[second]");
```

### Version 1

![version 1 top-level syntax](../diagrams/abbreviated-v1.svg#rr)

`[[` produces a literal `[`. No other character must be escaped.

### Version 2

![version 2 top-level syntax](../diagrams/abbreviated-v2.svg#rr)

`\` is used to begin an escape sequence. Currently, the only valid escape sequences are `\[`, `\]`,
and `\\`. Any other character following `\` is invalid.

## Components

Follows is the syntax for all components in alphabetical order. Any of the following may be used
where _component_ is present in the above diagram. "Whitespace" refers to any non-empty sequence of
ASCII whitespace characters.

- **Day of month**: `[day]`

  ![syntax for day component](../diagrams/day.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **First item**: `[first]`

  ![syntax for first component](../diagrams/first.svg#rr)

  A series of `FormatItem`s (or `OwnedFormatItem`s) where, when parsing, the first successful parse
  is used. When formatting, the first item is used.

  `format_description` refers to a complete format description that is nested; whitespace (including
  leading and trailing) is significant.

- **Clock hour**: `[hour]`

  ![syntax for hour component](../diagrams/hour.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spacing, or having
  no padding at all. The default is to pad the value with zeroes.

  Users have the option to choose between two representations. One is the 12-hour clock, frequently
  used in the Anglosphere, while the alternative (the 24-hour clock) is frequently used elsewhere.
  The 12-hour clock is typically used in conjunction with AM/PM.

- **Ignore**: `[ignore count:X]`

  ![syntax for ignore component](../diagrams/ignore.svg#rr)

  When parsing, this ignores the indicated number of bytes. This component is a no-op when
  formatting. The `count` modifier is mandatory. Its value must be a positive integer.

- **Minute within the clock hour**: `[minute]`

  ![syntax for minute component](../diagrams/minute.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **Month**: `[month]`

  ![syntax for month component](../diagrams/month.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users have the option to choose between three representations. The default is numerical.
  Alternatives are _long_ and _short_, both of which are textual formats and have no padding. The
  long format is the full English name of the month, while the short format is the first three
  letters of it.

  When parsing, there is the option to consume text-based formats case-insensitively.

- **Whole hours offset from UTC**: `[offset_hour]`

  ![syntax for offset hour component](../diagrams/offset_hour.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users have the option to choose whether the sign is _automatic_ (the default) or _mandatory_.
  If the sign is automatic, it will only be present when the value is negative. If mandatory, it
  will always be present.

- **Minutes within the hour offset from UTC**: `[offset_minute]`

  ![syntax for offset minute component](../diagrams/offset_minute.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  This value is always positive. As such, it has no sign.

- **Seconds within the minute offset from UTC**: `[offset_second]`

  ![syntax for offset second component](../diagrams/offset_second.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  This value is always positive. As such, it has no sign.

- **Optional items**: `[optional]`

  ![syntax for optional component](../diagrams/optional.svg#rr)

  An item that may or may not be present while parsing. While formatting, the value is always
  present.

  `format_description` refers to a complete format description that is nested; whitespace (including
  leading and trailing) is significant.

- **Day of year**: `[ordinal]`

  ![syntax for ordinal component](../diagrams/ordinal.svg#rr)

  The padded value has a width of 3. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **AM/PM**: `[period]`

  ![syntax for period component](../diagrams/period.svg#rr)

  Users have the option to choose whether the value is uppercase or lowercase. This component is
  typically used in conjunction with the hour of the day with `repr:12`.

  When parsing, there is the option to consume text-based formats case-insensitively.

- **Second within the clock minute**: `[second]`

  ![syntax for second component](../diagrams/second.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

- **Subsecond within the clock second**: `[subsecond]`

  ![syntax for subsecond component](../diagrams/subsecond.svg#rr)

  Users have the choice of how many digits should be displayed or parsed. By default, this is
  one or more, where the minimum number of digits will be used when formatting and any nonzero
  number of digits are accepted by the parser (though digits after the ninth will be discarded).
  There is the option to require a fixed number of digits between one and nine. When formatting, the
  value is not rounded if more digits would otherwise be present.

- **Week of the year**: `[week_number]`

  ![syntax for week number component](../diagrams/week_number.svg#rr)

  The padded value has a width of 2. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users can choose between three representations: _iso_ (the default), _sunday_, and _monday_. ISO
  week numbers are in between 1 and 53, while others are between 0 and 53. ISO week one is the
  Monday-to-Sunday week that contains January 4. Week one of other representations begins on the
  first instance of that day in the calendar year (e.g. Sunday-based week numbering has week one
  start on the first Sunday of the year).

- **Day of the week**: `[weekday]`

  ![syntax for weekday component](../diagrams/weekday.svg#rr)

  Users can choose between a number of representations for the day of the week. There are _long_
  (the default) and _short_, both of which are textual representations; the long representation is
  the weekday's full name in English, while the short is the first three letters. There are also
  _sunday_ and _monday_ representations, which are numerical. These formats are either zero to six
  or one to seven (depending on whether `one_indexed` is false or true, respectively), with the
  named day being at the start of that range.

  When parsing, there is the option to consume text-based formats case-insensitively.

- **Year**: `[year]`

  ![syntax for year component](../diagrams/year.svg#rr)

  The padded value has a width of 4. You can choose between padding with zeroes, spaces, or having
  no padding at all. The default is to pad the value with zeroes.

  Users can choose between two representations: the full year (the default) and the last two digits
  of the year. This should be relatively straightforward. Note that when parsing, if only the last
  two digits of the year are present, the value returned may not be what was expected — if the
  return is successful at all (it's not guaranteed).

  There are two bases for the year: _calendar_ and _iso\_week_. The former is what you want if using
  the month, day, ordinal, or similar. You likely only want to use `iso_week` if you are using the
  week number with `repr:iso`. [Don't be like Twitter][twitter-bug]; know which should be used when.

  Users have the option to choose whether the sign is _automatic_ (the default) or _mandatory_.
  If the sign is automatic, it will only be present when the value is negative _or_ if the
  `large-dates` feature is enabled and the value contains more than four digits. If mandatory, it
  will always be present.

  When the `large-dates` feature is enabled, ambiguities may exist when parsing. For example, if a
  year is immediately followed by the week number, the parser will eagerly consume six digits even
  if the year should only be four and the week number the remaining two.

  [twitter-bug]: https://www.theguardian.com/technology/2014/dec/29/twitter-2015-date-bug
