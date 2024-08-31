# -*- coding: utf-8 -*-
"""
Command-Line Interface (`click`) Utilities
"""

import dataclasses as dc
import functools
import inspect
from datetime import datetime
from types import NoneType, SimpleNamespace, UnionType
from typing import Any, Callable, Literal, Union, get_args, get_origin

import click

from .base import components

# Mapping of custom Click types
CLICK_TYPES = {
    datetime: click.DateTime(),
}


def get_click_name(parameters: Any) -> str:
    """Extract Click variable name from parameters."""
    args = [x for x in parameters if x.startswith("--")]
    name = parameters[0][1:]
    if len(args) == 1:
        name = args[0][2:]
    return name


@dc.dataclass
class Field:
    """Represents a field's annotation and type information."""

    annotation: Any
    origin: Any = None
    types: tuple[Any, ...] = ()
    default: Any = None
    required: bool = True
    is_union: bool = False
    is_choice: bool = False

    def __post_init__(self) -> None:
        self.origin = get_origin(self.annotation)
        self.types = get_args(self.annotation)
        # Update if origin found
        if self.origin:
            self.required = NoneType not in self.types
            self.is_union = self.origin in (UnionType, Union)
            self.is_choice = self.origin is Literal
        else:
            self.types = (self.annotation,)
        # Remove NoneType
        if not self.required:
            self.types = tuple(x for x in self.types if x is not NoneType)
        # Single-Type
        if len(self.types) > 1 and self.is_union:
            raise ValueError(
                f"Expected 1 type, but found {len(self.types)} types: {self.types}"
            )
        # Real-Type
        if len(self.types) == 1 and self.is_union:
            real = Field(self.types[0])
            if real.is_choice:
                self.is_choice = True
                self.types = real.types


def get_function_default_value(func: Any, name: str) -> Any:
    """Retrieve the default value of a function parameter."""
    signature = inspect.signature(func)
    param: Any = signature.parameters.get(name)
    return param.default if param.default is not inspect.Parameter.empty else None


def custom_annotations(type_in, is_flag=False):
    """Transform to `click` type"""

    annotation = Field(type_in)
    param = SimpleNamespace(is_flag=is_flag, required=True)

    # Determine parameter type based on annotation
    if annotation.is_choice:
        param.type = click.Choice(annotation.types)
    else:
        param.type = annotation.types[0]
        if annotation.types[0] is bool:
            param.is_flag = True
    # Datetime
    if param.type == datetime:
        param.type = CLICK_TYPES[datetime]
    # Required
    param.required = annotation.required
    return param


class CustomArgument(click.Argument):
    """Custom click.Argument with additional help support."""

    def __init__(
        self,
        param_decls: list[str],
        help: str | None = None,  # pylint: disable=W
        **kwargs: Any,
    ) -> None:
        super().__init__(param_decls, **kwargs, metavar=param_decls[0].lower())
        self.help = help


class CustomCommand(click.Command):
    """Custom click.Command with enhanced help formatting."""

    def format_help(self, ctx: click.Context, formatter: click.HelpFormatter) -> None:
        """Format command help output with custom sections."""
        self.format_usage(ctx, formatter)
        self.format_help_text(ctx, formatter)
        self.format_epilog(ctx, formatter)
        # Custom 'Arguments' section
        self.format_arguments(ctx, formatter)
        # Custom 'Options' section
        self.format_options(ctx, formatter)

    def __get_annotation(self, arg: Any, fallback_type: Any = click.STRING) -> str:
        """Get the annotation of a function parameter."""
        field = Field(arg.annotation)
        # Choices
        if field.is_choice:
            return "|".join(field.types)
        # Typing
        the_type = field.types[0]
        if the_type is inspect.Parameter.empty:
            return fallback_type.name.replace(" ", "-")
        # Type Name
        field_type = the_type.__name__
        # if not field.required:
        #    field_type += " | None"
        return field_type

    def __custom_arg_help(self, ctx: Any, param: Any) -> tuple[str, str]:
        """Generate custom help text for arguments."""
        signature = inspect.signature(ctx.command.callback)
        arg = signature.parameters.get(param.name)
        annotation = self.__get_annotation(arg, param.type)
        help_text = param.help or ""
        return f"{param.name} ({annotation})", help_text

    def __custom_opt_help(self, ctx: Any, param: Any) -> tuple[str, str]:
        """Generate custom help text for options."""
        if param.name == "help":
            return f"{' '.join(param.opts)}", param.help
        signature = inspect.signature(ctx.command.callback)
        arg = signature.parameters.get(param.name)
        annotation = self.__get_annotation(arg, param.type)
        help_text = param.help or ""
        return f"{' '.join(param.opts)} ({annotation})", help_text

    def format_arguments(self, ctx: Any, formatter: click.HelpFormatter) -> None:
        """Format the command's arguments section."""
        args = [
            self.__custom_arg_help(ctx, param)
            for param in self.get_params(ctx)
            if isinstance(param, click.Argument)
        ]
        if args:
            with formatter.section("Arguments"):
                formatter.write_dl(args)

    def format_options(self, ctx: Any, formatter: click.HelpFormatter) -> None:
        """Format the command's options section."""
        opts = [
            self.__custom_opt_help(ctx, param)
            for param in self.get_params(ctx)
            if isinstance(param, click.Option)
        ]
        if opts:
            with formatter.section("Options"):
                formatter.write_dl(opts)


class CustomGroup(click.Group):
    """Custom click.Group that uses CustomCommand by default."""

    def command(self, *args: Any, **kwargs: Any) -> click.Command | Any:
        """Register a command with CustomCommand as default."""
        kwargs.setdefault("cls", CustomCommand)
        return super().command(*args, **kwargs)

    def group(self, *args: Any, **kwargs: Any) -> click.Group | Any:
        """Register a subgroup with CustomGroup as default."""
        kwargs.setdefault("cls", CustomGroup)
        return super().group(*args, **kwargs)


class CLI:
    """
    Interface for creating `click` groups. Instead of using the `CLI` class directly,
    utilize it through the `cli` instance for consistent command-line interface management.

    Args:
        obj (Callable): A callable to be turned into a `click.Group`.
        register (bool | None): Whether to register the `group` as a component to be loaded.

    Returns:
        group: A `click` group object.

    Examples:

    ```python
    # Simple
    @zmag.cli
    def cli(): pass

    @cli.command()
    def hello_world():
        zmag.cli.echo("Hello World (Command)")
    ```

    ```python
    # Groups
    @zmag.cli
    def cli(): pass

    @zmag.cli(group=True)
    def database():  pass

    @database.command()
    def hello_world():
        zmag.cli.echo("Hello World (Command)")

    # Register Group
    cli.add_command(database)
    ```
    """

    @classmethod
    def command(cls, obj: Any = None, *, register: bool = True) -> click.Command | Any:
        """
        Decorate a function as a `click` command.

        Args:
            obj (Callable): A callable to be turned into a `click.Command`.
            register (bool | None): Whether to register the `command` as a component to be loaded.

        Returns:
            command: A `click` command object.
        """
        if obj is None:
            return functools.partial(cls.command, register=register)

        # Real Wrapper
        obj = click.command(cls=CustomCommand)(obj)
        if register:
            components.register("command", obj)
        return obj

    # Echo Utilities
    @staticmethod
    def echo(*args, **kwargs) -> None:
        """Wrapper around `click.secho`."""
        click.secho(*args, **kwargs)

    @staticmethod
    def clear() -> None:
        """Wrapper around `click.clear`."""
        click.clear()

    @staticmethod
    def range(
        min: int | float = 0,  # pylint: disable=W
        max: int | float = 1,  # pylint: disable=W
        min_open: bool = False,
        max_open: bool = False,
        clamp: bool = False,
    ) -> click.IntRange | click.FloatRange:
        """
        Wrapper around `click.IntRange` and `click.FloatRange`.

        Returns:
            range: range based on the `min` type.
        """
        if isinstance(min, int):
            return click.IntRange(
                min, max, min_open=min_open, max_open=max_open, clamp=clamp
            )
        return click.FloatRange(
            min, max, min_open=min_open, max_open=max_open, clamp=clamp
        )

    # Main Decorators
    @staticmethod
    def argument(
        parameter: str,
        type: Any = None,  # pylint: disable=W
        default: Any = None,
        nargs: int | None = None,
        # Help text for the option
        help: str | None = None,  # pylint: disable=W
        # Others
        **kwargs: Any,
    ) -> Any:
        """Wrapper around `click.argument`."""

        def decorator(f: Callable) -> Callable:
            """decorator"""

            @functools.wraps(f)
            def wrapped(*args, **kwargs) -> Any:
                """wrapper"""
                return f(*args, **kwargs)

            default_value = get_function_default_value(f, parameter)
            custom = custom_annotations(f.__annotations__.get(parameter))

            # Apply click.argument to the wrapped function
            arg = click.argument(
                parameter,
                type=type or custom.type,
                required=custom.required,
                default=default_value or default,
                nargs=nargs,
                cls=CustomArgument,
                help=help,
                **kwargs,
            )(wrapped)
            return arg

        return decorator

    @staticmethod
    def option(
        # Positional arguments defining the option's name(s)
        *parameters: Any,
        # The type of the option's value
        type: Any = None,  # pylint: disable=W
        # Default value for the option
        default: Any = None,
        # Number of arguments that the option takes
        nargs: int = 1,
        # Treat the option as a boolean flag
        is_flag: bool = False,
        # Help text for the option
        help: str | None = None,  # pylint: disable=W
        # Prompt for user input if not provided
        prompt: bool | str | None = None,
        # Ask for confirmation after prompting for input
        confirmation_prompt: bool = False,
        # Allow multiple values (collects into a tuple)
        multiple: bool = False,
        # Count the number of times the option is provided
        count: bool = False,
        # Hide input (useful for passwords)
        hide_input: bool = False,
        # Others
        **kwargs: Any,
    ) -> Any:
        """Wrapper around `click.option`."""

        def decorator(f: Callable) -> Callable:
            """decorator"""

            @functools.wraps(f)
            def wrapped(*args, **kwargs) -> Any:
                """wrapper"""
                return f(*args, **kwargs)

            # Get Field Info
            name = get_click_name(parameters)
            default_value = get_function_default_value(f, name) if name else None
            custom = custom_annotations(f.__annotations__.get(name), is_flag)

            # Apply click.option to the wrapped function
            return click.option(
                *parameters,
                type=type or custom.type,
                required=custom.required,
                default=default_value or default if not custom.is_flag else False,
                confirmation_prompt=confirmation_prompt,
                count=count,
                help=help,
                hide_input=hide_input,
                is_flag=custom.is_flag,
                multiple=multiple,
                nargs=nargs,
                prompt=prompt,
                # cls=
                **kwargs,
            )(wrapped)

        return decorator

    def __call__(self, obj: Any = None, *, group: bool = False) -> click.Group | Any:
        """
        Interface for creating `click` groups.
        """
        if obj is None:
            return functools.partial(self.__call__, group=group)

        # Real Wrapper
        obj = click.group(cls=CustomGroup)(obj)
        if not group:  # type: ignore
            components.register("command", obj)
        return obj


# Instantiate the CommandLineInterface
cli: CLI = CLI()
