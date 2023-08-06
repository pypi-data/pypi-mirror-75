import json
import winreg

from ..template import MemoryTemplate
from ..exceptions import NotFoundError


class RegistryTemplate(MemoryTemplate):
    root = winreg.HKEY_CURRENT_USER

    def __init__(self, name='xmem'):
        """
        :param name: name of your application, will be created in registry
        """
        super(RegistryTemplate, self).__init__()

        # check if os is supported [Windows]
        import platform
        if platform.system() != 'Windows':
            raise OSError('Unsupported operating system, this template only works on windows')

        self.registry_path = f'SOFTWARE\\{name}\\Settings'

    def save(self, data: dict):
        data_string = json.dumps(data)
        try:
            winreg.CreateKey(self.root, self.registry_path)

            with winreg.OpenKey(self.root, self.registry_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, str(self.path), 0, winreg.REG_SZ, data_string)

            return True
        except WindowsError:
            return False

    def load(self) -> dict:
        try:
            with winreg.OpenKey(self.root, self.registry_path, 0, winreg.KEY_READ) as key:
                data_string, type = winreg.QueryValueEx(key, str(self.path))

            return json.loads(data_string)
        except WindowsError:
            path = self.registry_path + f"\\{self.path}"

            raise NotFoundError(f'registry path, {path} does not exist')
