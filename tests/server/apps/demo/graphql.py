# -*- coding: utf-8 -*-
"""
{ API - GraphQL }
"""

import zmag

from . import forms, types


# Create your API (GraphQL) here.
@zmag.gql
class Demo:
    """Demo Api"""

    class Meta:
        """GQL-Class Metadata"""

        # app = None
        model = types.Book

    class Query:
        """Query"""

        async def detail(self, info) -> str:
            """Read the Docs"""
            # print(info)
            return "Detail"

        async def list(self, info) -> list[types.Book | None]:
            """Read the Docs"""
            # print(info)
            return [
                types.Book(
                    _id=1,
                    id="1",
                    title="The Great Gatsby",
                    author=types.Author(
                        name="F. Scott Fitzgerald",
                    ),
                )
            ]

    class Mutation:
        """Mutation"""

        async def create(
            self,
            info,
            form: forms.Point2D | None,
        ) -> zmag.mutation[types.Book]:
            """Read the Docs"""
            if form:
                print(form.input)
            return zmag.mutation()


# {'one': [('x', strawberry.scalars.ID), ('email', typing.Optional[str], Field(name='email',type=typing.Optional[str],default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD)), ('y', typing.Optional[float], Field(name='y',type=typing.Optional[float],default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD)), ('z', typing.Optional[float], Field(name='z',type=typing.Optional[float],default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD)), ('input', typing.Any, Field(name='input',type=typing.Any,default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD))], 'two': [('email', typing.Optional[str], Field(name='email',type=typing.Optional[str],default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD)), ('y', typing.Optional[float], Field(name='y',type=typing.Optional[float],default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD)), ('z', typing.Optional[float], Field(name='z',type=typing.Optional[float],default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD)), ('input', typing.Any, Field(name='input',type=typing.Any,default=None,default_factory=<dataclasses._MISSING_TYPE object at 0x0000023D05287B00>,init=True,repr=True,hash=None,compare=True,metadata=mappingproxy({}),kw_only=False,_field_type=_FIELD))]}
