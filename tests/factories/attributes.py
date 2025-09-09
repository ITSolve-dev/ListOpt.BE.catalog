from factory.declarations import LazyAttributeSequence

IDSequence = LazyAttributeSequence(lambda _, n: n + 1)


class ValueObjectIntSequence:
    def __new__(cls, obj: type) -> LazyAttributeSequence:
        return LazyAttributeSequence(lambda _, n: obj(n + 1))
