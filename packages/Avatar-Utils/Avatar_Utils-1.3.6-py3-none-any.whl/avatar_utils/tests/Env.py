class Env:
    protocol: str
    host: str
    port: int = 8000

    @property
    def base_url(self):
        return f'{self.protocol}{self.host}:{self.port}'


class DevEnv(Env):
    protocol = 'http://'
    host = 'dev0.avatar.vm.onti.actcognitive.org'


class TestEnv(Env):
    protocol = 'https://'
    host = 'avatar.dev-ops.zone/api/'


class ProdEnv(Env):
    protocol = 'https://'
    host = 'unknown'
