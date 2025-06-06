# Voidpop

**Voidpop** is a dummy POP3 server. It accepts any username/password and always
reports that there are no messages.

## Why??

I found myself in a situation where I needed someone to send some emails via a
particular SMTP account, but there was no corresponding incoming mail account.
Their email client refused to even try to connect to the SMTP server if it
couldn't first sync the mailbox from an incoming mail server. I didn't find any
existing dummy POP3 or IMAP services, and POP3 looked simpler to implement.

## Using pop.voidpop.org

You can connect to `pop.voidpop.org` on port 110 with any username and password,
and the server will report that you have 0 messages.

## Running your own instance

Install <a href=https://docs.astral.sh/uv/ rel=external target=_blank>uv</a>, then use:

```bash
$ uvx voidpop
```
