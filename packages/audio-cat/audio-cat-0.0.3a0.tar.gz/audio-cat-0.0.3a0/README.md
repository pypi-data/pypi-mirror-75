
# audio-cat
[![Documentation Status](https://readthedocs.org/projects/audio-cat/badge/?version=latest)](https://audio-cat.readthedocs.io/en/latest/?badge=latest)

high-level api to split and categorize audio samples, intended for data collection

Installation
------------
```
pip install audio-cat
```
or
```
git clone https://github.com/nathanielCherian/audio-cat.git
pip install -e audio-cat
```
audio-cat implements ffmpeg to proccess download it [here](https://www.ffmpeg.org/download.html) and add it to your path (from enviornment variables)

CLI Usage
---------
audio-cat can be used by command line for quick and easy sound wrangling

```
$ audio-cat [command] --optionals
```

**Download** and chop sound from a youtube video
```
$ audio-cat download [URL] [TITLE]

URL       video url
TITLE     name to save audio

--des     destination default=audio
--split   split interval default=2500 (set -1 for download only)
--blurb   full audio storage default=FULL_AUDIO
--dataset create dataset for samples
```

**Create Dataset** from chopped samples
```
$ audio-cat dataset [PATH] [TITLE]

PATH      path to directory containing segments
TITLE     desired title of dataset

--des     destination default=datasets
```



