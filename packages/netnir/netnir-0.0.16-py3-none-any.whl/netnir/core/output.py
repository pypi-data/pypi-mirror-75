from netnir.constants import OUTPUT_DIR
import os


"""ouput read/write/delete class
"""


class Output:
    """
    a class for writing, reading, and deleting output data to/from a file

    :param host: type str
    :param output_file: type str

    .. code:: python

       from netnir.core import Output

       o = Output(host='router.dc1', output_file='data.conf')
       ## write data to file
       o.write(output_data="some data")
       ## read data from file
       o.read()
       ## delete file
       o.delete()
    """

    def __init__(self, host: str = None, output_file: str = None):
        """
        initialize the output class
        """
        self.hostname = host
        self.output_dir = os.path.expanduser("/".join([OUTPUT_DIR, self.hostname]))
        self.output_file = os.path.expanduser("/".join([self.output_dir, output_file]))

        if not os.path.isdir(os.path.expanduser(OUTPUT_DIR)):
            os.mkdir(os.path.expanduser(OUTPUT_DIR))

        if not os.path.isdir(self.output_dir):
            os.mkdir(self.output_dir)

    def write(self, output_data):
        """
        write data to file

        :param output_data: type str
        :return: str
        """
        with open(self.output_file, "w") as f:
            f.write(output_data)

        return f"contents written to {self.output_file}"

    def read(self):
        """
        read data from file

        :return: read data
        """
        with open(self.output_file) as f:
            data = f.read()

        return data

    def delete(self):
        """
        delete file

        :return: str
        """
        if os.path.isfile(self.output_file):
            os.remove(self.output_file)

        return f"{self.output_file} has been deleted"
