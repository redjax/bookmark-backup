# Bookmarks Backup

A bookmarks backup/restore tool.

Detects the host's platform & dynamically builds path to bookmarks file, offering a CLI interface for backing up/restoring a browser's bookmarks store.

As of now, only Chromium-based browsers are supported.

## Supported browsers

- Google Chrome
- Vivaldi
- Microsoft Edge

## Usage

```shell
python -m bookmark_backup --help
```

With `uv`:

```shell
uv run bookmark-backup --help
```
