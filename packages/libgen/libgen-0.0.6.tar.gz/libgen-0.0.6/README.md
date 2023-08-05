# libgen :- A command line tool for downloading files from library genesis
<p align="center">
  <img src="https://github.com/amalshaji/libgen-cli/workflows/Upload%20Python%20Package/badge.svg">
  <img src="https://img.shields.io/pypi/v/libgen">
  <img src="https://img.shields.io/librariesio/github/amalshaji/libgen-cli">
</p>
1. Install

```bash
pip install libgen --upgrade
```

2. Usage

Search for books using title

```bash
libgen search "Machine Learning"
```
Result
```bash
{'author': 'Christopher M. Bishop',
  'format': 'pdf',
  'id': '640',
  'lang': 'English',
  'link': 'http://93.174.95.29/main/6B552B24CAE380BB656F7AAEF7F81B46',
  'name': 'Information science and statisticsPattern Recognition and Machine '
          'Learning [1st ed. 2006. Corr. 2nd printing] 9780387310732, '
          '0387310738',
  'publisher': 'Springer',
  'size': '5 Mb',
  'year': '2006'}
  .....
```

Download files using "link" obtained from search

```bash
libgen download --url http://93.174.95.29/main/6B552B24CAE380BB656F7AAEF7F81B46 --output file.pdf
# or download using id
# libgen download --id 640
```
Result
```bash
Downloading: file.pdf:  21%|████▌            956k/4.52M [00:10<00:32, 116kB/s]
```

You can specify the output file name using `--output`
