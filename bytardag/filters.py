from bytardag.models import Permission


class Filters(object):
    def init_app(self, app):
        app.jinja_env.filters["has_permission"] = Filters.has_permission

    @staticmethod
    def has_permission(user, permission):
        return user.can(getattr(Permission, permission))
