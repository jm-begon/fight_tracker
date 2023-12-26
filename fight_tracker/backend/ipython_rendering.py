from ..encounter import Encounter
from ..rendering import Renderer, StreamRenderer
from ..statblock import StatBlock


def override_ip_repr_encounter(renderer: Renderer | None = None) -> None:
    from IPython.core.formatters import BaseFormatter  # type: ignore

    if renderer is None:
        renderer = StreamRenderer()

    class EncounterFormatter(BaseFormatter):
        def __call__(self, __o, *args, **kwargs):
            renderer << __o
            return None

    ip = get_ipython()  # type: ignore
    ip.display_formatter.formatters["text/plain"].for_type(
        Encounter, EncounterFormatter()
    )


def override_ip_repr(renderer: Renderer | None = None) -> None:
    from IPython.core.formatters import BaseFormatter  # type: ignore

    if renderer is None:
        renderer = StreamRenderer()

    class RendererFormatter(BaseFormatter):
        def __call__(self, __o, *args, **kwargs):
            renderer(__o)
            return None

    ip = get_ipython()  # type: ignore
    for class_to_render in (
        Encounter,
        StatBlock,
    ):
        ip.display_formatter.formatters["text/plain"].for_type(
            class_to_render, RendererFormatter()
        )
