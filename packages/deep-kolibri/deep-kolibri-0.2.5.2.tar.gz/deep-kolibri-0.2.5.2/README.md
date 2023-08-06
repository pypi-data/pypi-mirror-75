# Kolibri

A comprehensive multi modal machine learning platform
# Contents

```
├── README.md
├── config

```

- `README.md`: this documentation

# Setting up PyFreeLing in Mac OS Sierra

There are 4 types of dependencies:

- [Homebrew](https://brew.sh), a package manager to install software in Mac
- [FreeLing](http://nlp.lsi.upc.edu/freeling), an open source language analysis tool suite
- [Python 3](https://www.python.org)
- [lxml](http://lxml.de), a Python library to work with XML
- [libxml2](http://xmlsoft.org) and [libxslt](http://xmlsoft.org/libxslt) C libraries which are dependencies of `lxml`

## Install Homebrew

Follow [Neil Gee's guide](https://coolestguidesontheplanet.com/installing-homebrew-on-macos-sierra-package-manager-for-unix-apps) to install and set up homebrew for Mac OS Sierra

## Install FreeLing

Use Homebrew to install FreeLing by running this command:

```bash
brew install freeling
```

Homebrew will take care of any dependencies.

## Install Python 3

You can install Python 3 with Homebrew following the instructions from [The Hitchhiker's Guide to Python](http://python-guide-pt-br.readthedocs.io/en/latest/starting/install3/osx/) or following the very complete [Lisa Tagliaferri's guide](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos).

Basically:

```bash
brew install python3
```

## Install libxml2 and libxslt

macOS Sierra already provides `libxml2` and `libxslt`. They can be installed through Homebrew though:

```bash
brew install libxml2
brew install libxslt
```

## Install lxml

Now, you are ready to install `lxml`:

```bash
pip3 install lxml
```



Once you have installed FreeLing and all the dependencies, you will always need to start a FreeLing analyzer in server mode


## Starting a FreeLing analyzer in server mode


```bash
analyze -f en.cfg --server --port 50005 &
```


# Install pyaudio

Intalling pyaudiocan be tricky in window platform and generally 'pip install pyaudio' will not work.
see the following stackoverflow response if you have any problem.

https://stackoverflow.com/questions/52283840/i-cant-install-pyaudio-on-windows-how-to-solve-error-microsoft-visual-c-14


# install pocketsphinx

Instaaling this library could be difficult on some systems.
If the command:
```bash
pip install pocketsphinx 
```
did not work for you then try the following steps
```bash
git clone --recursive https://github.com/bambocher/pocketsphinx-python
cd pocketsphinx-python
```

Edit file pocketsphinx-python/deps/sphinxbase/src/libsphinxad/ad_openal.c.

Change
```
#include <al.h>
#include <alc.h>
```

to
```
#include <OpenAL/al.h>
#include <OpenAL/alc.h>
```
and finally:
```bash
python setup.py install
```