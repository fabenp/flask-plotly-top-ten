from flask import Flask, render_template
import csv, re, operator

languages = ["Java", "C++", "C#", "ASM", "Python", "Visual Basic", "Javascript", "PHP", "Perl", "Ruby", "Swift", "R", "SQL", "Objective-C", "Haskell", "Elixir", "Rust", "Prolog", "C", "Smalltalk"]

app = Flask(__name__)

@app.route('/')
def main():
    language_frequencies = {}
    text = ""

    for language in languages:
        language_frequencies[language] = 0

    with open('askcomputerscience.csv', 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for idx, row in enumerate(reader):
            if idx > 0 and idx % 2000 == 0:
                break
            if  'text' in row:
                nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['text'], flags=re.MULTILINE)
                text += nolinkstext

            if 'title' in row:
                nolinkstext = re.sub(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', row['title'], flags=re.MULTILINE)
                text += nolinkstext

    for key in language_frequencies:
        for word in text.split():
            if str(key).lower() == str(word).lower():
                language_frequencies[key] += 1
            elif "VB".lower() == str(word).lower() or ".net".lower() == str(word).lower():
                language_frequencies['Visual Basic'] += 1
            elif "js" == str(word.lower()):
                language_frequencies['Javascript'] += 1
            elif "assembly" == str(word.lower()):
                language_frequencies['ASM'] += 1

    language_frequencies = sorted(language_frequencies.items(), key=operator.itemgetter(1))
    top_ten = list(reversed(language_frequencies))
    if len(top_ten) >= 11:
        top_ten = top_ten[1:11]
    else :
        top_ten = top_ten[0:len(top_ten)]


    top_ten_list_vals = []
    top_ten_list_labels = []
    for language in top_ten:
        top_ten_list_vals.append(language[1])
        top_ten_list_labels.append(language[0])

    graph_values = [{
                    'labels': top_ten_list_labels,
                    'values': top_ten_list_vals,
                    'type': 'pie',
                    'insidetextfont': {'color': '#FFFFFF',
                                        'size': '14',
                    },
                    'textfont': {'color': '#FFFFFF',
                                        'size': '14',
                    },
    }]

    layout = {
                'title': '<b>Top 10 Most Mentioned Programming Languages in /r/askcomputerscience</b>',

    }

    return render_template('index.html', graph_values=graph_values, layout=layout)

if __name__ == '__main__':
  app.run(debug= True,host="127.0.0.1",port=5000, threaded=True)
