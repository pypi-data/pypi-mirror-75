import flufl.i18n.testing.messages

from flufl.i18n import Application, PackageStrategy


def test_application_name():
    strategy = PackageStrategy('flufl', flufl.i18n.testing.messages)
    application = Application(strategy)
    assert application.name == 'flufl'
