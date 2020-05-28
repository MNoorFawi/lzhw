import lzhw
from sys import getsizeof
from random import sample, choices
import pandas as pd

def test_weather():
    weather = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny",
               "Rain", "Sunny", "Overcast", "Overcast", "Rain", "Rain", "Sunny", "Sunny"]
    comp_weather = lzhw.LZHW(weather)
    assert getsizeof(weather) > comp_weather.size()
    assert weather == comp_weather.decompress()

def test_num():
    numbers = choices(sample(range(0, 5), 5), k = 20)
    comp_num = lzhw.LZHW(numbers)
    assert getsizeof(numbers) > comp_num.size()
    assert numbers == list(map(int, comp_num.decompress()))

def test_read_write():
    weather = ["Sunny", "Sunny", "Overcast", "Rain", "Rain", "Rain", "Overcast", "Sunny", "Sunny",
               "Rain", "Sunny", "Overcast", "Overcast", "Rain", "Rain", "Sunny", "Sunny"]
    comp_weather = lzhw.LZHW(weather)
    comp_weather.save_to_file("test.pkl")
    decomp = lzhw.decompress_from_file("test.pkl")
    assert weather == decomp

def test_comp_df():
    df = pd.DataFrame({"a": [1, 1, 2, 2, 1, 3, 4, 4],
                       "b": ["A", "A", "B", "B", "A", "C,D", "D C", "D C"]})
    comp_df = lzhw.CompressedDF(df)
    assert comp_df.compressed[1].decompress() == list(map(str, df.b))