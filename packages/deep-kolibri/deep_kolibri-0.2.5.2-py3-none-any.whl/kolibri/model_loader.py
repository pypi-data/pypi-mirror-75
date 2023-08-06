import logging
from typing import Optional

from kolibri import kolibri_component
from kolibri import version as ver
from kolibri.document import Document
from kolibri.metadata import Metadata
from kolibri.pipeline import Pipeline
from .errors import *
from .kolibri_component import ComponentBuilder

logger = logging.getLogger(__name__)

MINIMUM_COMPATIBLE_VERSION = "0.0.1"


class ModelLoader(object):
    """Use a trained pipeline of components to parse text documents."""

    # Defines all attributes (& default values)
    # that will be returned by `parse`
    @staticmethod
    def default_output_attributes():
        return {"label": {"name": None, "confidence": 0.0}, "entities": []}

    @staticmethod
    def ensure_model_compatibility(metadata, version_to_check=None):
        from packaging import version

        if version_to_check is None:
            version_to_check = MINIMUM_COMPATIBLE_VERSION

        model_version = metadata.get("kolibri_nlu_version", "0.0.0")
        if version.parse(model_version) < version.parse(version_to_check):
            raise UnsupportedModelError(
                "The model version is to old to be "
                "loaded by this nlp instance. "
                "Either retrain the model, or run with"
                "an older version. "
                "Model version: {} Instance version: {}"
                "".format(model_version, ver.__version__))

    @staticmethod
    def load(model_dir, component_builder=None, skip_validation=False):
        """Create an interpreter based on a persisted model.

        Args:
            model_dir (str): The path of the model to load
            component_builder (ComponentBuilder): The
                :class:`ComponentBuilder` to use.

        Returns:
            ModelLoader: An interpreter that uses the loaded model.
        """

        model_metadata = Metadata.load(model_dir)

        ModelLoader.ensure_model_compatibility(model_metadata)
        return ModelLoader.create(model_metadata,
                                  component_builder,
                                  skip_validation)

    @staticmethod
    def create(model_metadata,  # type: Metadata
               component_builder=None,  # type: Optional[ComponentBuilder]
               skip_validation=False  # type: bool
               ):
        # type: (...) -> ModelLoader
        """Load stored model and components defined by the provided metadata."""

        context = {}

        if component_builder is None:
            # If no builder is passed, every interpreter creation will result
            # in a new builder. hence, no components are reused.
            component_builder = kolibri_component.ComponentBuilder()

        steps = []

        # Before instantiating the component classes,
        # lets check if all required packages are available
        if not skip_validation:
            kolibri_component.validate_requirements(model_metadata.component_classes)

        for component_name in model_metadata.component_classes:
            component = component_builder.load_component(
                component_name, model_metadata.model_dir,
                model_metadata, **context)
            try:
                updates = component.provide_context()
                if updates:
                    context.update(updates)
                steps.append((component.name, component))
            except kolibri_component.MissingArgumentError as e:
                raise Exception("Failed to initialize component '{}'. "
                                "{}".format(component.name, e))

        return ModelLoader(Pipeline(steps), context, model_metadata)

    def __init__(self, pipeline: Pipeline, context, model_metadata=None):
        """

        :type pipeline: Pipeline
        """
        self.pipeline = pipeline
        self.context = context if context is not None else {}
        self.model_metadata = model_metadata

    def predict(self, text):
        """Predict the input text, classify it and return pipeline result.

        The pipeline result usually contains intent and entities."""

        if text is None:
            # Not all components are able to handle empty strings. So we need
            # to prevent that... This default return will not contain all
            # output attributes of all components, but in the end, no one
            # should pass an empty string in the first place.
            output = self.default_output_attributes()
            output["text"] = ""
            return output

        return self.pipeline.predict(text)

    def process(self, text, time=None, only_output_properties=True):
        """Predict the input text, classify it and return pipeline result.

        The pipeline result usually contains intent and entities."""

        if not text:
            # Not all components are able to handle empty strings. So we need
            # to prevent that... This default return will not contain all
            # output attributes of all components, but in the end, no one
            # should pass an empty string in the first place.
            output = self.default_output_attributes()
            output["text"] = ""
            return output

        document = Document(**{'text':text, 'default_output_attributes': self.default_output_attributes(), 'time':time})

        self.pipeline.process(document, **self.context)

        output = self.default_output_attributes()
        output.update(document.as_dict(
            only_output_properties=only_output_properties))

        return output

    def get_component(self, component):
        for c in self.pipeline.components:
            if c.my_name == component:
                return c

        return None
