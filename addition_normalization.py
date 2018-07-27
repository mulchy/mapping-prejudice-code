#!/usr/bin/env python
"""
Normalize addtion names by replacing common abbreviations.
Split each row with multiple comma delimited lots into separate rows.
"""

import pandas as pd
import numpy as np
import argparse

def normalize_addition(df, column_name):
    """
    Updates the given dataframe by normalizing the addition names.
    Converts addition to addn and abbreviates first, second, third, fourth and fifth".
    """
    if column_name in df.columns:
        df[column_name] = df[column_name] \
          .str.strip() \
          .str.lower() \
          .str.replace('addition', 'addn') \
          .str.replace('first', '1st') \
          .str.replace('second', '2nd') \
          .str.replace('third', '3rd') \
          .str.replace('fourth', '4th') \
          .str.replace('fifth', '5th')
        return df
    else:
        raise Exception('Column name not present')

def split_rows(df, column_name):
    """
    Creates a new dataframe where lot columns containing multiple
    comma delimited values are split into seperate rows.
    """
    new_rows = []
    for (index, row) in df.iterrows():
        value = row[column_name]
        #skip null values or values with semicolons
        if pd.isnull(value) or ';' in value:
            new_rows.append(row)
        else:
            split_values = value.split(',')
            for new_value in split_values:
                new_row = row.copy()
                new_row[column_name] = new_value.strip()
                new_rows.append(new_row)
    return pd.DataFrame(new_rows)

def main(input_filename, output_filename):
        df = pd.read_csv(input_filename, encoding='latin1')
        normalize_addition(df, 'Addition')
        split = split_rows(df, 'Lot')
        split.to_csv(output_filename, line_terminator='\r\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Normalize additon names and split multi-lot records.')
    parser.add_argument('-i', '--input', help='Input csv filename', required=True)
    parser.add_argument('-o', '--output', help='Output csv filename', required=True)
    args = parser.parse_args()
    main(args.input, args.output)
