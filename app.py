# langkah awal set library pandas, regex, sqlite, flask, import page python reading and writing table, dan data cleansing
import re
import pandas as pd
import sqlite3

from flask import Flask, jsonify, request, render_template, redirect, url_for

from data_reading_and_writing import create_table_1, insert_to_table_1, create_table_2, insert_to_table_2, read_table

# create flask object
app = Flask(__name__, template_folder='templates')


# ******************************************
# bikin homepage untuk function2 nya
@app.route('/', methods=['GET', "POST"])
def homepage():
    if request.method == 'POST':
        go_to_page = request.form['inputText']
        if go_to_page == "1":
            return redirect(url_for("input_text"))
        elif go_to_page == "2":
            return redirect(url_for("input_file"))
        elif go_to_page == "3":
            return redirect(url_for("read_database"))
    else:
        return render_template("homepage.html")

# ******************************************
# langkah selanjutnya buat function input file csv, dimana user bisa input file csv yang selanjutnya akan di record ke table database (buy dan sell)

@app.route('/file-processing',methods=['GET', 'POST'])
def input_file():
    if request.method == 'POST':
        input_file = request.files['inputFile']
        df = pd.read_csv(input_file, sep=';')
        if('BVal' in df.columns):
            BCode = df['BCode']
            BVal = df['BVal']
            SCode = df['SCode']
            SVal = df['SVal']
            print(BCode)
            create_table_1()
            create_table_2()
            for EmitenBuy, BuyVal in zip(BCode, BVal):
                insert_to_table_1(value_1=EmitenBuy, value_2=BuyVal)

            for EmitenSell, SellVal in zip(SCode, SVal):
                insert_to_table_2(value_1=EmitenSell, value_2=SellVal)

            json_response={'response':"SUCCESS",
                           'total emiten': 'Ok',
                           'total val': 'Ok'
                          }
            json_response=jsonify(json_response)
            return json_response
        else:
            json_response={'ERROR_WARNING': "NO COLUMNS 'Tweet' APPEAR ON THE UPLOADED FILE"}
            json_response = jsonify(json_response)
            return json_response
        return json_response

    else:
        return render_template("test_file_input.html")

# ******************************************
# langkah selanjutnya buat function input file processing, dimana user bisa upload file csv yang ada column Tweet, untuk di cleansing dan hasil dari process tersebut di record di database

@app.route('/read-database',methods=['GET', 'POST'])
def read_database():
    if request.method == "POST":
        showed_index=request.form['inputIndex']
        showed_keywords = request.form['inputKeywords']
        if len(showed_index)>0:
            print("AAAAAAAAAA")
            result_from_reading_database = read_table(target_index=showed_index)
            previous_text=result_from_reading_database[0].decode('latin1')
            cleaned_text=result_from_reading_database[1].decode('latin1')
            json_response={'Index': showed_index,
                           'Previous_text': previous_text,
                           'Cleaned_text': cleaned_text
                          }
            json_response = jsonify(json_response)
            return json_response
        elif len(showed_keywords)>0:
            print("BBBBBBBBB")
            results = read_table(target_keywords=showed_keywords)
            json_response={'showed_keywords': showed_keywords,
                           'previous_text': results[0][0].decode('latin1'),
                           'cleaned_text': results[0][1].decode('latin1')
                          }
            json_response = jsonify(json_response)
            return json_response
        else:
            print("CCCCCCCC")
            json_response={'ERROR_WARNING': "INDEX OR KEYWORDS IS NONE"}
            json_response = jsonify(json_response)
            return json_response
    else:
        return render_template("read_database.html")

# ******************************************

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template("About.html")



if __name__ == '__main__':
    app.run(debug=True)
