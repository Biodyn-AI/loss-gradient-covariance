# Third-party notices

The bibliography and literature-validation records identify external scholarly
works; their copyrights remain with their authors/publishers.

`paper/spmpsci.bst` is the publisher-supplied style with its original LPPL
version 1-or-later notice. `paper/jota_spmpsci.bst` is a locally renamed variant
that only comments a malformed upstream provenance line; formatting functions
are unchanged. Both retain their upstream notices.

The Springer `svjour3.cls` and `svglov3.clo` files are not relicensed or tracked
here. The paper build downloads the official author template, verifies its
recorded SHA-256, and extracts those two files locally. Its provenance is in
`paper/fetch_template.py`. Retain publisher terms when using those files.

NumPy, Matplotlib, SciPy and other separately installed dependencies retain
their own licenses. No dependency binaries are vendored in this repository.
