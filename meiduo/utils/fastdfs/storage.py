from django.core.files.storage import Storage

class MyStorage(Storage):


    def _open(self, name, mode='rb'):
        """Retrieve the specified file from storage."""
        pass

    def _save(self, name, content, max_length=None):
        pass
    # @property
    def url(self, name):

        return "http://192.168.13.178:8888/" + name
