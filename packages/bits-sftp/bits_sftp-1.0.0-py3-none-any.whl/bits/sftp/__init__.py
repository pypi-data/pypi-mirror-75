# -*- coding: utf-8 -*-
"""SFTP class file."""

import logging

from io import BytesIO, StringIO

import paramiko


class SFTP(object):
    """SFTP class."""

    def __init__(
            self,
            host,
            username,
            key=None,
            passphrase=None,
            password=None,
            path="/",
            port=22,
    ):
        """Initialize a class instance."""
        self.host = host
        self.port = port
        self.path = path
        self.username = username

        # get SFTP secrets from secret manager
        self.key = key
        self.passphrase = passphrase
        self.password = password

        # create a transport object for the SFTP host
        self.transport = paramiko.Transport((self.host, self.port))

        # create an SFTP client
        self.sftp = self.create_sftp_client()

    def close(self):
        """Close connections."""
        try:
            self.sftp.close()
            self.transport.close()
        # pylint: disable=broad-except
        except Exception as exception:
            error = f"Failed to close SFTP connection to host: {self.host} [{exception}]"
            logging.error(error)

    def create_sftp_client(self):
        """Return a paramiko transport based on the host."""
        # connect to transport with a password
        if self.password:
            self.transport.connect(username=self.username, password=self.password)

        # connect to transport with a key (and passphrase, if exists)
        else:
            # create private key
            private_key = StringIO(self.key)
            pkey = paramiko.RSAKey.from_private_key(private_key, password=self.passphrase)

            # connect to transport based on private key
            self.transport.connect(username=self.username, pkey=pkey)

        # create and return a parimiko SFTP client from the transport we created
        return paramiko.SFTPClient.from_transport(self.transport)

    def get_file_object(self, name):
        """Retrieve a file from SFTP as a file object."""
        # create a in-memory file object so we don't write to disk
        file_object = BytesIO()

        # get sftp remove path
        remote_path = f"{self.path}/{name}"

        # get the file from the SFTP server at the remot epath
        try:
            self.sftp.getfo(remote_path, file_object)
            file_object.seek(0)
        except Exception as sftp_error:
            # close file object and raise the error
            file_object.close()
            raise sftp_error

        return file_object

    def list_files(self):
        """List files at sftp config host/path."""
        return self.sftp.listdir(self.path)

    def put_file_object(self, file_object, name):
        """Send a file to SFTP from GCS."""
        # get sftp remove path
        remote_path = f"{self.path}/{name}"

        # put the file onto the SFTP server at the remote path
        try:
            self.sftp.putfo(file_object, remote_path)
        except Exception as sftp_error:
            # close file object and raise the error
            file_object.close()
            raise sftp_error

        # cloud file object
        file_object.close()
