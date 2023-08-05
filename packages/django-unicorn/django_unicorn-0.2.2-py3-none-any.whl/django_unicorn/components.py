import hmac
import importlib
import inspect
import uuid

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.response import TemplateResponse
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView

import orjson
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter


# Module cache to reduce initialization costs
views_cache = {}
constructed_views_cache = {}


class ComponentNotFoundError(Exception):
    pass


class UnsortedAttributes(HTMLFormatter):
    """
    Prevent beautifulsoup from re-ordering attributes.
    """

    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


def convert_to_snake_case(s):
    # TODO: Better handling of dash->snake
    return s.replace("-", "_")


def convert_to_camel_case(s):
    # TODO: Better handling of dash/snake->camel-case
    s = convert_to_snake_case(s)
    return "".join(word.title() for word in s.split("_"))


class UnicornTemplateResponse(TemplateResponse):
    def __init__(
        self,
        template,
        request,
        context=None,
        content_type=None,
        status=None,
        charset=None,
        using=None,
        component_name=None,
        component_id=None,
        frontend_context_variables={},
        init_js=False,
        **kwargs,
    ):
        super().__init__(
            template=template,
            request=request,
            context=context,
            content_type=content_type,
            status=status,
            charset=charset,
            using=using,
        )

        self.component_id = component_id
        self.component_name = component_name
        self.frontend_context_variables = frontend_context_variables
        self.init_js = init_js

    def render(self):
        response = super().render()

        if not self.component_id:
            return response

        content = response.content.decode("utf-8")

        checksum = hmac.new(
            str.encode(settings.SECRET_KEY),
            str.encode(str(self.frontend_context_variables)),
            digestmod="sha256",
        ).hexdigest()

        soup = BeautifulSoup(content, features="html.parser")
        root_element = UnicornTemplateResponse._get_root_element(soup)
        root_element["unicorn:id"] = self.component_id
        root_element["unicorn:checksum"] = checksum

        if self.init_js:
            script = soup.new_tag("script")
            init = {
                "id": self.component_id,
                "name": self.component_name,
            }
            init = orjson.dumps(init).decode("utf-8")
            script.string = f"Unicorn.setData({self.frontend_context_variables}); Unicorn.componentInit({init});"
            root_element.insert_after(script)

        rendered_template = UnicornTemplateResponse._desoupify(soup)
        rendered_template = mark_safe(rendered_template)

        response.content = rendered_template
        return response

    @staticmethod
    def _get_root_element(soup):
        for element in soup.contents:
            if element.name and element.name == "div":
                return element

        raise Exception("No root element found")

    @staticmethod
    def _desoupify(soup):
        soup.smooth()
        return soup.encode(formatter=UnsortedAttributes()).decode("utf-8")


class UnicornView(TemplateView):
    response_class = UnicornTemplateResponse
    request = None

    # Caches to reduce the amount of time introspecting the class
    _methods_cache = None
    _attribute_name_cache = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        assert self.component_name, "Component name is required"

        if "component_id" not in kwargs or not kwargs["component_id"]:
            self.component_id = str(uuid.uuid4())

        if "request" in kwargs:
            self.setup(kwargs["request"])

        self._set_default_template_name()
        self._set_caches()

    def _set_default_template_name(self):
        get_template_names_is_valid = False

        try:
            # Check for get_template_names by explicitly calling it since it
            # is defined in TemplateResponseMixin, but throws ImproperlyConfigured.
            self.get_template_names()
            get_template_names_is_valid = True
        except ImproperlyConfigured:
            pass

        if not self.template_name and not get_template_names_is_valid:
            self.template_name = f"unicorn/{self.component_name}.html"

    def _set_caches(self):
        self._methods_cache = self._methods()
        self._attribute_names_cache = self._attribute_names()

    def render(self, init_js=False):
        frontend_context_variables = self.get_frontend_context_variables()

        response = self.render_to_response(
            context=self.get_context_data(),
            component_name=self.component_name,
            component_id=self.component_id,
            frontend_context_variables=frontend_context_variables,
            init_js=init_js,
        )

        response.render()
        rendered_component = response.content.decode("utf-8")

        return rendered_component

    def get_frontend_context_variables(self):
        frontend_context_variables = {}
        frontend_context_variables.update(self._attributes())
        frontend_context_variables = orjson.dumps(frontend_context_variables).decode(
            "utf-8"
        )

        return frontend_context_variables

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self._attributes())
        context.update(self._methods())

        return context

    def _attribute_names(self):
        non_callables = [
            member[0] for member in inspect.getmembers(self, lambda x: not callable(x))
        ]
        attribute_names = [name for name in non_callables if self._is_public(name)]

        return attribute_names

    def _attributes(self):
        """
        Get attributes that can be called in the component.
        """

        attribute_names = self._attribute_names_cache
        attributes = {}

        for attribute_name in attribute_names:
            attributes[attribute_name] = object.__getattribute__(self, attribute_name)

        return attributes

    def _methods(self):
        """
        Get methods that can be called in the component.
        """

        if self._methods_cache:
            return self._methods_cache

        member_methods = inspect.getmembers(self, inspect.ismethod)
        public_methods = [
            method for method in member_methods if self._is_public(method[0])
        ]
        methods = {k: v for (k, v) in public_methods}
        self._methods_cache = methods

        return methods

    def _is_public(self, name):
        """
        Determines if the name should be sent in the context.
        """

        # Ignore some standard attributes from TemplateVIew
        protected_names = (
            "render",
            "request",
            "args",
            "kwargs",
            "content_type",
            "extra_context",
            "http_method_names",
            "template_engine",
            "template_name",
            "id",
            "component_id",
            "component_name",
        )
        excludes = []

        if hasattr(self, "Meta") and hasattr(self.Meta, "exclude"):
            excludes = self.Meta.exclude

        return not (name.startswith("_") or name in protected_names or name in excludes)

    @staticmethod
    def create(component_name, component_id=None):
        if component_id:
            key = f"{component_name}-{component_id}"

            if key in constructed_views_cache:
                return constructed_views_cache[key]

        if component_name in views_cache:
            component = views_cache[component_name](
                component_name=component_name, component_id=component_id
            )

            if component_id:
                key = f"{component_name}-{component_id}"
                constructed_views_cache[key] = component

            return component

        locations = []

        def _get_component_class(module_name, class_name):
            module = importlib.import_module(module_name)
            component_class = getattr(module, class_name)

            return component_class

        if "." in component_name:
            class_name = component_name.split(".")[-1:][0]
            module_name = component_name.replace("." + class_name, "")
            locations.append((class_name, module_name))
        else:
            class_name = convert_to_camel_case(component_name)
            class_name = f"{class_name}View"

            module_name = convert_to_snake_case(component_name)
            module_name = f"unicorn.components.{module_name}"
            locations.append((class_name, module_name))

        # TODO: django.conf setting that has locations for where to look for components
        # TODO: django.conf setting bool that defines whether look in all installed apps for components

        # Store the last exception that got raised while looking for a component in case it is useful context
        last_exception = None

        for (class_name, module_name) in locations:
            try:
                component_class = _get_component_class(module_name, class_name)
                component = component_class(component_name=component_name, id=None)

                views_cache[component_name] = component_class

                if component_id:
                    constructed_views_cache[
                        f"{component_name}-{component_id}"
                    ] = component

                return component
            except ModuleNotFoundError as e:
                last_exception = e
            except AttributeError as e:
                last_exception = e

        raise ComponentNotFoundError(
            f"'{component_name}' component could not be found."
        ) from last_exception
