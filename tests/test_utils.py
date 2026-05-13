from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from pptx2md.utils import fix_null_rels


def _write_pptx_with_null_relationship(path: Path) -> None:
    with ZipFile(path, "w", ZIP_DEFLATED) as zf:
        zf.writestr(
            "ppt/_rels/presentation.xml.rels",
            '<Relationships><Relationship Id="rId1" Target="NULL"/></Relationships>',
        )
        zf.writestr("[Content_Types].xml", "<Types/>")


def test_fix_null_rels_uses_unique_temporary_outputs(tmp_path):
    source = tmp_path / "deck.pptx"
    _write_pptx_with_null_relationship(source)

    first = Path(fix_null_rels(source))
    second = Path(fix_null_rels(source))

    try:
        assert first != second
        assert first.exists()
        assert second.exists()
        assert not (tmp_path / "deck_purged.pptx").exists()
    finally:
        first.unlink(missing_ok=True)
        second.unlink(missing_ok=True)
