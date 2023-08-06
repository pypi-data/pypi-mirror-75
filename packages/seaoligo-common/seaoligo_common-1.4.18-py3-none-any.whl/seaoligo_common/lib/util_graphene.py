import os
from graphene import AbstractType, Enum, Field, Int, List, NonNull, ObjectType, relay, String
from flask import current_app, g, request
from werkzeug.exceptions import Unauthorized


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        if (
            info.context.get('current_user')  # Valid login credentials provided
            or info.field_name in ['_service', 'sdl', '__typename']  # Gateway initialization
            or (os.environ.get('FLASK_ENV') == 'development'
                and ((info.field_name in ['__typename'])  # GraphQL Playground initialization
                     or request.headers.get('origin') ==
                     f"http://localhost:{os.environ.get('NODE_PORT')}"))  # GraphiQL request
            or current_app.config['TESTING']  # Test environment
        ):
            return next(root, info, **args)
        else:
            raise Unauthorized()


class NonNullConnection(relay.Connection, abstract=True):
    @classmethod
    def __init_subclass_with_meta__(cls, node=None, **kwargs):
        _node = None
        if not hasattr(cls, 'Edge'):
            _node = node
            class EdgeBase(ObjectType, name=f'{node._meta.name}Edge'):
                cursor = String(required=True)
                node = Field(_node, required=True)

            setattr(cls, 'Edge', EdgeBase)

        if not hasattr(cls, 'edges'):
            setattr(cls, 'edges', List(NonNull(cls.Edge), required=True))

        super(NonNullConnection, cls).__init_subclass_with_meta__(node=_node, **kwargs)


class Counts(AbstractType):
    total_count = Int()
    def resolve_total_count(root, info):
        return g.total_count

    filtered_count = Int()
    def resolve_filtered_count(root, info):
        return g.filtered_count

    page_count = Int()
    def resolve_page_count(root, info):
        return g.page_count

    current_page = Int()
    def resolve_current_page(root, info):
        return g.current_page


class OrganismSelect(Enum):
    HUMAN = 'human'
    MOUSE = 'mouse'
    # RAT = 'rat'


class AssemblySelect(Enum):
    hg38 = 'hg38'
    mm10 = 'mm10'
    # rn6 = 'rn6'
