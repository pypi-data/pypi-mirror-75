from . import Module


def ping(target, pong='pong'):
    ret, out, err = target.run('echo', pong)
    response = out[0]
    return response==pong


class debian_9(Module):
    def deploy(self, target, **kw):
        return ping(target, 'Debian 9')


class debian_10(Module):
    def deploy(self, target, **kw):
        return ping(target, 'Debian 10')


class MX_19(Module):
    def deploy(self, target, **kw):
        return ping(target, 'MX 19')


class fedora_32(Module):
    def deploy(self, target, **kw):
        return ping(target, 'Fedora 32')


class manjaro(Module):
    def deploy(self, target, **kw):
        return ping(target, 'Manjaro')

