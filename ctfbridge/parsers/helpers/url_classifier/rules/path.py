from ..utils import LinkClassifierContext


def is_root_path(ctx: LinkClassifierContext) -> bool:
    return (
        ctx.parsed.path in ["", "/"]
        and not ctx.parsed.params
        and not ctx.parsed.query
        and not ctx.parsed.fragment
    )
