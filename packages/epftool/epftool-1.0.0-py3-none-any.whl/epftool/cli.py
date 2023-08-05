import codecs
import json
import os
import sqlite3
import click
from tqdm import tqdm
__version__ = "1.0.0"
sep = chr(1)


def parse_epf(path, dbname, c, id, function, multiple=False):
    dbfile = os.path.join(path, dbname)
    if not os.path.isfile(dbfile):
        print(dbfile, "file not found.")
        return
    positions = []
    if multiple:
        for row in c.execute("SELECT * FROM " + dbname + " WHERE id2=?", (id,)):
            positions.append(row[2])
    else:
        c.execute("SELECT * FROM " + dbname + " WHERE id=?", (id,))
        row = c.fetchone()
        if row is not None:
            positions.append(row[1])
    data_found = []
    if len(positions) > 0:
        with open(dbfile, "rb") as f:
            for position in positions:
                f.seek(position)
                line = f.readline().decode("utf-8")
                fields = line.rstrip("\n\u0002").split(sep)
                data_found.append(function(fields))
    return data_found


def index_epf(path, dbname, function, c, statement):
    dbfile = os.path.join(path, dbname)
    if not os.path.isfile(dbfile):
        print(dbfile, "file not found.")
        return
    dbsize = os.path.getsize(dbfile)
    prog = tqdm(desc="Indexing " + dbname, total=dbsize)
    with open(dbfile, "rb") as f:
        while True:
            pos = f.tell()
            line = f.readline().decode("utf-8")
            if line == '':
                prog.close()
                break
            prog.update(len(line))
            if line[0] == "#":
                continue
            fields = line.rstrip("\n\u0002").split(sep)
            if len(fields) == 1:
                continue
            function(fields, pos, c, statement)
    prog.close()


def get_upc(fields):
    ret = {"upc": fields[2]}
    if len(fields) > 3:
        ret["amg_album_id"] = fields[3]
    return ret


def get_collection(fields):
    artwork_big = fields[8].split("/")
    artwork_idx = len(artwork_big) - 1
    artwork_big[artwork_idx] = "10000x10000." + artwork_big[artwork_idx].split(".")[1]
    return {"collection_id": fields[1],
            "name": fields[2],
            "title_version": fields[3],
            "search_terms": fields[4],
            "parental_advisory_id": fields[5],
            "artist_display_name": fields[6],
            "view_url": fields[7],
            "artwork_url": fields[8],
            "artwork_url_big": "/".join(artwork_big),
            "original_release_date": fields[9],
            "itunes_release_date": fields[10],
            "label_studio": fields[11],
            "content_provider": fields[12],
            "copyright": fields[13],
            "pline": fields[14],
            "media_type_id": fields[15],
            "is_compilation": fields[16],
            "collection_type_id": fields[17]
            }


def get_collection_song(fields):
    return {"song_id": fields[2],
            "track_number": int(fields[3]),
            "volume_number": int(fields[4])
            }


def get_song_match(fields):
    return {"song_id": fields[1],
            "isrc": fields[2],
            "amg_track_id": fields[3]
            }


def get_artist(fields):
    return {"artist_id": fields[1],
            "name": fields[2],
            "view_url": fields[4]
            }


def index_single(fields, pos, c, statement):
    try:
        c.execute(statement, (fields[1], pos))
    except sqlite3.IntegrityError:
        pass


def index_many(fields, pos, c, statement):
    try:
        c.execute(statement, (fields[2], fields[1], pos))
    except sqlite3.IntegrityError:
        pass


def write_output(data):
    with codecs.open("output.txt", "w", "utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


@click.group(no_args_is_help=True)
def cli_group():
    pass


@click.command()
@click.argument("albumid")
@click.option("--path", default="", help="Path for the db files.")
def upc(albumid, path):
    conn = sqlite3.connect("index.db")
    c = conn.cursor()
    data = parse_epf(path, "collection_match", c, albumid, get_upc)
    if len(data):
        print("Found!", data[0])
    else:
        print("Not found :(")
    conn.close()


@click.command()
@click.argument("albumid")
@click.option("--path", default="", help="Path for the db files.")
def album(albumid, path):
    conn = sqlite3.connect("index.db")
    c = conn.cursor()
    print("Searching collection...")
    upc_data = parse_epf(path, "collection_match", c, albumid, get_upc)
    collection_data = parse_epf(path, "collection", c, albumid, get_collection)
    data = {**upc_data[0], **collection_data[0]}
    conn.close()
    write_output(data)
    print("Done!")


@click.command()
@click.argument("albumid")
@click.option("--path", default="", help="Path for the db files.")
@click.option('--artists', default=False, is_flag=True, help="Include track artists.")
def tracks(albumid, path, artists):
    conn = sqlite3.connect("index.db")
    c = conn.cursor()
    print("Searching collection...")
    upc_data = parse_epf(path, "collection_match", c, albumid, get_upc)
    collection_data = parse_epf(path, "collection", c, albumid, get_collection)
    data = {**upc_data[0], **collection_data[0]}
    print("Searching songs...")
    collection_song_data = parse_epf(path, "collection_song", c, albumid, get_collection_song, True)
    collection_song_data = sorted(collection_song_data, key=lambda i: (i["volume_number"], i["track_number"]))
    songids = []
    for collection_song in collection_song_data:
        songids.append(collection_song["song_id"])
    data["songs"] = []
    print("Searching song data...")
    for collection_song in collection_song_data:
        song_match_data = parse_epf(path, "song_match", c, collection_song["song_id"], get_song_match)[0]
        song_data = {**collection_song, **song_match_data}
        if artists:
            artistsids = []
            for row in c.execute("SELECT * FROM artist_song WHERE id=?", (collection_song["song_id"],)):
                artistsids.append(row[1])
            if len(artistsids) > 0:
                song_data["artists"] = []
                for artistid in artistsids:
                    song_data["artists"].append(parse_epf(path, "artist", c, artistid, get_artist))
        data["songs"].append(song_data)
    conn.close()
    write_output(data)
    print("Done!")


@click.command()
@click.option("--path", default="", help="Path for the db files.")
@click.option('--upc', default=False, is_flag=True, help="Index the collection_match file.")
@click.option('--album', default=False, is_flag=True, help="Index the collection file.")
@click.option('--tracks', default=False, is_flag=True, help="Index the song_match and collection_song files.")
@click.option('--artists', default=False, is_flag=True, help="Index the artist and artist_song files.")
def index(path, upc, album, tracks, artists):
    all = not upc and not album and not tracks and not artists
    conn = sqlite3.connect("index.db")
    c = conn.cursor()
    if all or upc:
        c.execute("DROP TABLE IF EXISTS collection_match;")
        c.execute("CREATE TABLE collection_match (id BIGINT PRIMARY KEY, pos BIGINT);")
        index_epf(path, "collection_match", index_single, c, "INSERT INTO collection_match VALUES (?,?);")
        conn.commit()
    if all or album:
        c.execute("DROP TABLE IF EXISTS collection;")
        c.execute("CREATE TABLE collection (id BIGINT PRIMARY KEY, pos BIGINT);")
        index_epf(path, "collection", index_single, c, "INSERT INTO collection VALUES (?,?);")
        conn.commit()
    if all or tracks:
        c.execute("DROP TABLE IF EXISTS song_match;")
        c.execute("CREATE TABLE song_match (id BIGINT PRIMARY KEY, pos BIGINT);")
        index_epf(path, "song_match", index_single, c, "INSERT INTO song_match VALUES (?,?);")
        conn.commit()
        c.execute("DROP TABLE IF EXISTS collection_song;")
        c.execute("CREATE TABLE collection_song (id BIGINT PRIMARY KEY, id2 BIGINT, pos BIGINT);")
        c.execute("CREATE INDEX collection_song_id2_IDX ON collection_song (id2);")
        index_epf(path, "collection_song", index_many, c, "INSERT INTO collection_song VALUES (?,?,?);")
        conn.commit()
    if all or artists:
        c.execute("DROP TABLE IF EXISTS artist;")
        c.execute("CREATE TABLE artist (id BIGINT PRIMARY KEY, pos BIGINT);")
        index_epf(path, "artist", index_single, c, "INSERT INTO artist VALUES (?,?);")
        conn.commit()
        c.execute("DROP TABLE IF EXISTS artist_song;")
        c.execute("CREATE TABLE artist_song (id BIGINT, id2 BIGINT, pos BIGINT);")
        c.execute("CREATE INDEX artist_song_id_IDX ON artist_song (id);")
        index_epf(path, "artist_song", index_many, c, "INSERT INTO artist_song VALUES (?,?,?);")
        conn.commit()
    conn.close()


cli_group.add_command(upc)
cli_group.add_command(album)
cli_group.add_command(tracks)
cli_group.add_command(index)


def main():
    click.echo("epftool version " + __version__)
    cli_group()
