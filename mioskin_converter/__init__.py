# /usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from six import BytesIO, StringIO

from flask import Flask, request, render_template, send_file
from werkzeug import secure_filename

import csv

app = Flask(__name__)


def export_for_mioskin(csv_input, **kwargs):
    csv_input = StringIO(csv_input.read().decode('utf-8'))
    csv_output = StringIO()
    reader = csv.reader(csv_input, delimiter=',')
    delimiter = kwargs.get("csv", False) and ";" or ","
    writer = csv.writer(csv_output, delimiter=delimiter)

    first_line = True
    # POUR CHAQUE LIGNE EN ENTREE
    for row in reader:
        row = list(row)
        if first_line:
            # ON GERE LES ENTETES de COLONNES
            result = row[0:2]
            if kwargs.get("radar_type", False):
                result.append("TYPE")
            if kwargs.get("speed", False):
                result.append("SPEED")
            if kwargs.get("dirtype", False):
                result.append("DIRTYPE")
            if kwargs.get("direction", False):
                result.append("DIRECTION")
            if kwargs.get("mioskin", False):
                result.append("MIOSKIN")
            if kwargs.get("scdb", False):
                result.append("SCDB")
            if kwargs.get("hauteur", False):
                result.append("HAUTEUR")
            if kwargs.get("SURCHARGE", False) and len(row) > 6:
                result.append("SURCHARGE")
            first_line = False
        else:
            # On LIT LES COLONNES DE LA LIGNE
            radar_type = row[2]
            speed = row[3]
            dirtype = row[4]
            direction = row[5]

            surcharge = False
            if len(row) > 6:
                surcharge = row[6]

            result = row[0:2]
            if kwargs.get("radar_type", False):
                result.append(radar_type)

            if kwargs.get("speed", False):
                result.append(speed)

            if kwargs.get("dirtype", False):
                result.append(dirtype)

            if kwargs.get("direction", False):
                result.append(direction)

            if kwargs.get("surcharge", False) and surcharge:
                result.append(surcharge)

            # ON CONSTRUIT LES NOUVELLES COLONNES POUR LA LIGNE
            if kwargs.get("mioskin", False):
                result.append("%sD%sa%s" % (dirtype, direction, speed))

            if kwargs.get("scdb", False):
                result.append("%s-%sD%sa%s" % (radar_type, dirtype,
                                               direction, speed))

            if kwargs.get("hauteur", False):
                result.append("H%sD%sa%s" % (speed, dirtype, direction))

            if kwargs.get("SURCHARGE", False) and surcharge:
                result.append("SD%sa%s" % (direction, surcharge))

        # ON ECRIT LA NOUVELLE LIGNE
        writer.writerow(result)

    csv_output.seek(0)
    return csv_output


@app.route('/', methods=['GET'])
def form(name=None):
    return render_template('form.html', name=name)


@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        if request.form.get("csv", False):
            filename += '.csv'
        output = export_for_mioskin(file, **request.form)
        return send_file(BytesIO(output.read().encode('utf-8')),
                         attachment_filename=filename,
                         as_attachment=True, mimetype="text/csv")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
