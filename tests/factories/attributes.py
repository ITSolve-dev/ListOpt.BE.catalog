from factory.declarations import LazyAttributeSequence

IDSequence = LazyAttributeSequence(lambda _, n: n + 1)


def ValueObjectIntSequence(cls):
    return LazyAttributeSequence(lambda _, n: cls(n + 1))
