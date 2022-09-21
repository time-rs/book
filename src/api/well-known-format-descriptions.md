# Well known format descriptions

The following format descriptions are approximations of their respective standards. They are unable to
fully model all the parsing and formatting edgecases that you might encounter in the real world. The
format descriptions provided here are intended to help you understand how to write your own 
if you need your own custom format. If you specifically need one of these standards, you
should use the provided structs within the `time` crate itself found in the
[`time::format_description::well_known`](https://docs.rs/time/latest/time/format_description/well_known/index.html) module instead of writing your own format description for them, as those structs have been
designed to handle those edgecases correctly.

All the samples will use the following datetimes
- `1997-11-12 09:55:06 -06:00`
- `2022-09-08 13:55:24 +02:00`
- `2010-03-14 18:32:03 +00:00`

## ISO 8601

The format described in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html). It can be
found in the [api documentation here](https://docs.rs/time/latest/time/format_description/well_known/struct.Iso8601.html).

The samples and format description shown below are using the default configuration of ISO 8601, but
the `time` crate does provide various configuration options for this standard which you can change
if you require, such as the time precision, date format (year-month-day, year-week-weekday, year-ordinal), removing separators, and more. Additional information can be found in the 
[configuration api documentation](https://docs.rs/time/latest/time/format_description/well_known/iso8601/struct.Config.html).

Samples
- `1997-11-12T09:55:06.000000000-06:00`
- `2022-09-08T13:55:24.000000000+02:00`
- `2010-03-14T18:32:03.000000000Z`

Approximate Format Description:
`[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9][offset_hour sign:mandatory]:[offset_minute]`

Approximate Format Description when timezone == 0: `[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9]Z`


## RFC 2822

The format described in [RFC 2822](https://www.rfc-editor.org/rfc/rfc2822#section-3.3). It can be
found in the [api documentation here](https://docs.rs/time/latest/time/format_description/well_known/struct.Rfc2822.html).

Samples
- `Wed, 12 Nov 1997 09:55:06 -0600`
- `Thu, 08 Sep 2022 13:55:24 +0200`
- `Sun, 14 Mar 2010 18:32:03 +0000`

Approximate Format Description: `[weekday repr:short], [day] [month repr:short] [year] [hour]:[minute]:[second] [offset_hour][offset_minute]`

## RFC 3339

The format described in [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339#section-5.6). It can be
found in the [api documentation here](https://docs.rs/time/latest/time/format_description/well_known/struct.Rfc3339.html).

Samples
- `1997-11-12T09:55:06-06:00`
- `2022-09-08T13:55:24+02:00`
- `2010-03-14T18:32:03Z`


Approximate Format Description: `[year]-[month]-[day]T[hour]:[minute]:[second][offset_hour sign:mandatory]:[offset_minute]`

Approximate Format Description when timezone == 0: `[year]-[month]-[day]T[hour]:[minute]:[second]Z`