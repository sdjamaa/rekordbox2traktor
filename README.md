# Rekordbox to Traktor
Playlist converter so I can finally use my Kontrol X1 MK2 :angryface:

## Summary
Takes as an input the path of your Rekordbox playlist and generates a Traktor playlist.
Nested playlists are - for now - flattened by keeping the last level. In other words you lose your folders but keep your playlists inside.

Rekordbox can export your playlist in XML format (find out in one of the top-level menu). `nml` files are just XMLs of Traktor playlists.
## Install

Install `virtualenv`, `pip-tools`:

```commandline
pip intall virtualenv pip-tools
```

Prepare your virtual environment:
```commandline
python -m venv venv
pip-compile requirements.in
pip install -r requirements.txt
```

## Use
Launch:
```commandline
python rkdbx2trktr/__init__.py /Users/sofian/Documents/rekordbox-Jan125.xml /Users/sofian/Documents/traktor.xml
```

It takes 2 arguments:
- the path of your Rekordbox playlist
- the output path of your converted Traktor playlist

## Development notes

You can run tests by 

# Contact

Please check GitHub issues for a gist of the roadmap.

My email: sofian.djamaa@gmail.com

# Release notes

TBD