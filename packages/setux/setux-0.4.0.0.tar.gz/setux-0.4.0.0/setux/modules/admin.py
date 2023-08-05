from . import Module


class Distro(Module):
    def deploy(self, target, **kw):

        usr = kw['usr']
        pub = kw['pub']

        if not target.User(usr).deploy():
            return False

        if not target.deploy('.sudoers', user=usr):
            return False

        if not target.deploy('.copy_id', **kw):
            return False


        return True
