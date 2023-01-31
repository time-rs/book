# Well-known format descriptions

A number of well-known format descriptions are provided by `time`. These are intended to be used
when you need to be fully compliant with a specification. Many specifications have various
edge-cases that are difficult to model with a custom format description. Using a well-known format
description allows you to handle all relevant edge cases.

## Guarantees

The guarantees provided by well-known formats are deliberately minimal. The only guarantees, unless
otherwise documented, are:

- When formatting, the output will be valid according to the specification.
- Parsing will succeed if and only if the input is valid according to the specification.

If you are expecting a specific output and not just any valid output, you should use a custom
format.

## ISO 8601

The format described in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html). It can
be found in the
[api documentation here](https://docs.rs/time/latest/time/format_description/well_known/struct.Iso8601.html).

The examples and format description shown below are for the default configuration. Various options
are available for this format which you can change. Additional information can be found in the
[configuration api documentation](https://docs.rs/time/latest/time/format_description/well_known/iso8601/struct.Config.html).

**Note**: When using the `time::serde::iso8601` module in conjunction with `serde`, the default
configuration is different. In that case, the years are always six digits and preceded by a sign.

Examples:

- `1997-11-12T09:55:06.000000000-06:00`
- `2022-09-08T13:55:24.000000000+02:00`
- `2010-03-14T18:32:03.000000000Z`

Approximate format description:\
`[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9][offset_hour]:[offset_minute]`

Approximate format description when the time zone is UTC:\
`[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9]Z`

## RFC 2822

The format described in [RFC 2822](https://www.rfc-editor.org/rfc/rfc2822#section-3.3). It can be
found in the [api documentation here](https://docs.rs/time/latest/time/format_description/well_known/struct.Rfc2822.html).

Examples:

- `Wed, 12 Nov 1997 09:55:06 -0600`
- `Thu, 08 Sep 2022 13:55:24 +0200`
- `Sun, 14 Mar 2010 18:32:03 +0000`

Approximate format description:\
`[weekday repr:short], [day] [month repr:short] [year] [hour]:[minute]:[second] [offset_hour][offset_minute]`

## RFC 3339

The format described in [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339#section-5.6). It can be
found in the [api documentation here](https://docs.rs/time/latest/time/format_description/well_known/struct.Rfc3339.html).

Examples:

- `1997-11-12T09:55:06-06:00`
- `2022-09-08T13:55:24+02:00`
- `2010-03-14T18:32:03Z`

Approximate format description:\
`[year]-[month]-[day]T[hour]:[minute]:[second][offset_hour]:[offset_minute]`

Approximate format description when the time zone is UTC:\
`[year]-[month]-[day]T[hour]:[minute]:[second]Z`
