from nornir.plugins.tasks.text import template_file


"""compile template class
"""


class CompileTemplate:
    """compile jinja2 template utilizing the nornir template_file plugin

    :param nr: type obj
    :param host: type str
    :param template: type str

    :return: compled template result
    """

    def __init__(self, nr: object, host: str = None, template: str = None):
        """initialize the compiletemplate class
        """
        self.nr = nr
        self.host = self.nr.filter(name=host)
        self.file = template
        self.path = self.host.inventory.hosts[host].data["template_path"]
        self.render()

    def render(self):
        """execute the class and return the results

        return: nornir results
        """
        result = self.host.run(task=template_file, template=self.file, path=self.path)

        return result
