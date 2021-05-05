#!/usr/bin/python

import requests
import json
import csv
import argparse
import sqlite3

API_URL = "http://images-api.nasa.gov/search"
CSV_PATH = './output/query_results.csv'
DB_NAME = 'nasa.db'
TABLE_CREATE = "create table if not exists result(id integer PRIMARY KEY, nasa_id text, url text, size integer )"
SQL_INSERT = """INSERT INTO result
                          (id, nasa_id, url, size) 
                          VALUES (?, ?, ?, ?);"""
SQL_FETCH = "SELECT * FROM result"


def main():
    args = parse_args()
    params = {'q': args.query_string, 'media_type': args.media_type}
    response = requests.get(API_URL, params)
    result_list = response_parser(json.loads(response.text), args.file_size)
    if result_list:
        if args.output_to == 'csv':
            write_to_csv(result_list)
        else:
            write_to_db(result_list, DB_NAME, TABLE_CREATE, SQL_INSERT)
            poc_db_data(DB_NAME, SQL_FETCH)
    return


def response_parser(pyval_response, threshold_size):
    result = []
    for content in pyval_response.items():
        for query_result in (content[1].items()):
            for each_result in query_result[1]:
                if type(each_result) is dict:  # Referring to relevant results by correct data types
                    try:
                        for each_result_data in (each_result['data']):
                            metadata_url = each_result['href']
                            url_to_orig = requests.get(metadata_url).json()[0]
                            get_orig_size = check_image_size(requests.get(metadata_url).json()[0], threshold_size)
                            if get_orig_size:
                                result.append([each_result_data['nasa_id'], get_orig_size, url_to_orig])
                    except:
                        print("Ignoring irrelevant data while parsing")
    return result


def check_image_size(url, min_size):
    try:
        head_response = requests.head(url, allow_redirects=True)
        if head_response.headers['content-length'] > min_size:
            return head_response.headers['content-length']
        else:
            return False
    except:
        print("Failed to extract content-length from header")
        exit()


def write_to_csv(result):
    try:
        with open(CSV_PATH, 'w') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',')
            for line in result:
                csv_writer.writerow(line)
                print("committed one line")
    except:
        print("failed to write csv")
    return


def write_to_db(response, db_name, create_command, insert_command):
    i = 1
    con = sqlite3.connect(db_name)
    print("connected to nasa.db")
    cursorObj = con.cursor()
    cursorObj.execute("drop table if exists result")
    cursorObj.execute(create_command)
    print("Table was created successfully")
    for line in response:
        data_tuple = (i, line[0], line[1], line[2])
        try:
            cursorObj.execute(insert_command, data_tuple)
            print("row {id} was inserted successfully".format(id=i))
            i += 1
        except Exception as e:
            print(e)
    con.commit()
    return


def poc_db_data(db_name, fetch_command):
    con = sqlite3.connect(db_name)
    cursorObj = con.cursor()
    cursorObj.execute(fetch_command)
    rows = cursorObj.fetchall()
    print("\n" * 10)
    print("Preparing to print all existing data: ")
    print("*" * 38, "\n\n")
    for row in rows:
        print(row)
    return


def parse_args():
    parser = argparse.ArgumentParser(description='NASA image API')
    parser.add_argument('-q', '--query',
                        dest='query_string',
                        default="Ilan Ramon",
                        help='Free text search terms to compare to all indexed metadata')
    parser.add_argument('-m', '--media-type',
                        dest='media_type',
                        default='image',
                        help='Media types to restrict the search to. Available types: '
                             '[“image”, “audio”]. Separate multiple values with commas.')
    parser.add_argument('-s', '--size',
                        dest='file_size',
                        default='100000',
                        help='Original image size')
    parser.add_argument('-o', '--output',
                        choices=['csv', 'db'],
                        dest='output_to',
                        default='db',
                        help='By default, script will write to CSV. Modify to db if needed')
    result = parser.parse_args()
    return result


if __name__ == '__main__':
    main()
