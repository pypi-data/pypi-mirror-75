"""
Miscellaneous information for the pathomap project
"""

import pandas as pd
import pathlib

class Meta:
    
    def __init__(self):
        self.info = "This class has meta information for genes and organs."

    def get_organ_list(self):
        """
        Returns a list of organs currently available in PathoMap
        """
        filepath = pathlib.Path(__file__).parent / 'data/gene_tissue_similarity.csv'
        with open(filepath) as f:
            df = pd.read_csv(filepath)
            organ_names = list(df.columns)
            organ_names.remove('0')

            cleaned = [(" ").join(name.split("_")).capitalize() for
                      name in organ_names]
            
            return cleaned


    def get_gene_list(self, startchars='A', limit=-1, offset=0):
        """
        Returns all the genes that start with startchars
        according to limit and offset
        """

        filepath = pathlib.Path(__file__).parent / 'data/gene_tissue_similarity.csv'
        with open(filepath) as f:
            df = pd.read_csv(filepath)
            try:
                genes = list(df[df['0'].str.startswith(startchars)]['0'])
            except KeyError:
                return ["Invalid Value for startchars. Must be alphabetical."]
            
            except TypeError:
                return ["Limit/Offset datatype is wrong. Please provide an integer."]

        if limit == -1:
            # return all the genes
            return genes[offset:len(genes)]

        return genes[offset:offset+limit]

if __name__ == '__main__':
    m = Meta()
    print(m.get_gene_list('F', 10))
    print(m.get_organ_list())