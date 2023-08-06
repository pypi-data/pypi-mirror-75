from netnir.helpers.colors import TextColor
from getpass import getpass
import keyring
import logging
import os


"""credentials create/fetch/delete class
"""


class Credentials:
    """
    a class to do credentials administration.

    :params username: type str (required)
    :params password: type str (optional)
    :params confirm_password: type str (optional)
    :params service_name: type str (required)

    .. code:: python

       from netnir.core import Credentials

       creds = Credentials(service_name="testService", username="testUser")
       ## fetch or create credentials
       creds.fetch()
       ## delete credentials from the keyring
       creds.delete()
    """

    def __init__(
        self,
        username: str = None,
        password: str = None,
        confirm_password: str = None,
        service_name: str = None,
    ):
        """
        initialize the credentials class
        """
        from netnir.constants import SERVICE_NAME, NETNIR_USER, NETNIR_PASS

        self.username = NETNIR_USER or username
        self.password = NETNIR_PASS or password
        self.confirm_password = NETNIR_PASS or confirm_password
        self.service_name = SERVICE_NAME or service_name
        self.message = "netnir network authentication"
        self.status = None
        self.username_file = os.path.expanduser("~/.netniruser")

        if self.username is None:
            self._username()

    def create(self):
        """
        create or update credentials

        :returns: dict
        """
        if self.password is None:
            self.password = getpass(f"{self.message} password: ")
            self.confirm_password = getpass(f"{self.message} confirm passowrd: ")

        if self.password == self.confirm_password:
            keyring.set_password(
                service_name=self.service_name,
                username=self.username,
                password=self.password,
            )

        self.status = "created"
        self.password = self._fetch()

        return self._schema()

    def fetch(self):
        """
        fetch or create credentials

        :returns: dict
        """

        if self._fetch() is None:
            self.create()
        else:
            self.status = "fetched"
            self.password = self._fetch()

        return self._schema()

    def delete(self):
        """
        delete credentials

        :returns: dict
        """
        if self.confirm_password is None:
            self.confirm_password = getpass(f"{self.message} password: ")

        creds = self.fetch()
        self.password = creds["password"]

        if self.password == self.confirm_password:
            keyring.delete_password(
                service_name=self.service_name, username=self.username
            )

            self.status = "deleted"

            if os.path.isfile(self.username_file):
                os.remove(self.username_file)
                message = TextColor.green(
                    f"username file {self.username_file} has been deleted"
                )
                logging.warning(message)

            return self._schema()

        return creds

    def _username(self):
        """internal method to read or create the username file

        :returns: username string
        """
        if os.path.isfile(self.username_file):
            with open(self.username_file, "r") as user:
                self.username = user.read()
                message = TextColor.green(f"username read from {self.username_file}")
                logging.info(message)
        else:
            self.username = input("netnir username: ")

            with open(self.username_file, "w") as user:
                user.write(self.username)
                message = TextColor.green(f"username written to {self.username_file}")
                logging.info(message)

        return self.username

    def _fetch(self):
        """
        private function to fetch credentials

        :returns: keyring object
        """
        return keyring.get_password(
            service_name=self.service_name, username=self.username
        )

    def _schema(self):
        """
        private function defining the returned output schema

        :returns: dict
        """
        return {
            "service": self.service_name,
            "username": self.username,
            "password": self.password,
            "status": self.status,
        }
