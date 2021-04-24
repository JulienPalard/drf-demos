# Uptime monitor

Monitor a server:

```
POST /uptime -d '{"domain": "mdk.fr"}'
201 Created
Location: /uptime/mdk.fr
```

See all monitored machines:

```
GET /uptime
{"checks": [
  {
    "is_up": True,
    "domain": "mdk.fr",
    "up_since": "2021-01-01T00:00:00Z",
    "checks": "/uptime/mdk.fr/checks",
  },
  {
    "is_up": True,
    "domain": "afpy.org",
    "up_since": "2021-01-01T00:00:00Z",
    "checks": "/uptime/afpy.org/checks",
  },
...
```

Get a check:

```
GET /uptime/mdk.fr
{
  "is_up": True,
  "domain": "mdk.fr",
  "up_since": "2021-01-01T00:00:00Z",
  "checks": "/uptime/mdk.fr/checks",
}
```

See check history

```
GET /uptime/mdk.fr/checks
{
  "checks": [
      {"date": "2021-04-05T00:01:02Z", "is_up": True},
      {"date": "2021-04-05T00:02:02Z", "is_up": True},
      {"date": "2021-04-05T00:03:02Z", "is_up": True},
      {"date": "2021-04-05T00:04:02Z", "is_up": True}
  ]
}
```
