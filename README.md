# Shark'Guestbook

*say something.*

Demo: http://guestbook.iconb.cn

![Screenshot](https://www.iconb.cn/image/guestbook.png)

## Installation

clone:
```
$ git clone https://github.com/sharkcheung/guestbook.git
$ cd guestbook
```
create & activate virtual env then install dependency:

with venv/virtualenv + pip:
```
$ python -m venv env  # use `virtualenv env` for Python2, use `python3 ...` for Python3 on Linux & macOS
$ source env/bin/activate  # use `env\Scripts\activate` on Windows
$ pip install -r requirements.txt
```
or with Pipenv:
```
$ pipenv install --dev
$ pipenv shell
```
generate fake data then run:
```
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/
```

install font：

Make directory chinese
Upload font file to chinese directory
```
$ chmod u+rwx /usr/share/fonts/chinese/*
$ fc-cache –fv
```

## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
