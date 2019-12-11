from testing_framework import testing
from pathlib import Path

src_dir = Path.joinpath(Path(__file__).parent)
out_dir = Path.joinpath(Path(__file__).parent, "../../reports/")
testing.start(str(src_dir), str(out_dir))