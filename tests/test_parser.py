from pathlib import Path
from types import SimpleNamespace

from pptx2md.parser import parse
from pptx2md.types import ConversionConfig


def test_parse_skips_notes_slide_without_text_frame():
    slide = SimpleNamespace(
        shapes=[],
        has_notes_slide=True,
        notes_slide=SimpleNamespace(notes_text_frame=None),
    )
    prs = SimpleNamespace(slides=[slide])
    config = ConversionConfig(
        pptx_path=Path("deck.pptx"),
        output_path=Path("out.md"),
        image_dir=Path("img"),
    )

    result = parse(config, prs)

    assert len(result.slides) == 1
    assert result.slides[0].notes == []
