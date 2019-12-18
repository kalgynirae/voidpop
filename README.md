# voidpop

Voidpop is a dummy POP3 server. It accepts any username/password and always
reports that there are no messages.

## Using pop.voidpop.org

You can connect to `pop.voidpop.org` on port 110 with any username and password,
and the server will report that you have 0 messages.

## Running your own instance

```bash
$ python3 -m venv env
$ env/bin/pip install voidpop
$ env/bin/voidpop --help
```
