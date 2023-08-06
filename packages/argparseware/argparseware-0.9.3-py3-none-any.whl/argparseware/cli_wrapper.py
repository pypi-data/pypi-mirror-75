"""
This package provides interfaces to enhance the `argparse` module allowing
for custom middleware to be injected during parsing and at run time.
"""

import os
import abc
import sys
import json
import argparse
import typing
import logging


def merge_dicts(data: dict, *args, overwrite: bool = True, recurse: bool = True) -> dict:
    """
    Merge dictionaries recursively and return the result.

    If *recurse* is true, the dictionaries are merged recursively. When *overwrite*
    is true, any value that exist in previous dictionaries will be overwritten with the
    latest (until that value is also a dictionary and *recurse* is true).
    """
    result = dict(data)

    for item in args:
        for key, value in item.items():
            data_value = data.get(key)

            if isinstance(value, dict) and isinstance(data_value, dict) and recurse:
                result[key] = merge_dicts(data_value, value, overwrite=overwrite)
            elif key in data:
                if overwrite:
                    result[key] = value
                else:
                    result[key] = data_value
            else:
                result[key] = value

    return result


def middleware(func: typing.Callable):
    """
    This method is an alias for `WrapperMiddleware` to be used
    as a decorator.
    """
    return WrapperMiddleware(func)


class IMiddleware(metaclass=abc.ABCMeta):
    """
    This class is the base interface for all middleware.
    """

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        This method is invoked before the arguments are parsed and is passed the parser
        instance.

        It's in this method that a subclass can add custom parser arguments.
        """

    def run(self, args: argparse.Namespace) -> None:
        """
        This method is invoked the the parser's `run` method is invoked, after all
        the middlewares have been configured and the arguments have been parsed. The
        first argument is the namespace object containing the parsed arguments.
        """


class WrapperMiddleware(IMiddleware):
    """
    Wrapper middlware, typically used by decorators.
    """

    def __init__(self, func: typing.Callable, conf: typing.Callable = None) -> None:
        """
        This middleware is typically used by decorators to create custom middleware
        on the fly.

        The *func* argument is a callable that will be executed, with the extracted
        arguments as the first paramter.

        The *conf* argument is a callable that will be executed before the arguments
        are parsed, usually to define custom arguments. Alternatively, the `configure`
        method also acts as a decorator that can be used for this same purpose.
        """
        self.func = func
        self.conf = conf or (lambda parser: None)

    def configure(self, arg: typing.Union[typing.Callable, argparse.ArgumentParser]) \
            -> typing.Union['WrapperMiddleware', None]:  # pylint: disable=arguments-differ
        """
        Configure the middleware.
        """
        if isinstance(arg, ArgumentParser):
            self.conf(arg)
            return None

        self.conf = arg
        return self

    def run(self, args):
        self.func(args)


class LoggingMiddleware(IMiddleware):
    """
    Logging middleware.
    """

    def __init__(self, name: str = None, *, formatter: logging.Formatter = None,
                 handler: logging.Handler = None) -> None:
        """
        This middleware registers a few arguments that allow to automatically configure
        and control the logging output.

        The *name* argument is the name of the logger to configure. By default, the
        root logger is used.

        The *formatter* argument is an instance of `Formatter` that will be used.
        If omitted, it is automatically configured.

        The *handler* argument is an instance of a `Handler` that will be used for
        output. If omitted, it will log messages to stderr.
        """
        self.name = name
        self.formatter = formatter
        self.handler = handler

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the middleware arguments.
        """
        parser.add_argument('--log-std', action='store_true',
                            help='the whether to enable standard logging when logging to files')
        parser.add_argument('--log-file',
                            help='the log file to use')

        group = parser.add_mutually_exclusive_group()
        group.add_argument('--log-level',
                           help='the log level to use')
        group.add_argument('-q', '--quiet', action='store_true',
                           help='suppress the output except warnings and errors')
        group.add_argument('-v', '--verbose', action='store_true',
                           help='enable additional debug output')

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        log_level = args.log_level or \
                ('debug' if args.verbose else 'warning' if args.quiet else 'info')
        formatter = self.formatter or \
                logging.Formatter('%(asctime)-25s %(levelname)-10s %(name)-20s: %(message)s')

        logger = logging.getLogger(self.name)

        if not args.log_file or args.log_std:
            handler = self.handler or logging.StreamHandler(sys.stderr)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(log_level.upper())

        if args.log_file:
            handler = logging.FileHandler(args.log_file)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(log_level.upper())

        args.__dict__.update({'log_level': log_level})
        del args.__dict__['quiet']
        del args.__dict__['verbose']


class ConfigMiddleware(IMiddleware):
    """
    Configuration file middleware.
    """

    def __init__(self, defaults: typing.List[str] = None, *, allow_multi: bool = False,
                 ignore_missing: bool = False, overwrite: bool = False, merge: bool = True) -> None:
        """
        This middleware loads configuration files and merge their contents into the
        parser's namespace object.

        The *defaults* argument is a list of default configuration files to load.

        If *allow_multi* is enabled, the argument can be specified multiple times, with
        each loaded configuration file being merged to the previous ones.

        If *ignore_missing* is enabled, configuration files that do not exist will not
        cause exceptions to be raised.

        When *overwrite* is true, values that already exist in the parser's namespace
        will be overwritten by values in the configuration files. Otherwise, if a duplicate
        occurs, the namespace value has precedence, unless it's a dict and merging is enabled.

        When *merge* is enabled, if a value is a dictionary and exists both in the namespace
        and configuration file, it will be merged into the resulting object, complying with
        the *overwrite* parameter for duplicate values. If *merge* is false and *overwrite*
        is true, a value that is a dict that exists in both source and destination will be
        completely overwritten by the configuration file value.
        """
        self.defaults = defaults or []
        self.allow_multi = allow_multi
        self.ignore_missing = ignore_missing
        self.overwrite = overwrite
        self.merge = merge

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the middleware arguments.
        """
        parser.add_argument('-c', '--config', action='append' if self.allow_multi else None,
                            dest='config_file',
                            help='the path to the configuration file')

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        import anyconfig  # pylint: disable=import-outside-toplevel

        files = args.config_file or self.defaults
        data = anyconfig.load(files, ignore_missing=self.ignore_missing)
        result = merge_dicts(
            args.__dict__, data,
            overwrite=self.overwrite,
            recurse=self.merge,
        )

        args.__dict__.update(result)


class ConfigListMiddleware(IMiddleware):
    """
    Configuration file list middleware.
    """

    def __init__(self, defaults: typing.Union[bool, dict] = None, *, allow_multi: bool = True,
                 ignore_missing: bool = False, merge: bool = True) -> None:
        """
        This middleware loads configuration files and adds a variable list to the argument
        parser namespace, with each entry being the parsed configuration data in the
        order it was declared.

        The *defaults* argument is a dictionary of data that will be set as the base data
        dictionary for each loaded configuration file. If *defaults* is the `True` boolean,
        the arguments from the namespace are used as defaults.

        If *allow_multi* is disabled, the argument can be only be specified once.

        If *ignore_missing* is enabled, configuration files that do not exist will not
        cause exceptions to be raised.

        When *merge* is enabled, if a value is a dictionary and exists both in the namespace
        and configuration file, it will be merged into the resulting object. If *merge* is false,
        a value that is a dict that exists in both source and destination will be
        completely overwritten by the configuration file value.
        """
        self.defaults = defaults or {}
        self.allow_multi = allow_multi
        self.ignore_missing = ignore_missing
        self.merge = merge

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the middleware arguments.
        """
        parser.add_argument('-c', '--config', action='append' if self.allow_multi else None,
                            dest='config_files',
                            help='the path to the configuration file')

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        import anyconfig  # pylint: disable=import-outside-toplevel

        defaults = args.__dict__ if self.defaults is True else self.defaults

        results = []
        for filename in args.config_files or []:
            if filename == '-':
                result = dict(defaults)
            else:
                data = anyconfig.load(filename, ignore_missing=self.ignore_missing)
                result = merge_dicts(
                    defaults, data,
                    overwrite=True,
                    recurse=self.merge,
                )
            results.append(result)

        args.__dict__.update({'config_data': results})


class InlineConfigMiddleware(IMiddleware):
    """
    Inline configuration middleware.
    """

    def __init__(self, *, overwrite: bool = True, merge: bool = True) -> None:
        """
        This middleware registers an argument - that can be specified multiple times -
        that allows to override configuration values/arguments using a string syntax.

        Each argument should be in the form of `KEY=VALUE`. The VALUE will be parsed
        as a JSON string. If it's not valid JSON, it will be assumed to be a string.

        Example values:
            - `foo=42`: int
            - `foo=42.0`: float
            - `foo=null`: None
            - `foo=bar`: str
            - `foo=[1,2,3]`: list
            - `foo={"hello": "world"}`: dict
            - `foo=true`: bool
            - `foo="null"`: str

        The *overwrite* and *merge* arguments work the same as the `ConfigMiddleware`.
        """
        self.overwrite = overwrite
        self.merge = merge

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the middleware arguments.
        """
        parser.add_argument('-e', '--env', action='append',
                            dest='config_env',
                            help='additional configuration values to pass, as JSON strings')

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        items = []
        for item in args.config_env or []:
            if '=' in item:
                key, value = item.split('=', 1)
                try:
                    value = json.loads(value)
                except json.decoder.JSONDecodeError:
                    pass
                items.append({key: value})

        result = merge_dicts(
            args.__dict__, *items,
            overwrite=self.overwrite,
            recurse=self.merge,
        )

        args.__dict__.update(result)
        del args.__dict__['config_env']


class EnvironmentConfigMiddleware(IMiddleware):
    """
    Environment variables middleware.
    """

    def __init__(self, prefix: str, *, lower: bool = True, overwrite: bool = False,
                 merge: bool = True) -> None:
        """
        This middleware allows for configuration values/arguments to be overriden using
        environment variables.

        The *prefix* is a string argument that defines the prefix (case sensitive) to
        look for in environment variables. Per example, with a prefix of `TEST_`, the
        variables `TEST_FOO` and `TEST_BAR` will be matched.

        The `lower` argument defines whether to lower case the variable key - everything
        after the prefix - when storing it. If enabled, in `TEST_FOO=1`, the resulting
        argument key will be `foo` rather than `FOO`.

        The values parsing rules, *overwrite* and *merge* arguments work the same way as
        the `InlineConfigMiddleware`.
        """
        self.lower = lower
        self.prefix = prefix
        self.overwrite = overwrite
        self.merge = merge

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        data = {}
        for key, value in os.environ.items():
            if not key.startswith(self.prefix):
                continue

            if self.lower:
                key = key[len(self.prefix):].lower()

            try:
                value = json.loads(value)
                data[key] = value
            except json.decoder.JSONDecodeError:
                data[key] = value

        result = merge_dicts(
            args.__dict__, data,
            overwrite=self.overwrite,
            recurse=self.merge,
        )
        args.__dict__.update(result)


class InjectMiddleware(IMiddleware):
    """
    Default arguments injection middleware.
    """

    def __init__(self, defaults: dict) -> None:
        """
        This middleware injects defaults for any parameter that wasn't specified at
        runtime.
        """
        self.defaults = defaults

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        result = merge_dicts(
            args.__dict__, self.defaults,
            overwrite=False, recurse=True,
        )

        args.__dict__.update(result)


class ServerMiddleware(IMiddleware, metaclass=abc.ABCMeta):
    """
    WSGI server middleware.
    """

    def __init__(self, app: typing.Callable, addr: typing.Union[int, str]) -> None:
        """
        This middleware interface can be used by sub-implementations to configure
        a WSGI server to listen on a specific address.

        The first *app* argument is the WSGI callable object.

        The *addr* argument should be either an integer with a port number, or a string
        in the format of `addr:port`. If an int is supplied, the listen address
        is assumed to be `0.0.0.0` (listening on all interfaces).
        """
        self.app = app
        self.addr = addr

    def parse_addr(self, addr: typing.Union[int, str]) -> typing.Tuple[str, int]:
        """
        Parse an address string into a tuple of host, port.
        """
        if isinstance(addr, str) and ':' in addr:
            host, port = addr.split(addr)
            host = host or '0.0.0.0'
            return (host, int(port))

        return ('0.0.0.0', int(addr))

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the middleware arguments.
        """
        parser.add_argument('-L', '--listen-addr', default=str(self.addr),
                            help='the address and/or port to listen on '
                                 '(e.g.: 8080 or localhost:1234')

    @abc.abstractmethod
    def run(self, args: argparse.Namespace) -> None:
        """
        This method should be implemented by subclasses to actually run a server
        based on the source arguments.
        """


class FlaskServerMiddleware(ServerMiddleware, metaclass=abc.ABCMeta):
    """
    Server middleware to run Flask applications integrated server.
    """

    def __init__(self, app: typing.Union['Flask', ServerMiddleware],
                 addr: typing.Union[int, str] = None, *, debug: bool = False) -> None:
        """
        This middleware allows to run Flask applications through the
        command line.

        The first argument should be a `Flask` instance to run. Alternatively,
        it can be a instance of a `ServerMiddleware` subclass. When that is the
        case, the server will be started using this middleware object instead,
        unless the debug switch (`--debug`) is passed at runtime.

        Before the server is run, the passed arguments are also assigned to
        application object's `Flask.args` attribute.
        """
        if not isinstance(app, ServerMiddleware):
            if not addr:
                raise ValueError('addr argument is mandatory')
            super().__init__(app, addr)
        else:
            super().__init__(app, app.addr)
        self.debug = debug

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the middleware arguments.
        """
        if isinstance(self.app, ServerMiddleware):
            self.app.configure(parser)
        else:
            super().configure(parser)

        parser.add_argument('--debug', action='store_true', dest='flask_debug',
                            help='enable the server debug mode')

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        host, port = self.parse_addr(args.listen_addr)
        if isinstance(self.app, ServerMiddleware):
            self.app.app.args = args
            if args.flask_debug:
                self.app.app.run(host=host, port=port, debug=True)
            else:
                self.app.run(args)
        else:
            self.app.args = args
            self.app.run(host=host, port=port, debug=args.flask_debug)


class GunicornServerMiddleware(ServerMiddleware, metaclass=abc.ABCMeta):
    """
    Server middleware that wraps gunicorn for WSGI applicications.
    """
    # pylint: disable=import-outside-toplevel

    def __init__(self, *args, count: int = None, timeout: int = 120) -> None:
        """
        This middleware wraps a WSGI application callable to run through
        a gunicorn server.

        The *count* is the default count of workers to pre-fork. If omitted, it
        defaults to the number of available CPUs.

        The *timeout* is the default count for a request timeout, after which
        the pre-fork worker will bail and terminate a pending request.
        """
        super().__init__(*args)
        import multiprocessing
        self.count = count or multiprocessing.cpu_count()
        self.timeout = timeout

    def configure(self, parser: argparse.ArgumentParser) -> None:
        """
        Configure the middleware arguments.
        """
        super().configure(parser)

        parser.add_argument('-j', '--prefork-count', type=int, default=self.count,
                            help='the number of workers to pre-fork')
        parser.add_argument('-T', '--request-timeout', type=int, default=self.timeout,
                            help='the amount of time before a worker times out')
        parser.add_argument('-l', '--prefork-preload', action='store_true',
                            help='preload the workers on startup')

        found = False
        for item in parser.middlewares:
            if isinstance(item, LoggingMiddleware):
                found = True
                break

        if not found:
            parser.add_middleware(LoggingMiddleware())

    def run(self, args: argparse.Namespace) -> None:
        """
        Run the middleware.
        """
        try:
            log_level = args.log_level
        except AttributeError:
            log_level = 'info'

        self.run_server(
            args.listen_addr,
            count=args.prefork_count,
            timeout=args.request_timeout,
            preload=args.prefork_preload,
            log_level=log_level,
        )

    def run_server(self, addr, *, count: int, timeout: int, preload: bool, log_level: int):
        """
        Run the application server through gunicorn.

        This function creates and runs the application server for the *app* WSGI application.
        It will listen bind to *host* on *port*.

        Since it is backed by gunicorn and uses a pre-fork model, it can be passed the *count*
        number of workers to create on startup. It defaults to the number of CPUs on the
        machine.

        The *timeout* defines, in seconds, the amount of time after which a worker is
        considered to have timed out and will be forcefully restarted.

        If *preload* is switched on, the code is pre-loaded in the workers at startup
        rather than lazy loaded at runtime.

        The *log_level* can be changed to a specific verbosity level, using the `logging`
        package values.
        """
        from gunicorn.app.wsgiapp import WSGIApplication

        wsgi_app = self.app
        class WSGIServer(WSGIApplication):
            """The WSGI Server implementation."""

            def init(self, parser, opts, args):
                pass

            def load(self):
                return wsgi_app

        host, port = self.parse_addr(addr)
        args = [
            '--bind', '{0}:{1}'.format(host, port),
            '--log-level', logging.getLevelName(log_level).lower(),
            '--workers', str(count),
            '--timeout', str(timeout),
            '--preload' if preload else '',
            '--access-logfile', '-',
        ]

        sys.argv = [sys.argv[0]]
        os.environ['GUNICORN_CMD_ARGS'] = ' '.join(args)
        return WSGIServer('').run()


class ArgumentParser(argparse.ArgumentParser):
    """
    Argument parser class override.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        This special argument parser class works the same way as the original,
        except that it adds the `add_middleware` and `run` methods.
        """
        super().__init__(*args, **kwargs)
        self.middlewares = []

    def add_middleware(self, item: IMiddleware) -> None:
        """
        Add a middleware to the parser.

        Middleware objects are first configured prior to parsing arguments,
        then run when the parser's `run` method is invoked.

        It is possible to add middleware within another middleware `configure`
        or `run` implementations using this method.
        """
        self.middlewares.append(item)

    def middleware(self, func: typing.Callable) -> WrapperMiddleware:
        """
        This method allows to easily add a custom middleware function to an
        argument parser.
        """
        item = WrapperMiddleware(func)
        self.add_middleware(item)
        return item

    def parse_args(self, *args, **kwargs) -> argparse.Namespace:  # pylint: disable=arguments-differ
        """
        Override the parent method to automatically configure middleware.
        """
        index = 0
        while True:
            try:
                item = self.middlewares[index]
                index += 1
            except IndexError:
                break
            item.configure(self)

        return super().parse_args(*args, **kwargs)

    def run(self, *args, **kwargs) -> argparse.Namespace:
        """
        Run the argument parser.

        This method works the same way as `parse_args` returning a `Namespace`
        object with the arguments. However, unlike the former once the arguments
        have been parsed, each registered middleware will have its `run` method
        invoked and the resulting namespace object will be returned.
        """
        namespace = self.parse_args(*args, **kwargs)

        index = 0
        while True:
            try:
                item = self.middlewares[index]
                index += 1
            except IndexError:
                break
            item.run(namespace)

        return namespace
