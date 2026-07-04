def inspect_telemetry(df, driver: str):
    print(f"\n=== {driver} ===")
    print(f"Rows: {len(df):,}  |  Columns: {list(df.columns)}")
    print(df.dtypes)
    print(df[["Speed", "Throttle", "Brake", "nGear", "RPM", "Distance"]].describe())
    print(df.head(3))