import sqlite3
import pandas as pd
import logging


# Configure logging
logging.basicConfig(
    filename="get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)


def create_vendor_summary(conn):
    """
    Create vendor sales summary by merging purchases,
    sales, purchase prices, and vendor invoice data.
    """

    vendor_sales_summary = pd.read_sql_query("""
    WITH FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price,
            pp.Volume
    ),

    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost

    FROM PurchaseSummary ps

    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
       AND ps.Brand = ss.Brand

    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber

    ORDER BY ps.TotalPurchaseDollars DESC
    """, conn)

    return vendor_sales_summary


def clean_data(df):
    """
    Clean vendor summary data and create
    business metrics for analysis.
    """

    # Data type conversion
    df["Volume"] = df["Volume"].astype("float64")

    # Fill missing values
    df.fillna(0, inplace=True)

    # Remove leading/trailing spaces
    df["VendorName"] = df["VendorName"].astype(str).str.strip()
    df["Description"] = df["Description"].astype(str).str.strip()

    # Business metrics
    df["GrossProfit"] = (
        df["TotalSalesDollars"] -
        df["TotalPurchaseDollars"]
    )

    df["ProfitMargin"] = (
        df["GrossProfit"] /
        df["TotalSalesDollars"]
    ) * 100

    df["SalesToPurchaseRatio"] = (
        df["TotalSalesDollars"] /
        df["TotalPurchaseDollars"]
    )

    df["StockTurnover"] = (
        df["TotalSalesQuantity"] /
        df["TotalPurchaseQuantity"]
    )

    return df


if __name__ == "__main__":

    conn = sqlite3.connect("inventory.db")

    try:

        logging.info(
            "Creating Vendor Summary Table..."
        )

        summary_df = create_vendor_summary(conn)

        logging.info(
            f"Summary table created with "
            f"{summary_df.shape[0]} rows and "
            f"{summary_df.shape[1]} columns"
        )

        logging.debug(
            "\n" + summary_df.head().to_string()
        )

        logging.info("Cleaning Data...")

        clean_df = clean_data(summary_df)

        logging.debug(
            "\n" + clean_df.head().to_string()
        )

        logging.info(
            "Loading vendor_sales_summary table..."
        )

        clean_df.to_sql(
            "vendor_sales_summary",
            conn,
            if_exists="replace",
            index=False
        )

        logging.info(
            "vendor_sales_summary loaded successfully."
        )

        print(
            "vendor_sales_summary table created successfully."
        )

    except Exception as e:

        logging.error(
            f"Error occurred: {e}",
            exc_info=True
        )

        print(f"Error: {e}")

    finally:

        conn.close()

        logging.info(
            "Database connection closed."
        )