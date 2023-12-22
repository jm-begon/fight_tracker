from ..encounter import Encounter
from ..rendering import Renderer, StreamRenderer


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
