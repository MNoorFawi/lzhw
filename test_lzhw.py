import lzhw
from sys import getsizeof
from random import sample, choices
import pandas as pd


def test_weather():
    weather = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny",
               "Rain", "Sunny", "Overcast", "Overcast", "Rain", "Rain", "Sunny", "Sunny"]
    comp_weather = lzhw.LZHW(weather)
    comp_weather2 = lzhw.LZHW(weather, sliding_window = 5)
    assert getsizeof(weather) > comp_weather.size()
    assert all(weather == comp_weather.decompress())
    assert all(weather == comp_weather2.decompress())


def test_num():
    numbers = choices(sample(range(0, 5), 5), k=20)
    comp_num = lzhw.LZHW(numbers)
    assert getsizeof(numbers) > comp_num.size()
    assert numbers == list(map(int, comp_num.decompress()))


def test_read_write():
    weather = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny",
               "Rain", "Sunny", "Overcast", "Overcast", "Rain", "Rain", "Sunny", "Sunny"]
    comp_weather = lzhw.LZHW(weather)
    comp_weather.save_to_file("test.pkl")
    decomp = lzhw.decompress_from_file("test.pkl")
    assert all(weather == decomp)


def test_comp_df():
    df = pd.DataFrame({"a": [1, 1, 2, 2, 1, 3, 4, 4],
                       "b": ["A", "A", "B", "B", "A", "C,D", "D C", "D C"]})
    comp_df = lzhw.CompressedDF(df, parallel=True)
    comp_df2 = lzhw.CompressedDF(df, sliding_window = 10)
    assert all(comp_df.compressed[1].decompress() == df.b)
    assert all(comp_df2.compressed[0].decompress() == df.a)


def test_comp_chunks():
    df = pd.DataFrame({"a": [1, 1, 2, 2, 1, 3, 4, 4],
                       "b": ["A", "A", "B", "B", "A", "C,D", "D C", "D C"]})
    df.to_csv("example.csv", index=False)
    chunks = 4
    compressed_chunks = lzhw.CompressedFromCSV("example.csv", chunksize=chunks)
    totals = (df.shape[0] / chunks)
    assert totals == len(compressed_chunks.all_comp.keys())
    compressed_chunks.save_to_file("comp_ex.txt")
    decomp_chunk = lzhw.decompress_df_from_file("comp_ex.txt")
    assert len(decomp_chunk) == totals
    assert all(decomp_chunk[0].a == df.a[:4])
    assert all(compressed_chunks.all_comp[1].compressed[1].decompress() == df.b[4:8])
