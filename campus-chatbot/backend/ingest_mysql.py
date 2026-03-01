from backend.ingest import ingest_text_file
from backend.db import insert_document, create_tables
import os


def ingest_and_record_text(filepath: str, index_path: str, source: str = None):
    # create tables if needed
    create_tables()
    vs = ingest_text_file(filepath, index_path)
    # read file content for metadata
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        content = ''
    title = os.path.basename(filepath)
    insert_document(source or 'local', title, content[:2000])
    return vs


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('file')
    p.add_argument('--index', default='faiss_index')
    p.add_argument('--source', default='local')
    args = p.parse_args()
    ingest_and_record_text(args.file, args.index, args.source)
    print('Ingested', args.file)
