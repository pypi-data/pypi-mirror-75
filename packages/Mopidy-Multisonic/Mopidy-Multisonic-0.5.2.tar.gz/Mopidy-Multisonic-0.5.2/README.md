Mopidy Multisonic
=================

Yes, another mopidy subsonic backend provider. This module allow multiple
subsonic server providers

## Installation

Install by running:

```
python3 -m pip install Mopidy-Multisonic
```

## Configuration

Before starting Mopidy, you must add configuration for
Mopidy-Multisonic to your Mopidy configuration file:

```
[multisonic]
providers =
  PROVIDER_NAME: PROTOCOL://USERNAME:PASSWORD@TARGET?[option1=value1&option2=value2]
  [ANOTHER]
```

```
[multisonic]
providers =
  banalisation: https://mr_banal:azerty@music.banalserver.com?max_bit_rate=320&format=mp3
```

```
[multisonic]
providers =
  banalisation: https://mr_banal:azerty@music.banalserver.com?max_bit_rate=320
  decadence: http://h4ck3r:1213@toot.com
```


Project resources
=================

- [Project hub](https://sr.ht/~reedwade/mopidy-multisonic/)
- [Todo tracker](https://todo.sr.ht/~reedwade/Mopidy-Multisonic)
- [Mailing list](https://sr.ht/~reedwade/mopidy-multisonic/lists)
- [Changelog](https://hg.sr.ht/~reedwade/mopidy_multisonic/browse/default/CHANGELOG.md)


Credits
=======

- Original author: [ReedWade](https://sr.ht/~reedwade)
- Current maintainer: [ReedWade](https://sr.ht/~reedwade)
- [Contributors](https://hg.sr.ht/~reedwade/mopidy_multisonic/contributors)
