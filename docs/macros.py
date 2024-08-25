"""
Mkdocs-Macros Module

# Learn More. . .
https://mkdocs-macros-plugin.readthedocs.io/en/latest/macros/
"""


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments, used to perform a transformation
    - variables: the dictionary that contains the environment variables
    """

    @env.macro
    def current_year():
        from datetime import datetime

        return datetime.now().year
