import sqlite3
import csv

def handle_sqlite3(db_path, query_file_path, csv_file_path):
    """
    Handle the data export from a SQLite 3 DB to CSV
    """
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    query_string = __query_file_to_string(query_file_path)

    with open(csv_file_path, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

        cursor.execute(query_string)

        csv_writer.writerow([d[0] for d in cursor.description])
        for row in cursor:
            csv_writer.writerow(row)


def handle_annotations(annotation_file_path, csv_file_path):
    """
    Handle the data export from a Go Annotation File to CSV
    """
    try:
        with open(annotation_file_path) as annotation_file, open(csv_file_path, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC)

            for line in annotation_file:
                if line.startswith('UniProtKB'):
                    line_arr = line.split('\t')
                    csv_file_writer.writerow(line_arr)

        return True
    except:
        return False



def __query_file_to_string(query_file_path):
    query_string = ""
    with open(query_file_path) as f:
        lines = f.readlines()
        query_string = " ".join(lines)
    
    return query_string