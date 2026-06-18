import os
import pandas as pd
import logging
from sqlalchemy import create_engine
import time


import time

def ingest_db(engine, data_path='data'):
    """
    Load all CSV files from a directory into a SQLite database.

    This function:
    - Reads CSV files in chunks of 50,000 rows.
    - Creates/replaces the table using the first chunk.
    - Appends subsequent chunks to the same table.
    - Logs ETL execution details and errors.
    - Tracks processing time and row counts for each file.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
        SQLAlchemy database connection object.

    data_path : str, optional
        Path to the directory containing CSV files.
        Default is 'data'.

    Returns
    -------
    None
    """

    for file in os.listdir(data_path):

        if file.endswith('.csv'):

            start = time.time()

            try:
                table_name = file[:-4]
                file_path = os.path.join(data_path, file)

                first_chunk = True
                total_rows = 0

                logging.info(f"Started loading {file}")

                for chunk in pd.read_csv(file_path, chunksize=50000):

                    chunk.to_sql(
                        table_name,
                        engine,
                        if_exists='replace' if first_chunk else 'append',
                        index=False
                    )

                    first_chunk = False
                    total_rows += len(chunk)

                end = time.time()
                total_time = (end - start) / 60

                logging.info(
                    f"Completed loading {file}. "
                    f"Rows loaded: {total_rows}. "
                    f"Time taken: {total_time:.2f} minutes."
                )

                print(
                    f"{file} loaded successfully "
                    f"({total_rows:,} rows, {total_time:.2f} min)"
                )

            except Exception as e:

                logging.error(
                    f"Error loading {file}: {str(e)}",
                    exc_info=True
                )

                print(f"Failed: {file}")



if __name__ == "__main__":

    logging.basicConfig(
        filename='etl.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    engine = create_engine('sqlite:///inventory.db')

    ingest_db(engine)
            
