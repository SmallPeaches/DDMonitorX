from importlib import import_module

class GetStreamerInfo():
    def __init__(self,platform,rid) -> None:
        self.platform = platform
        self.rid = rid
        
        if __package__:
            self.metaclass = getattr(import_module(f'{__package__}.{self.platform}'),self.platform)
        else:
            self.metaclass = getattr(import_module(f'{self.platform}'),self.platform)
        self.api_class = self.metaclass(rid=self.rid)

    def __getattribute__(self, __name: str):
        try:
            return object.__getattribute__(self,__name)
        except AttributeError:
            return self.api_class.__getattribute__(__name)

if __name__ == '__main__':
    api = GetStreamerInfo('douyu','6746940')
    api.get_info()
    print(api.is_available())