from typing import Any, Optional, Union

from pydantic import BaseModel, Field

from invokeai.app.invocations.baseinvocation import (
    BaseInvocation,
    BaseInvocationOutput,
    FieldDescriptions,
    InputField,
    InvocationContext,
    OutputField,
    UIType,
    invocation,
    invocation_output,
)
from invokeai.app.invocations.controlnet_image_processors import ControlField
from invokeai.app.invocations.model import LoRAModelField, MainModelField, VAEModelField
from invokeai.app.util.model_exclude_null import BaseModelExcludeNull

from ...version import __version__


class LoRAMetadataField(BaseModelExcludeNull):
    """LoRA metadata for an image generated in InvokeAI."""

    lora: LoRAModelField = Field(description="The LoRA model")
    weight: float = Field(description="The weight of the LoRA model")


class CoreMetadata(BaseModelExcludeNull):
    """Core generation metadata for an image generated in InvokeAI."""

    app_version: str = Field(default=__version__, description="The version of InvokeAI used to generate this image")
    generation_mode: str = Field(
        description="The generation mode that output this image",
    )
    created_by: Optional[str] = Field(description="The name of the creator of the image")
    positive_prompt: str = Field(description="The positive prompt parameter")
    negative_prompt: str = Field(description="The negative prompt parameter")
    width: int = Field(description="The width parameter")
    height: int = Field(description="The height parameter")
    seed: int = Field(description="The seed used for noise generation")
    rand_device: str = Field(description="The device used for random number generation")
    cfg_scale: float = Field(description="The classifier-free guidance scale parameter")
    steps: int = Field(description="The number of steps used for inference")
    scheduler: str = Field(description="The scheduler used for inference")
    clip_skip: Optional[int] = Field(
        default=None,
        description="The number of skipped CLIP layers",
    )
    model: MainModelField = Field(description="The main model used for inference")
    controlnets: list[ControlField] = Field(description="The ControlNets used for inference")
    loras: list[LoRAMetadataField] = Field(description="The LoRAs used for inference")
    vae: Optional[VAEModelField] = Field(
        default=None,
        description="The VAE used for decoding, if the main model's default was not used",
    )

    # Latents-to-Latents
    strength: Optional[float] = Field(
        default=None,
        description="The strength used for latents-to-latents",
    )
    init_image: Optional[str] = Field(default=None, description="The name of the initial image")

    # SDXL
    positive_style_prompt: Optional[str] = Field(default=None, description="The positive style prompt parameter")
    negative_style_prompt: Optional[str] = Field(default=None, description="The negative style prompt parameter")

    # SDXL Refiner
    refiner_model: Optional[MainModelField] = Field(default=None, description="The SDXL Refiner model used")
    refiner_cfg_scale: Optional[float] = Field(
        default=None,
        description="The classifier-free guidance scale parameter used for the refiner",
    )
    refiner_steps: Optional[int] = Field(default=None, description="The number of steps used for the refiner")
    refiner_scheduler: Optional[str] = Field(default=None, description="The scheduler used for the refiner")
    refiner_positive_aesthetic_score: Optional[float] = Field(
        default=None, description="The aesthetic score used for the refiner"
    )
    refiner_negative_aesthetic_score: Optional[float] = Field(
        default=None, description="The aesthetic score used for the refiner"
    )
    refiner_start: Optional[float] = Field(default=None, description="The start value used for refiner denoising")


class ImageMetadata(BaseModelExcludeNull):
    """An image's generation metadata"""

    metadata: Optional[dict] = Field(default=None, description="The metadata associated with the image")
    workflow: Optional[dict] = Field(default=None, description="The workflow associated with the image")


@invocation_output("metadata_accumulator_output")
class MetadataAccumulatorOutput(BaseInvocationOutput):
    """The output of the MetadataAccumulator node"""

    metadata: CoreMetadata = OutputField(description="The core metadata for the image")


@invocation(
    "metadata_accumulator", title="Metadata Accumulator", tags=["metadata"], category="metadata", version="1.0.0"
)
class MetadataAccumulatorInvocation(BaseInvocation):
    """Outputs a Core Metadata Object"""

    generation_mode: str = InputField(
        description="The generation mode that output this image",
    )
    positive_prompt: str = InputField(description="The positive prompt parameter")
    negative_prompt: str = InputField(description="The negative prompt parameter")
    width: int = InputField(description="The width parameter")
    height: int = InputField(description="The height parameter")
    seed: int = InputField(description="The seed used for noise generation")
    rand_device: str = InputField(description="The device used for random number generation")
    cfg_scale: float = InputField(description="The classifier-free guidance scale parameter")
    steps: int = InputField(description="The number of steps used for inference")
    scheduler: str = InputField(description="The scheduler used for inference")
    clip_skip: Optional[int] = Field(
        default=None,
        description="The number of skipped CLIP layers",
    )
    model: MainModelField = InputField(description="The main model used for inference")
    controlnets: list[ControlField] = InputField(description="The ControlNets used for inference")
    loras: list[LoRAMetadataField] = InputField(description="The LoRAs used for inference")
    strength: Optional[float] = InputField(
        default=None,
        description="The strength used for latents-to-latents",
    )
    init_image: Optional[str] = InputField(
        default=None,
        description="The name of the initial image",
    )
    vae: Optional[VAEModelField] = InputField(
        default=None,
        description="The VAE used for decoding, if the main model's default was not used",
    )

    # SDXL
    positive_style_prompt: Optional[str] = InputField(
        default=None,
        description="The positive style prompt parameter",
    )
    negative_style_prompt: Optional[str] = InputField(
        default=None,
        description="The negative style prompt parameter",
    )

    # SDXL Refiner
    refiner_model: Optional[MainModelField] = InputField(
        default=None,
        description="The SDXL Refiner model used",
    )
    refiner_cfg_scale: Optional[float] = InputField(
        default=None,
        description="The classifier-free guidance scale parameter used for the refiner",
    )
    refiner_steps: Optional[int] = InputField(
        default=None,
        description="The number of steps used for the refiner",
    )
    refiner_scheduler: Optional[str] = InputField(
        default=None,
        description="The scheduler used for the refiner",
    )
    refiner_positive_aesthetic_score: Optional[float] = InputField(
        default=None,
        description="The aesthetic score used for the refiner",
    )
    refiner_negative_aesthetic_score: Optional[float] = InputField(
        default=None,
        description="The aesthetic score used for the refiner",
    )
    refiner_start: Optional[float] = InputField(
        default=None,
        description="The start value used for refiner denoising",
    )

    def invoke(self, context: InvocationContext) -> MetadataAccumulatorOutput:
        """Collects and outputs a CoreMetadata object"""

        return MetadataAccumulatorOutput(metadata=CoreMetadata(**self.dict()))


class MetadataItem(BaseModel):
    label: str = Field(description=FieldDescriptions.metadata_item_label)
    value: Any = Field(description=FieldDescriptions.metadata_item_value)


@invocation_output("metadata_item_output")
class MetadataItemOutput(BaseInvocationOutput):
    """Metadata Item Output"""

    item: MetadataItem = OutputField(description="Metadata Item")


@invocation("metadata_item", title="Metadata Item", tags=["metadata"], category="metadata", version="1.0.0")
class MetadataItemInvocation(BaseInvocation):
    """Used to create an arbitrary metadata item. Provide "label" and make a connection to "value" to store that data as the value."""

    label: str = InputField(description=FieldDescriptions.metadata_item_label)
    value: Any = InputField(description=FieldDescriptions.metadata_item_value, ui_type=UIType.Any)

    def invoke(self, context: InvocationContext) -> MetadataItemOutput:
        return MetadataItemOutput(item=MetadataItem(label=self.label, value=self.value))


class MetadataDict(BaseModel):
    """Accepts a single MetadataItem or collection of MetadataItems (use a Collect node)."""

    data: dict[str, Any] = Field(description="Metadata dict")


@invocation_output("metadata_dict")
class MetadataDictOutput(BaseInvocationOutput):
    metadata_dict: MetadataDict = OutputField(description="Metadata Dict")


@invocation("metadata", title="Metadata", tags=["metadata"], category="metadata", version="1.0.0")
class MetadataInvocation(BaseInvocation):
    """Takes a list of MetadataItems and outputs a MetadataDict."""

    items: Union[list[MetadataItem], MetadataItem] = InputField(description=FieldDescriptions.metadata_item_polymorphic)

    def invoke(self, context: InvocationContext) -> MetadataDictOutput:
        if isinstance(self.items, MetadataItem):
            return MetadataDictOutput(metadata_dict=(MetadataDict(data={self.items.label: self.items.value})))

        return MetadataDictOutput(metadata_dict=(MetadataDict(data={item.label: item.value for item in self.items})))


@invocation("merge_metadata_dict", title="Metadata Merge", tags=["metadata"], category="metadata", version="1.0.0")
class MergeMetadataDictInvocation(BaseInvocation):
    """Takes a list of MetadataItems and outputs a MetadataDict."""

    collection: list[MetadataDict] = InputField(description=FieldDescriptions.metadata_dict_collection)

    def invoke(self, context: InvocationContext) -> MetadataDictOutput:
        data = {}
        for item in self.collection:
            data.update(item.data)

        return MetadataDictOutput(metadata_dict=MetadataDict(data=data))


class WithMetadata(BaseModel):
    metadata: Optional[MetadataDict] = InputField(default=None, description=FieldDescriptions.metadata)
