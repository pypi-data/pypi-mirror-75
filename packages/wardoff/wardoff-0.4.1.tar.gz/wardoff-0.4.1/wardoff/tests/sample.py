def baz():
    print("baz")


def raiseValueError():
    print("raise")
    raise ValueError("boom")


def fiz():
    print("fiz")
    print("fiz")
    print("fiz")
    print("fiz")
    raise DeprecationWarning()


def foz():
    raise DeprecationWarning("foz is deprecated please stop to use it")
    print("foz")


def fuzz():
    raise DeprecationWarning(
        "foz is deprecated please stop to use it" "blablabla" "blablafuzz"
    )
    print("foz")


class Bar:
    def run(self):
        print("run")

    def bar(self):
        print("bar")
        raise PendingDeprecationWarning("boom")


class Bob:
    def run(self):
        print("run")

    def yop(self):
        print("bar")
        raise FutureWarning("boom")


class Foo:
    pass


def boom(name="yo", age=1):
    pass
