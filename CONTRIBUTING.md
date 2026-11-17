# Contributing

Open an issue for an unclear proof step, a reproducibility problem or a proposed
extension. Include the release/commit, Python version, exact command and relevant
error. Avoid uploading credentials or private environment files.

For code changes, run `python -m unittest discover -s tests -v`. Preserve exact
Fraction-based checks and add a literal regression test for a corrected numerical
or optimizer-update bug. Keep finite-horizon demonstrations separate from saved
paper results. Never replace frozen observations or manifests to make a check pass.

Paper and research changes need an explicit statement of what claim changed and
what evidence supports it. Internal software tests do not replace mathematical
review or establish stationarity. Corrections to a frozen release should receive
a new version and a documented explanation, retaining the prior record.
