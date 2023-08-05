"""
Miscellaneous information for the pathomap project
"""

import pandas as pd
import pathlib


def  rev_sort_df(df):
    """
    To sort the row in reverse order according to values.
    """
    df_dict = df.to_dict(orient='records')[0]
    gene_name = df_dict['gene_name']
    del df_dict['gene_name']

    df_dict_sorted = {k: v for k, v in sorted(df_dict.items(), key=lambda item:
        item[1], reverse=True)}

    df = pd.DataFrame([df_dict_sorted])
    df.insert(0, 'gene_name', gene_name)
    return df


def healthyscore(gene_name, organ_list=[], normalize=False, desc=False):
    """
    """
    filepath = pathlib.Path(__file__).parent / 'data/expression_value.csv'
    with open(filepath) as f:
        df = pd.read_csv(filepath)

        if normalize:
            # apply z-scoring on the df
            mean = df.mean(axis=1)
            sd = df.std(axis=1)
            for col_name in df.columns:
                if col_name not in ['id', 'gene_name']:
                   df[col_name] = (df[col_name] - mean)/sd
                
        if isinstance(gene_name, str ):
            result_df =  df.loc[df['gene_name'] == gene_name]
            

            if isinstance(organ_list, (list, tuple)):
                if len(organ_list) > 0:
                    # only return the pathoscore for organs in organ_list
                    column_list = ['gene_name'] + organ_list
                    if desc:
                        return rev_sort_df(result_df[column_list])
                    else:
                        return result_df[column_list]
                else:
                    # return the pathoscore for all organs
                    if desc:
                        return rev_sort_df(result_df)
                    else:
                        return result_df
        else:
            return 'Invalid parameter value'


def pathoscore(gene_name, organ_list=[], normalize=False, desc=False):
    """
    """
    filepath = pathlib.Path(__file__).parent / 'data/gene_tissue_similarity.csv'
    with open(filepath) as f:
        df = pd.read_csv(filepath)
        df.rename(columns={"0": "gene_name"}, inplace=True)

        if normalize:
            # apply z-scoring on the df
            mean = df.mean(axis=1)
            sd = df.std(axis=1)
            for col_name in df.columns:
                if col_name not in ['id', 'gene_name']:
                   df[col_name] = (df[col_name] - mean)/sd
                
        if isinstance(gene_name, str ):
            result_df =  df.loc[df['gene_name'] == gene_name]
            

            if isinstance(organ_list, (list, tuple)):
                if len(organ_list) > 0:
                    # only return the pathoscore for organs in organ_list
                    column_list = ['gene_name'] + organ_list
                    if desc:
                        return rev_sort_df(result_df[column_list])
                    else:
                        return result_df[column_list]
                else:
                    # return the pathoscore for all organs
                    if desc:
                        return rev_sort_df(result_df)
                    else:
                        return result_df
        else:
            return 'Invalid parameter value'

if __name__ == '__main__':
    #print(pathoscore('MT-TL1'))
    #print(pathoscore('MT-TL1', organ_list=['adipose_tissue']))
    print(pathoscore('MT-TL1', ['adipose_tissue'], normalize=True))
    print(healthyscore('MT-TL1', ['adipose_tissue'], normalize=True))
    #print(pathoscore('MT-TL1', ['adipose_tissue', 'vagina']))
    # print(pathoscore('MT-TL1', ['adipose_tissue', 'vagina'], desc=False))
    # print(pathoscore('MT-TL1', ['adipose_tissue', 'vagina'], desc=True))
    # print(pathoscore('MT-TL1', ['vagina', 'adipose_tissue'], desc=True))
    # print(healthyscore('FGR', organ_list=['adipose_tissue']))
    # print(healthyscore('FGR', organ_list=['adipose_tissue'], normalize=True))
