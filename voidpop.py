#!/usr/bin/env python3
"""Dummy POP3 server that accepts any login and never has any messages"""
from __future__ import annotations

import argparse
import enum
import logging
import signal
import socket
import time
from functools import partial
from itertools import count
from typing import List, Optional

import trio

connection_ids = count()
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--port", type=int, default=110, help="Listen on PORT")
    parser.add_argument("--verbose", action="store_true", help="Log debug messages")
    return parser.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format=f"%(asctime)s.%(msecs)03d %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )
    try:
        trio.run(trio.serve_tcp, handler, args.port)
    except KeyboardInterrupt:
        return


def ok(msg: Optional[str] = None) -> bytes:
    if msg is None:
        return b"+OK\r\n"
    return b"+OK %b\r\n" % msg.encode("ascii", errors="replace")


def err(msg: Optional[str] = None) -> bytes:
    if msg is None:
        return b"-ERR\r\n"
    return b"-ERR %b\r\n" % msg.encode("ascii", errors="replace")


class State(enum.Enum):
    authorization = enum.auto()
    transaction = enum.auto()
    update = enum.auto()
    done = enum.auto()


class POP3:
    def __init__(self) -> None:
        self.state = State.authorization

    def banner(self) -> bytes:
        return ok(f"<{time.monotonic()}@{socket.gethostname()}>")

    def handle(self, command: str, args: List[str]) -> bytes:
        if self.state == State.authorization:
            if command == "USER":
                return ok("pretending your mailbox exists")
            if command == "PASS":
                self.state = State.transaction
                return ok("how did you know")
            if command == "QUIT":
                self.state = State.done
                return ok("goodbye")
            if command == "APOP":
                self.state = State.transaction
                return ok("pretending your mailbox exists")

        if self.state == State.transaction:
            if command == "STAT":
                return ok("0 0")
            if command == "LIST":
                return err("no such message") if args else ok("\r\n.")
            if command == "RETR":
                return err("no such message")
            if command == "DELE":
                return err("no such message")
            if command == "NOOP":
                return ok()
            if command == "RSET":
                return ok()
            if command == "QUIT":
                self.state = State.update
                return ok("goodbye")
            if command == "TOP":
                return err("no such message")
            if command == "UIDL":
                return err("no such message") if args else ok("\r\n.")

        return err("unrecognized command")


async def handler(stream: trio.SocketStream) -> None:
    id = next(connection_ids)
    pop3 = POP3()
    logger.debug("[%s] Connection opened", id)
    try:
        await stream.send_all(pop3.banner())
        async for data in stream:
            command, *args = (
                data.decode("ascii", errors="replace").rstrip("\r\n").split(" ")
            )
            command = command.upper()
            response = pop3.handle(command, args)
            await stream.send_all(response)
            logger.debug("[%s] - %r", id, data)
            logger.debug("[%s]   -> %r", id, response)
            if pop3.state in {State.update, State.done}:
                break
    except Exception:
        logger.warning("[%s] Crashed", id, exc_info=True)
    logger.debug("[%s] Connection closed", id)
