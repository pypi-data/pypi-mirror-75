"""
# constructs-tokens-staging

Tokens system for the constructs programming model
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import constructs


@jsii.data_type(
    jsii_type="constructs-tokens-staging.EncodingOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint"},
)
class EncodingOptions:
    def __init__(self, *, display_hint: typing.Optional[str] = None) -> None:
        """Properties to string encodings.

        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """A hint for the Token's purpose when stringifying it.

        default
        :default: - no display hint
        """
        return self._values.get("display_hint")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncodingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="constructs-tokens-staging.IAnyProducer")
class IAnyProducer(jsii.compat.Protocol):
    """Interface for lazy untyped value producers."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAnyProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -
        """
        ...


class _IAnyProducerProxy:
    """Interface for lazy untyped value producers."""

    __jsii_type__ = "constructs-tokens-staging.IAnyProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="constructs-tokens-staging.IFragmentConcatenator")
class IFragmentConcatenator(jsii.compat.Protocol):
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFragmentConcatenatorProxy

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        ...


class _IFragmentConcatenatorProxy:
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """

    __jsii_type__ = "constructs-tokens-staging.IFragmentConcatenator"

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


@jsii.interface(jsii_type="constructs-tokens-staging.IListProducer")
class IListProducer(jsii.compat.Protocol):
    """Interface for lazy list producers."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -
        """
        ...


class _IListProducerProxy:
    """Interface for lazy list producers."""

    __jsii_type__ = "constructs-tokens-staging.IListProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="constructs-tokens-staging.INumberProducer")
class INumberProducer(jsii.compat.Protocol):
    """Interface for lazy number producers."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INumberProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -
        """
        ...


class _INumberProducerProxy:
    """Interface for lazy number producers."""

    __jsii_type__ = "constructs-tokens-staging.INumberProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="constructs-tokens-staging.IPostProcessor")
class IPostProcessor(jsii.compat.Protocol):
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPostProcessorProxy

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -
        """
        ...


class _IPostProcessorProxy:
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it."""

    __jsii_type__ = "constructs-tokens-staging.IPostProcessor"

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -
        """
        return jsii.invoke(self, "postProcess", [input, context])


@jsii.interface(jsii_type="constructs-tokens-staging.IResolvable")
class IResolvable(jsii.compat.Protocol):
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolvableProxy

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -
        """
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.
        """
        ...


class _IResolvableProxy:
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.
    """

    __jsii_type__ = "constructs-tokens-staging.IResolvable"

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.
        """
        return jsii.get(self, "creationStack")

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -
        """
        return jsii.invoke(self, "resolve", [context])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.
        """
        return jsii.invoke(self, "toString", [])


@jsii.interface(jsii_type="constructs-tokens-staging.IResolveContext")
class IResolveContext(jsii.compat.Protocol):
    """Current resolution context for tokens."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolveContextProxy

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output."""
        ...

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution has been initiated."""
        ...

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -
        """
        ...


class _IResolveContextProxy:
    """Current resolution context for tokens."""

    __jsii_type__ = "constructs-tokens-staging.IResolveContext"

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output."""
        return jsii.get(self, "preparing")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution has been initiated."""
        return jsii.get(self, "scope")

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -
        """
        return jsii.invoke(self, "registerPostProcessor", [post_processor])

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -
        """
        return jsii.invoke(self, "resolve", [x])


@jsii.interface(jsii_type="constructs-tokens-staging.IStringProducer")
class IStringProducer(jsii.compat.Protocol):
    """Interface for lazy string producers."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStringProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -
        """
        ...


class _IStringProducerProxy:
    """Interface for lazy string producers."""

    __jsii_type__ = "constructs-tokens-staging.IStringProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="constructs-tokens-staging.ITokenMapper")
class ITokenMapper(jsii.compat.Protocol):
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenMapperProxy

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -
        """
        ...


class _ITokenMapperProxy:
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.
    """

    __jsii_type__ = "constructs-tokens-staging.ITokenMapper"

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -
        """
        return jsii.invoke(self, "mapToken", [t])


@jsii.interface(jsii_type="constructs-tokens-staging.ITokenResolver")
class ITokenResolver(jsii.compat.Protocol):
    """How to resolve tokens."""

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenResolverProxy

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self, l: typing.List[str], context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -
        """
        ...

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self, s: "TokenizedStringFragments", context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -
        """
        ...

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: "IResolvable",
        context: "IResolveContext",
        post_processor: "IPostProcessor",
    ) -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -
        """
        ...


class _ITokenResolverProxy:
    """How to resolve tokens."""

    __jsii_type__ = "constructs-tokens-staging.ITokenResolver"

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self, l: typing.List[str], context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -
        """
        return jsii.invoke(self, "resolveList", [l, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self, s: "TokenizedStringFragments", context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -
        """
        return jsii.invoke(self, "resolveString", [s, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: "IResolvable",
        context: "IResolveContext",
        post_processor: "IPostProcessor",
    ) -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="constructs-tokens-staging.Lazy"):
    """Lazily produce a value.

    Can be used to return a string, list or numeric value whose actual value
    will only be calculated later, during synthesis.
    """

    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(
        cls,
        producer: "IAnyProducer",
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty_array: typing.Optional[bool] = None,
    ) -> "IResolvable":
        """Produces a lazy token from an untyped value.

        :param producer: The lazy producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false
        """
        options = LazyAnyValueOptions(
            display_hint=display_hint, omit_empty_array=omit_empty_array
        )

        return jsii.sinvoke(cls, "anyValue", [producer, options])

    @jsii.member(jsii_name="listValue")
    @builtins.classmethod
    def list_value(
        cls,
        producer: "IListProducer",
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty: typing.Optional[bool] = None,
    ) -> typing.List[str]:
        """Returns a list-ified token for a lazy value.

        :param producer: The producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false
        """
        options = LazyListValueOptions(display_hint=display_hint, omit_empty=omit_empty)

        return jsii.sinvoke(cls, "listValue", [producer, options])

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, producer: "INumberProducer") -> jsii.Number:
        """Returns a numberified token for a lazy value.

        :param producer: The producer.
        """
        return jsii.sinvoke(cls, "numberValue", [producer])

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(
        cls, producer: "IStringProducer", *, display_hint: typing.Optional[str] = None
    ) -> str:
        """Returns a stringified token for a lazy value.

        :param producer: The producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint
        """
        options = LazyStringValueOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "stringValue", [producer, options])


@jsii.data_type(
    jsii_type="constructs-tokens-staging.LazyAnyValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint", "omit_empty_array": "omitEmptyArray"},
)
class LazyAnyValueOptions:
    def __init__(
        self,
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty_array: typing.Optional[bool] = None,
    ) -> None:
        """Options for creating lazy untyped tokens.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint
        if omit_empty_array is not None:
            self._values["omit_empty_array"] = omit_empty_array

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint
        """
        return self._values.get("display_hint")

    @builtins.property
    def omit_empty_array(self) -> typing.Optional[bool]:
        """If the produced value is an array and it is empty, return 'undefined' instead.

        default
        :default: false
        """
        return self._values.get("omit_empty_array")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyAnyValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="constructs-tokens-staging.LazyListValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint", "omit_empty": "omitEmpty"},
)
class LazyListValueOptions:
    def __init__(
        self,
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty: typing.Optional[bool] = None,
    ) -> None:
        """Options for creating a lazy list token.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint
        """
        return self._values.get("display_hint")

    @builtins.property
    def omit_empty(self) -> typing.Optional[bool]:
        """If the produced list is empty, return 'undefined' instead.

        default
        :default: false
        """
        return self._values.get("omit_empty")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyListValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="constructs-tokens-staging.LazyStringValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint"},
)
class LazyStringValueOptions:
    def __init__(self, *, display_hint: typing.Optional[str] = None) -> None:
        """Options for creating a lazy string token.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint
        """
        return self._values.get("display_hint")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyStringValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="constructs-tokens-staging.ResolveOptions",
    jsii_struct_bases=[],
    name_mapping={"resolver": "resolver", "scope": "scope", "preparing": "preparing"},
)
class ResolveOptions:
    def __init__(
        self,
        *,
        resolver: "ITokenResolver",
        scope: constructs.IConstruct,
        preparing: typing.Optional[bool] = None,
    ) -> None:
        """Options to the resolve() operation.

        NOT the same as the ResolveContext; ResolveContext is exposed to Token
        implementors and resolution hooks, whereas this struct is just to bundle
        a number of things that would otherwise be arguments to resolve() in a
        readable way.

        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false
        """
        self._values = {
            "resolver": resolver,
            "scope": scope,
        }
        if preparing is not None:
            self._values["preparing"] = preparing

    @builtins.property
    def resolver(self) -> "ITokenResolver":
        """The resolver to apply to any resolvable tokens found."""
        return self._values.get("resolver")

    @builtins.property
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution is performed."""
        return self._values.get("scope")

    @builtins.property
    def preparing(self) -> typing.Optional[bool]:
        """Whether the resolution is being executed during the prepare phase or not.

        default
        :default: false
        """
        return self._values.get("preparing")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolveOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IFragmentConcatenator)
class StringConcat(
    metaclass=jsii.JSIIMeta, jsii_type="constructs-tokens-staging.StringConcat"
):
    """Converts all fragments to strings and concats those.

    Drops 'undefined's.
    """

    def __init__(self) -> None:
        jsii.create(StringConcat, self, [])

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -
        """
        return jsii.invoke(self, "join", [left, right])


class Token(metaclass=jsii.JSIIMeta, jsii_type="constructs-tokens-staging.Token"):
    """Represents a special or lazily-evaluated value.

    Can be used to delay evaluation of a certain value in case, for example,
    that it requires some context or late-bound data. Can also be used to
    mark values that need special processing at document rendering time.

    Tokens can be embedded into strings while retaining their original
    semantics.
    """

    @jsii.member(jsii_name="asAny")
    @builtins.classmethod
    def as_any(cls, value: typing.Any) -> "IResolvable":
        """Return a resolvable representation of the given value.

        :param value: -
        """
        return jsii.sinvoke(cls, "asAny", [value])

    @jsii.member(jsii_name="asList")
    @builtins.classmethod
    def as_list(
        cls, value: typing.Any, *, display_hint: typing.Optional[str] = None
    ) -> typing.List[str]:
        """Return a reversible list representation of this token.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asList", [value, options])

    @jsii.member(jsii_name="asNumber")
    @builtins.classmethod
    def as_number(cls, value: typing.Any) -> jsii.Number:
        """Return a reversible number representation of this token.

        :param value: -
        """
        return jsii.sinvoke(cls, "asNumber", [value])

    @jsii.member(jsii_name="asString")
    @builtins.classmethod
    def as_string(
        cls, value: typing.Any, *, display_hint: typing.Optional[str] = None
    ) -> str:
        """Return a reversible string representation of this token.

        If the Token is initialized with a literal, the stringified value of the
        literal is returned. Otherwise, a special quoted string representation
        of the Token is returned that can be embedded into other strings.

        Strings with quoted Tokens in them can be restored back into
        complex values with the Tokens restored by calling ``resolve()``
        on the string.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asString", [value, options])

    @jsii.member(jsii_name="isUnresolved")
    @builtins.classmethod
    def is_unresolved(cls, obj: typing.Any) -> bool:
        """Returns true if obj represents an unresolved value.

        One of these must be true:

        - ``obj`` is an IResolvable
        - ``obj`` is a string containing at least one encoded ``IResolvable``
        - ``obj`` is either an encoded number or list

        This does NOT recurse into lists or objects to see if they
        containing resolvables.

        :param obj: The object to test.
        """
        return jsii.sinvoke(cls, "isUnresolved", [obj])


class Tokenization(
    metaclass=jsii.JSIIMeta, jsii_type="constructs-tokens-staging.Tokenization"
):
    """Less oft-needed functions to manipulate Tokens."""

    @jsii.member(jsii_name="isResolvable")
    @builtins.classmethod
    def is_resolvable(cls, obj: typing.Any) -> bool:
        """Return whether the given object is an IResolvable object.

        This is different from Token.isUnresolved() which will also check for
        encoded Tokens, whereas this method will only do a type check on the given
        object.

        :param obj: -
        """
        return jsii.sinvoke(cls, "isResolvable", [obj])

    @jsii.member(jsii_name="resolve")
    @builtins.classmethod
    def resolve(
        cls,
        obj: typing.Any,
        *,
        resolver: "ITokenResolver",
        scope: constructs.IConstruct,
        preparing: typing.Optional[bool] = None,
    ) -> typing.Any:
        """Resolves an object by evaluating all tokens and removing any undefined or empty objects or arrays.

        Values can only be primitives, arrays or tokens. Other objects (i.e. with methods) will be rejected.

        :param obj: The object to resolve.
        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false
        """
        options = ResolveOptions(resolver=resolver, scope=scope, preparing=preparing)

        return jsii.sinvoke(cls, "resolve", [obj, options])

    @jsii.member(jsii_name="reverseList")
    @builtins.classmethod
    def reverse_list(cls, l: typing.List[str]) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a list.

        :param l: -
        """
        return jsii.sinvoke(cls, "reverseList", [l])

    @jsii.member(jsii_name="reverseNumber")
    @builtins.classmethod
    def reverse_number(cls, n: jsii.Number) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a number.

        :param n: -
        """
        return jsii.sinvoke(cls, "reverseNumber", [n])

    @jsii.member(jsii_name="reverseString")
    @builtins.classmethod
    def reverse_string(cls, s: str) -> "TokenizedStringFragments":
        """Un-encode a string potentially containing encoded tokens.

        :param s: -
        """
        return jsii.sinvoke(cls, "reverseString", [s])

    @jsii.member(jsii_name="stringifyNumber")
    @builtins.classmethod
    def stringify_number(cls, x: jsii.Number) -> str:
        """Stringify a number directly or lazily if it's a Token.

        If it is an object (i.e., { Ref: 'SomeLogicalId' }), return it as-is.

        :param x: -
        """
        return jsii.sinvoke(cls, "stringifyNumber", [x])


class TokenizedStringFragments(
    metaclass=jsii.JSIIMeta,
    jsii_type="constructs-tokens-staging.TokenizedStringFragments",
):
    """Fragments of a concatenated string containing stringified Tokens.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        jsii.create(TokenizedStringFragments, self, [])

    @jsii.member(jsii_name="addIntrinsic")
    def add_intrinsic(self, value: typing.Any) -> None:
        """Adds an intrinsic fragment.

        :param value: the intrinsic value to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addIntrinsic", [value])

    @jsii.member(jsii_name="addLiteral")
    def add_literal(self, lit: typing.Any) -> None:
        """Adds a literal fragment.

        :param lit: the literal to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addLiteral", [lit])

    @jsii.member(jsii_name="addToken")
    def add_token(self, token: "IResolvable") -> None:
        """Adds a token fragment.

        :param token: the token to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToken", [token])

    @jsii.member(jsii_name="join")
    def join(self, concat: "IFragmentConcatenator") -> typing.Any:
        """Combine the string fragments using the given joiner.

        If there are any

        :param concat: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [concat])

    @jsii.member(jsii_name="mapTokens")
    def map_tokens(self, mapper: "ITokenMapper") -> "TokenizedStringFragments":
        """Apply a transformation function to all tokens in the string.

        :param mapper: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapTokens", [mapper])

    @builtins.property
    @jsii.member(jsii_name="firstValue")
    def first_value(self) -> typing.Any:
        """Returns the first value.

        stability
        :stability: experimental
        """
        return jsii.get(self, "firstValue")

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        """Returns the number of fragments.

        stability
        :stability: experimental
        """
        return jsii.get(self, "length")

    @builtins.property
    @jsii.member(jsii_name="tokens")
    def tokens(self) -> typing.List["IResolvable"]:
        """Return all Tokens from this string.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tokens")

    @builtins.property
    @jsii.member(jsii_name="firstToken")
    def first_token(self) -> typing.Optional["IResolvable"]:
        """Returns the first token.

        stability
        :stability: experimental
        """
        return jsii.get(self, "firstToken")


@jsii.implements(ITokenResolver)
class DefaultTokenResolver(
    metaclass=jsii.JSIIMeta, jsii_type="constructs-tokens-staging.DefaultTokenResolver"
):
    """Default resolver implementation.

    stability
    :stability: experimental
    """

    def __init__(self, concat: "IFragmentConcatenator") -> None:
        """
        :param concat: -

        stability
        :stability: experimental
        """
        jsii.create(DefaultTokenResolver, self, [concat])

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self, xs: typing.List[str], context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a tokenized list.

        :param xs: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [xs, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self, fragments: "TokenizedStringFragments", context: "IResolveContext"
    ) -> typing.Any:
        """Resolve string fragments to Tokens.

        :param fragments: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [fragments, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: "IResolvable",
        context: "IResolveContext",
        post_processor: "IPostProcessor",
    ) -> typing.Any:
        """Default Token resolution.

        Resolve the Token, recurse into whatever it returns,
        then finally post-process it.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


__all__ = [
    "DefaultTokenResolver",
    "EncodingOptions",
    "IAnyProducer",
    "IFragmentConcatenator",
    "IListProducer",
    "INumberProducer",
    "IPostProcessor",
    "IResolvable",
    "IResolveContext",
    "IStringProducer",
    "ITokenMapper",
    "ITokenResolver",
    "Lazy",
    "LazyAnyValueOptions",
    "LazyListValueOptions",
    "LazyStringValueOptions",
    "ResolveOptions",
    "StringConcat",
    "Token",
    "Tokenization",
    "TokenizedStringFragments",
]

publication.publish()
