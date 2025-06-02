#### 1. Install python package
```
# install from pypi
pip install -U cadences

# or from github very latest
pip install -U git+https://github.com/quadrismegistus/cadence
```

#### 2. Run setup file from github repo 
* Run on the terminal:
        ```python setup.py install```

#### 3. Install espeak (TTS)

Install espeak, free TTS software, to 'sound out' unknown words. See [here](http://espeak.sourceforge.net/download.html) for all downloads.

* On Linux, type into the terminal:
        ```apt-get install espeak```
    
* On Mac:
  * Install [homebrew](brew.sh) if not already installed.

  * Type into the Terminal app: `brew install espeak`
    
* On Windows:
        Download and install from http://espeak.sourceforge.net/download.html

#### 4. NLTK data
* First time calling the function `extract_title_cadence`, you need to run `nltk.download()`
