from phoenix4all.net.http import fetch_listing


def test_fetch_listing():
    cwd, files = fetch_listing("http://httpredir.debian.org/debian/")
    assert isinstance(files, list)
    assert len(files) > 0
