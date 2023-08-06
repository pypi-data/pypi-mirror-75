import asyncio
import random
import string
from typing import List, Dict, Type, Callable

from macrobase_driver import MacrobaseDriver
from macrobase_driver.config import CommonConfig, AppConfig, DriverConfig
from structlog import get_logger

from macrobase.hook import HookNames
from macrobase.pool import DriversPool

log = get_logger('macrobase')


class Application:

    def __init__(self, config: AppConfig, name: str = None):
        """Create Application object.

        :param name: string for naming drivers
        :return: Nothing
        """
        self.name = name
        self._config = config
        self._pool = None
        self._hooks: Dict[HookNames, List[Callable]] = {}
        self.drivers: Dict[str, MacrobaseDriver] = {}

    @property
    def config(self) -> AppConfig:
        return self._config

    def get_driver(self, driver_cls: Type[MacrobaseDriver], driver_config: Type[DriverConfig], *args, **kwargs) -> MacrobaseDriver:
        # TODO: fix type hints
        common_config = CommonConfig(self.config, driver_config)
        driver = driver_cls(config=common_config, *args, **kwargs)

        return driver

    def add_driver(self, driver: MacrobaseDriver, alias: str = None):
        if alias is None:
            alias = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
        self.drivers[alias] = driver

    def add_drivers(self, drivers: List[MacrobaseDriver]):
        [self.add_driver(d) for d in drivers]

    def add_hook(self, name: HookNames, handler):
        if name not in self._hooks:
            self._hooks[name] = []

        self._hooks[name].append(handler)

    def call_hooks(self, name: HookNames):
        if name not in self._hooks:
            return

        for handler in self._hooks[name]:
            handler(self)

    # TODO: fix logging
    # def _apply_logging(self):
    #     self._logging_config = get_logging_config(self.config.app)
    #     logging.config.dictConfig(self._logging_config)

    def _prepare(self):
        # self._apply_logging()
        pass

    def run(self, aliases: List[str] = None):
        self._prepare()

        self.call_hooks(HookNames.before_start)

        if aliases is not None and len(aliases) == 1:
            try:
                self.drivers.get(aliases[0]).run()
            finally:
                asyncio.get_event_loop().close()
        else:
            self._pool = DriversPool()
            self._pool.start(
                [d for a, d in self.drivers.items() if a in aliases]
                if aliases is not None
                else list(self.drivers.values())
            )

        self.call_hooks(HookNames.after_stop)
