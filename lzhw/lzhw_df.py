from .lzhw_alg import LZHW

class CompressedDF:
    def __init__(self, df, selected_columns = "all"):
        if selected_columns == "all":
            selected = range(df.shape[1])
        else:
            selected = selected_columns
        self.compressed = []
        for i in selected:
            comp_col = LZHW(df.iloc[:, i])
            self.compressed.append(comp_col)

