import sqlalchemy as sa

def inspect_type(mixed):
    if isinstance(mixed, sa.orm.attributes.InstrumentedAttribute):
        return mixed.property.columns[0].type
    elif isinstance(mixed, sa.orm.ColumnProperty):
        return mixed.columns[0].type
    elif isinstance(mixed, sa.Column):
        return mixed.type


def is_case_insensitive(mixed):
    try:
        return isinstance(
            inspect_type(mixed).comparator,
            CaseInsensitiveComparator
        )
    except AttributeError:
        try:
            return issubclass(
                inspect_type(mixed).comparator_factory,
                CaseInsensitiveComparator
            )
        except AttributeError:
            return False

class CaseInsensitiveComparator(sa.Unicode.Comparator):
    @classmethod
    def lowercase_arg(cls, func):
        def operation(self, other, **kwargs):
            operator = getattr(sa.Unicode.Comparator, func)
            if other is None:
                return operator(self, other, **kwargs)
            if not is_case_insensitive(other):
                other = sa.func.lower(other)
            return operator(self, other, **kwargs)
        return operation

    def in_(self, other):
        if isinstance(other, list) or isinstance(other, tuple):
            other = map(sa.func.lower, other)
        return sa.Unicode.Comparator.in_(self, other)

    def notin_(self, other):
        if isinstance(other, list) or isinstance(other, tuple):
            other = map(sa.func.lower, other)
        return sa.Unicode.Comparator.notin_(self, other)

string_operator_funcs = [
    '__eq__',
    '__ne__',
    '__lt__',
    '__le__',
    '__gt__',
    '__ge__',
    'concat',
    'contains',
    'ilike',
    'like',
    'notlike',
    'notilike',
    'startswith',
    'endswith',
]

for func in string_operator_funcs:
    setattr(
        CaseInsensitiveComparator,
        func,
        CaseInsensitiveComparator.lowercase_arg(func)
    )

class EmailType(sa.types.TypeDecorator):
    """
    Provides a way for storing emails in a lower case.
    Example::
        from sqlalchemy_utils import EmailType
        class User(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.Unicode(255))
            email = sa.Column(EmailType)
        user = User()
        user.email = 'John.Smith@foo.com'
        user.name = 'John Smith'
        session.add(user)
        session.commit()
        # Notice - email in filter() is lowercase.
        user = (session.query(User)
                       .filter(User.email == 'john.smith@foo.com')
                       .one())
        assert user.name == 'John Smith'
    """
    impl = sa.Unicode
    comparator_factory = CaseInsensitiveComparator
    cache_ok = True

    def __init__(self, length=255, *args, **kwargs):
        super().__init__(length=length, *args, **kwargs)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return value.lower()
        return value

    @property
    def python_type(self):
        return self.impl.type.python_type
