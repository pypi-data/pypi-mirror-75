"""This is a somewhat delicate package. It contains all registered components
and preconfigured templates.

Hence, it imports all of the components. To avoid cycles, no component should
import this in module scope."""

from typing import Any
from typing import Optional
from typing import Text
from typing import Type

# Classes of all known components. If a new component should be added,
# its class name should be listed here.
component_classes = [
]

# Mapping from a components name to its class to allow name based lookup.
registered_components = {c.my_name: c for c in component_classes}


def class_from_module_path(module_path):
    """Given the module name and path of a class, tries to retrieve the class.

    The loaded class can be used to instantiate new objects. """
    import importlib

    # load the module, will raise ImportError if module cannot be loaded
    if "." in module_path:
        module_name, _, class_name = module_path.rpartition('.')

        m = importlib.import_module(module_name)
        # get the class, will raise AttributeError if class cannot be found
        return getattr(m, class_name)
    else:
        return globals()[module_path]


def get_component_class(component_name):
    # type: (Text) -> Optional[Type[Component]]
    """Resolve component name to a registered components class."""
    if component_name not in registered_components:
        try:
            return class_from_module_path(component_name)
        except Exception:
            raise Exception(
                "Failed to find component class for '{}'. Unknown "
                "component name. Check your configured pipeline and make "
                "sure the mentioned component is not misspelled. If you "
                "are creating your own component, make sure it is either "
                "listed as part of the `component_classes` in "
                "`kolibti.modulesy.py` or is a proper name of a class "
                "in a module.".format(component_name))
    return registered_components[component_name]


def load_component_by_name(component_name, model_dir, metadata, cached_component, **kwargs):
    """Resolves a component and calls its load method to init it based on a
    previously persisted model."""

    component_clz = get_component_class(component_name)
    return component_clz.load(model_dir, metadata, cached_component, **kwargs)


def create_component_by_name(component_name, config):
    """Resolves a component and calls it's create method to init it based on a
    previously persisted model."""

    component_clz = get_component_class(component_name)
    return component_clz.create(config)


def module_path_from_instance(inst):
    # type: (Any) -> Text
    """Return the module path of an instances class."""
    return inst.__module__ + "." + inst.__class__.__name__


def all_subclasses(cls):
    # type: (Any) -> List[Any]
    """Returns all known (imported) subclasses of a class."""

    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in all_subclasses(s)]


def register_component(Component):
    component_classes.append(Component)
    global registered_components
    registered_components = {c.name: c for c in component_classes}
