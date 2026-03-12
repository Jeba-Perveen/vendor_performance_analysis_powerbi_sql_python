import pandas as pd
import sqlite3
import logging

logging.basicConfig(
    filename = 'logs/get_vendor_summary',
    level = logging.DEBUG,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filemode = 'a')

def create_vendor_summary(conn):
    vendor_sales_summary= pd.read_sql_query("""with freight_summary as (
                select VendorNumber,
                   sum(Freight) as freight_cost
                   from vendor_invoice
                   group by VendorNumber),

    purchase_summary as(select 
                p.VendorNumber,
                p.VendorName,
                p.Brand,
                p.Description,
                p.PurchasePrice,
                pp.Volume,
                pp.Price as actual_price,
                sum(p.Quantity) as total_purchase_quantity,
                sum(p.Dollars) as total_purchase_dollars
                from purchases p
                join purchase_prices pp
                on p.Brand = pp.Brand
                where p.PurchasePrice >0
                group by p.VendorNumber,p.VendorName,p.Brand,p.Description,p.PurchasePrice,pp.Price,pp.Volume
                ),
                        sales_summary as (select
                VendorNo,
                Brand,
                sum(SalesDollars) as total_sales_dollars,
                sum(SalesPrice) as total_sales_price,
                sum(SalesQuantity) as total_sales_quantity,
                sum(ExciseTax) as total_excise_tax
                from sales
                group by VendorNo,Brand)

    select 
        ps.VendorNumber as vendor_number,
        ps.VendorName as vendor_name,
        ps.Brand as brand,
        ps.Description as description,
        ps.PurchasePrice as purchase_price,
        ps.actual_price,
        ps.Volume as volume,
        ps.total_purchase_quantity,
        ps.total_purchase_dollars,
        ss.total_sales_quantity,
        ss.total_sales_dollars,
        ss.total_sales_price,
        ss.total_excise_tax,
        fs.freight_cost
        from purchase_summary ps
    left join sales_summary ss
    on ps.VendorNumber = ss.VendorNO and ps.Brand = ss.Brand
    left join Freight_summary fs
    on ps.VendorNumber = fs.VendorNumber
    order by ps.total_purchase_dollars desc """
    ,conn)
    return vendor_sales_summary

def clean_data(df):
    #changing data tpe to float
    df['volume'] = df['volume'].astype('float64')
    df.fillna(0,inplace = True)

    #removing spaces from categorical column
    df['vendor_name'] = df['vendor_name'].str.strip()
    df['description'] = df['description'].str.strip()

    #creating new columns for analysis
    vendor_sales_summary['gross_profit'] = vendor_sales_summary['total_sales_dollars']- vendor_sales_summary['total_purchase_dollars']
    vendor_sales_summary['profit_margin'] = (vendor_sales_summary['gross_profit']/vendor_sales_summary['total_sales_dollars'])*100
    vendor_sales_summary['stock_turnover'] = vendor_sales_summary['total_sales_quantity']/vendor_sales_summary['total_purchase_quantity']
    vendor_sales_summary['sales_purchase_ratio'] = vendor_sales_summary['total_sales_dollars']/vendor_sales_summary['total_purchase_dollars']

    return df
if __name__ == '__main__':
    #creating database
    conn = sqlite3.connect('inventoy.db')

    logging.info('creating vendor summary table....')
    summary_df = create_vendor_summary(conn)
    loggig.info(summary_df.head())

    logging.info('cleaning data....')
    clean_df = clean_data(summary_df)
    logging.info(clean_df.head())

    logging.info('ingesting data.....')
    ingest_db(clean_df,'vendor_sales_summary',conn)
    logging.info('completed')