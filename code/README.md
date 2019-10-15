
## Troubleshooting 

### OSX (MAC)

#### PyAudio

If an error similar to `portaudio.h file not found` appears, then follow these steps:

First, install portaudio if you haven't already.

```sh
brew install portaudio
```

Then, inside the virtual environment do the following:

```sh
pip install --global-option='build_ext' --global-option='-I/usr/local/include' --global-option='-L/usr/local/lib' pyaudio
```

#### PocketSphinx 

Having started the virtual environment, go to the `build/` folder or any of your choice and follow these steps.

```sh
git clone --recursive https://github.com/bambocher/pocketsphinx-python
cd pocketsphinx-python
```

Edit `pocketsphinx-python/deps/sphinxbase/src/libsphinxad/ad_openal.c`
And change
```cpp
#include <al.h>
#include <alc.h>
```

to

```cpp
#include <OpenAL/al.h>
#include <OpenAL/alc.h>
```

Ultimately, run `python setup.py install`.


