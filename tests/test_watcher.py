import pytest
from watcher import get_latest_patch, create_snapshot



def test_get_latest_patch():
    fake_data = {
        "patches": [
            {
                "is_latest": False,
                "version": "01.56"
            },
            {
                "is_latest": True,
                "version": "01.57"
            }
        ]
    }

    result = get_latest_patch(fake_data)

    assert result["version"] == "01.57"

def test_create_snapshot():
    patch = {
        "is_latest": True,
        "version": "01.57",
        "filesize": "49.3GB",
        "required_firmware": "13.52",
        "creation_date": "2026-07-09",
        "changelog_preview": "The Kortz Center Heist update.",
        "changelog_charcount": 111,
        "keyset": {
            "patch": "abc",
            "details": "def",
            "changeinfo": "ghi"
        }
    }

    result = create_snapshot(patch)

    assert result == {
        "version": "01.57",
        "filesize": "49.3GB",
        "required_firmware": "13.52",
        "creation_date": "2026-07-09",
        "changelog_preview": "The Kortz Center Heist update."
    }
    
def test_get_latestpatch_raises_error_when_missing():
    fake_data = {
        "patches": [
            {
                "is_latest": False,
                "version": "01.56"
            }
        ]
    }
    with pytest.raises(ValueError):
        get_latest_patch(fake_data)