import io
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pip import main

# importer csv

def importer_csv():
    try:
        df = pd.read_csv(
            r'https://raw.githubusercontent.com/jbrownlee/Datasets/master/daily-min-temperatures.csv')
        con = sqlite3.connect('database.db')
        wb = pd.read_excel('data\temperatures_excel.xlsx', sheet_name=None)

        for sheet in wb:
            wb[sheet].to_sql(sheet, con, index=False)
        con.commit()
        msg = "Record Sucessfully add to database"
    except:
        con.rollback()
        msg = "Error in insert to database"
    finally:
        con.close()

    df1 = pd.DataFrame(df, columns=["Date", "Temp"])
    df1["Date"] = pd.Series(
        list(
            range(
                len(df))))
    df1.plot(x="Date", y="Temp")
    fig = df1.plot(x="Date", y="Temp").get_figure()
    plt.tight_layout()

    imgdata = io.StringIO()
    fig.savefig(imgdata, format='svg')

    return imgdata.getvalue()

    # fig.savefig('static/outputs/saida.svg')


if __name__ == '__main__':
    importer_csv()
