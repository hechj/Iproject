import akshare as ak

bond_zh_us_rate_df = ak.bond_zh_us_rate()
bond_zh_us_rate_df = bond_zh_us_rate_df[['日期', '中国国债收益率10年']]
bond_zh_us_rate_df.dropna(inplace=True)
bond_zh_us_rate_df = bond_zh_us_rate_df.reindex(index=bond_zh_us_rate_df.index[::-1])
bond_zh_us_rate_df = bond_zh_us_rate_df.reset_index(drop=True)
print(bond_zh_us_rate_df)
