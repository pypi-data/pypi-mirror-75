import pyarrow as pa
import pyarrow.parquet as pq


def numerize(x, max_padding=20):
    return str(x).zfill(max_padding)


def raise_(exception):
    raise exception


def chunkize(list_data, chunk_size=32495):
    for i in range(0, len(list_data), chunk_size):
        yield list_data[i:i + chunk_size]


def dechunkize(chunks):
    return "".join(chunks)


def to_parquet_bytes(dataframe):
    table = pa.Table.from_pandas(dataframe)
    buf = pa.BufferOutputStream()
    pq.write_table(table, buf)
    value = buf.getvalue()
    return value.to_pybytes()
