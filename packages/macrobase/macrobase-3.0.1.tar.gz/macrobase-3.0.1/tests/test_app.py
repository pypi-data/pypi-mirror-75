import pytest

from macrobase.app import Application, HookNames
from tests.sample_app import SampleApplication


@pytest.mark.timeout(3)
def test_empty_application(application: Application):
    application.run()


def test_hooks_before_start(mocker, application: Application, sample_app: SampleApplication):
    hook_spy = mocker.spy(sample_app, 'hook_before_start')

    application.add_hook(HookNames.before_start, sample_app.hook_before_start)
    application.run()

    hook_spy.assert_called_once_with(application)


def test_hooks_after_stop(mocker, application: Application, sample_app: SampleApplication):
    hook_spy = mocker.spy(sample_app, 'hook_after_stop')

    application.add_hook(HookNames.before_start, sample_app.hook_after_stop)
    application.run()

    hook_spy.assert_called_once_with(application)
