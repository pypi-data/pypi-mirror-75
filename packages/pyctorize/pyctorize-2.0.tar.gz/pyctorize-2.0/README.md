# Pyctorize

A Python command line program to extract frames of videos

### Prerequisites

[Python 3](https://www.python.org/downloads/release/python-373/)

### Installing

```
python3 -m pip install pyctorize
```

## Using

```console
$ pyctorize <PATH_TO_FILE> \
    --output <PATH_TO_OUTPUT_DIRECTORY> \
    --start-time <TIME_IN_MILLISECONDS_OF_FIRST_FRAME> \
    --step <CAPTURE_IMAGE_EVERY_STEP_MILLISECONDS>
```

Example:
```console
$ pyctorize example.mp4 \
    --output output/ \ # save result to output/
    --start-time 100 \ # starting at 100ms
    --step 1000 # take a frame every second
```

In this example, pyctorize will produce a frame for 1100ms, 2100ms, 3100ms and so on.


## Built With

* [Moviepy](https://github.com/Zulko/moviepy)

## Authors

* **Víctor Colombo** - [vccolombo](https://github.com/vccolombo)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
