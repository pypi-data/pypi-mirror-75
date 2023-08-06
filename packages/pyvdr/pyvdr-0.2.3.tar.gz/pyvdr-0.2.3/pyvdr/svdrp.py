#!/usr/bin/env python3

import re
import socket
import logging
from collections import namedtuple

response_data = namedtuple('ResponseData', 'Code Separator Value')
SVDRP_EMPTY_RESPONSE = ""

_LOGGER = logging.getLogger(__name__)


class SVDRP(object):
    SVDRP_STATUS_OK = '250'

    def __init__(self, hostname='localhost', port=6419, timeout=10):
        self.hostname = hostname
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.socket_file = None
        self.responses = []

    def connect(self):
        if self.socket is None:
            try:
                _LOGGER.debug("Setting up connection to {}".format(self.hostname))
                self.socket = socket.create_connection((self.hostname, self.port), timeout=self.timeout)
                self.socket_file = self.socket.makefile('r')
            except socket.error as se:
                _LOGGER.info('Unable to connect. Not powered on? {}'.format(se))

    def is_connected(self):
        return self.socket is not None

    def disconnect(self):
        _LOGGER.debug("Closing communication with server.")
        if self.socket is not None:
            self.send_cmd("quit")
            self.socket_file.close()
            self.socket.close()

        self.responses = []
        self.socket = None

    def send_cmd(self, cmd):
        _LOGGER.debug("Send cmd: {}".format(cmd))
        if not self.is_connected():
            return

        cmd += '\r\n'

        if isinstance(cmd, str):
            cmd = cmd.encode("utf-8")

        try:
            self.socket.sendall(cmd)
        except IOError as e:
            _LOGGER.debug("IOError e {}, closing connection".format(e))
            self.socket.close()

    def _parse_response(self, resp):
        # <Reply code:3><-|Space><Text><Newline>
        matchobj = re.match(r'^(\d{3})(.)(.*)', resp, re.M | re.I)

        return response_data(Code=matchobj.group(1), Separator=matchobj.group(2), Value=matchobj.group(3))

    """
    Gets the response from the last CMD and puts it in the internal list.
    :return Namedtuple (Code, Separator, Value)
    """
    def _read_response(self):
        for line in self.socket_file:
            response_entry = self._parse_response(line)
            self.responses.append(response_entry)

            # The first and last row are separated simply by ' ', other with '-'.
            # End once found a ' ' separator
            if response_entry.Separator != '-' and len(self.responses) > 1:
                break

    """
    Gets the response of the latest CMD as plaintext
    :return response as plain text
    """
    def get_response_as_text(self):
        self._read_response()
        return "".join(str(self.responses))

    """
    Gets the response of the latest CMD as data structure
    By default returns a list, if single line set to true it will just return the
    1st state line.
    :return List of Namedtuple (Code, Separator, Value)
    """
    def get_response(self, single_line=False):
        if not self.is_connected():
            return SVDRP_EMPTY_RESPONSE

        self._read_response()
        if single_line:
            _LOGGER.debug("Returning single item")
            return self.responses[2]
        else:
            _LOGGER.debug("Returning {} items".format(len(self.responses)))
            return self.responses

    def shutdown(self):
        if self.socket is not None:
            self.send_cmd("quit")
            self.socket_file.close()
            self.socket.close()
            self.responses = None
