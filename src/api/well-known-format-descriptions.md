# Well known format descriptions

All the following samples will use the following datetimes
- `1997-11-12 09:55:06 -06:00`
- `2022-09-08 13:55:24 +02:00`
- `2010-03-14 18:32:03 +00:00`

## ISO 8601

The format described in [ISO 8601](https://www.iso.org/iso-8601-date-and-time-format.html)

Samples
- `1997-11-12T09:55:06.000000000-06:00`
- `2022-09-08T13:55:24.000000000+02:00`
- `2010-03-14T18:32:03.000000000Z`

Format String:
`[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9][offset_hour sign:mandatory]:[offset_minute]`

Format String when timezone == 0: `[year]-[month]-[day]T[hour]:[minute]:[second].[subsecond digits:9]Z`


## RFC 2822

The format described in [RFC 2822](https://www.rfc-editor.org/rfc/rfc2822#section-3.3)

Samples
- `Wed, 12 Nov 1997 09:55:06 -0600`
- `Thu, 08 Sep 2022 13:55:24 +0200`
- `Sun, 14 Mar 2010 18:32:03 +0000`

Format String: `[weekday repr:short], [day] [month repr:short] [year] [hour]:[minute]:[second] [offset_hour][offset_minute]`

## RFC 3339

The format described in [RFC 3339](https://www.rfc-editor.org/rfc/rfc3339#section-5.6)

Samples
- `1997-11-12T09:55:06-06:00`
- `2022-09-08T13:55:24+02:00`
- `2010-03-14T18:32:03Z`


Format String: `[year]-[month]-[day]T[hour]:[minute]:[second][offset_hour sign:mandatory]:[offset_minute]`

Format String when timezone == 0: `[year]-[month]-[day]T[hour]:[minute]:[second]Z`