#-----------------------------------------------------------------------------
# Copyright (c) 2023 Doug Bellinger
# All rights reserved.
#
# The full license is in the file LICENSE, distributed with this software.
#-----------------------------------------------------------------------------
import os
import pandas as pd
import logging

logger = logging.getLogger("file_utils")

def open_csv_or_excel(f,s=None,dtype=None):
    """ open_csv_or_excel

    This function dramatically reduces the load time jupyter notebooks that ingest 
    a lot of static xlsx data.   CSV's load MUCH faster.

    Args:
        f (file path): path to a csv or xlsx file
        s (sheet name): if an excel file, read this worksheet, and write csv file.
        dtype (types dictionary)

    """
    logger.debug(f"opening {f} (sheet:{s}, dtype:{dtype is not None})")
    f = os.path.splitext(f)[0]
    logging.info(f"reading file {f}")
    if (os.path.isfile(f+".csv")):
        return(pd.read_csv(f+".csv", dtype=dtype))
    else:
        df = pd.read_excel(f+".xlsx", dtype=dtype)#,sheet_name=s)#, dtype=dtype)
        logging.info(f"file:{f} {len(df)}")
        df.to_csv(f+".csv")
        return(df)
        