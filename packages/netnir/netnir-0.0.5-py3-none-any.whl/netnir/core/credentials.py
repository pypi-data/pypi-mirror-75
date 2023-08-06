import keyring
from getpass import getpass
from netnir.constants import SERVICE_NAME


"""credentials create/fetch/delete class
"""


class Credentials:
    """
    a class to do credentials administration.

    :param username: type str (required)
    :param password: type str (optional)
    :param confirm_password: type str (optional)
    :param service_name: type str (required)

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
        service_name: str = SERVICE_NAME,
    ):
        """
        initialize the credentials class
        """
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.service_name = service_name
        self.message = "netnir network authentication"
        self.status = None

    def create(self):
        """
        create credentials
        :return: dict
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

        :return: dict
        """
        self.password = self._fetch()

        if self.password is None:
            self.create()
        else:
            self.status = "fetched"

        self.password = self._fetch()

        return self._schema()

    def delete(self):
        """
        delete credentials

        :return: dict
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

            return self._schema()

        return creds

    def _fetch(self):
        """
        private function to fetch credentials

        :return: keyring object
        """
        return keyring.get_password(
            service_name=self.service_name, username=self.username
        )

    def _schema(self):
        """
        private function defining the returned output schema

        :return: dict
        """
        return {
            "username": self.username,
            "password": self.password,
            "status": self.status,
        }
