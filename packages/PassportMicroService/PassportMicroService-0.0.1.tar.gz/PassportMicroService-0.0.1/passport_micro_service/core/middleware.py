import importlib


class Middleware(object):

    @staticmethod
    def init_app(app):
        if 'MIDDLE_WARES' in app.config:
            for middleware in app.config['MIDDLE_WARES']:
                print('Load Middleware: ', middleware)
                pkgs = str(middleware).split('.')
                pkg = '.'.join([pkg for pkg in pkgs[:-1]])
                res = importlib.import_module(pkg)
                cls = getattr(res, pkgs[-1])
                cls(app)
