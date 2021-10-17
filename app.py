import csv

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    print("-----> hitting index")
    if request.method == 'POST':
        if request.files:
            f = request.files['file']
            if str(f.content_type) == "text/csv":
                f.save('uploads/1.csv')
                return redirect("/result")
            else:
                return render_template("home.html", error="Please Upload file in a CSV format")

    return render_template("home.html")


@app.route("/result")
def result():
    NLS_KEYS = convert_to_nls('uploads/1.csv')
    print(NLS_KEYS)
    return render_template("result.html", result=NLS_KEYS)


def convert_to_nls(path):
    YAML_STR = "\n\n"
    language_map = {
        "hi": 2,
        "en": 4
    }
    try:
        for lang in language_map.keys():
            with open(path, 'r', encoding="utf-8") as file:
                reader = csv.reader(file)
                YAML_STR += f"{lang}_nls: &{lang}_nls\n"
                for row in reader:
                    row_two = row[language_map[lang]]  # row 2 hindi
                    val = str(row_two)
                    if row[0] and row[0] != "NLS Key" and row[4] != "":
                        YAML_STR += "  " + row[0] + " : " + val.replace("\n", " ") + "\n"

            YAML_STR += "\n\n"

        YAML_STR += "\n\n"
        YAML_STR += "labels:\n"
        YAML_STR += " TTS:\n"
        YAML_STR += "  en:\n"
        YAML_STR += "   <<: *en_nls\n"
        YAML_STR += "  hi:\n"
        YAML_STR += "   <<: *hi_nls\n"
        return YAML_STR

    except Exception as e:
        print(e)
        return "Something Went Wrong : " + str(e)
