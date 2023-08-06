import copy
import emoji
import datetime
import dbstream
import pyodbc
import os
import re
from pyzure.core.Column import create_columns, change_column_type
from pyzure.core.Table import create_table
from pyzure.core.tools.print_colors import C
from pyzure.core.tools.progress_bar import print_progress_bar


def extract_emojis(str_):
    return ''.join(c for c in str_ if c in emoji.UNICODE_EMOJI or c in ('🏻', '🇺', '🇸', '🇬', '🇧'))


def replace_all_emoji(str_):
    for i in extract_emojis(str_):
        str_ = str_.replace(i, '???')
    return str_


class AzureDBStream(dbstream.DBStream):
    def __init__(self, instance_name, client_id):
        super().__init__(instance_name, client_id=client_id)
        self.instance_type_prefix = "AZURE"
        self.ssh_init_port = 6544

    def credentials(self):
        creds = super().credentials()
        alias = self.instance_type_prefix + "_" + self.instance_name
        if os.environ.get(alias + "_DRIVER_PATH"):
            driver = os.environ.get(alias + "_DRIVER_PATH")
        else:
            driver = os.environ.get(alias + "_DRIVER")
        creds.update({
            "uid": creds["user"],
            "server": creds["host"],
            "driver": driver,
            "TDS_Version": "7.2"
        })
        return creds

    def _execute_query_custom(self, query, data=None):
        connection_kwargs = self.credentials()
        con = pyodbc.connect(**connection_kwargs)
        cursor = con.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
        except Exception as e:
            cursor.close()
            con.close()
            raise e
        result = []
        try:
            columns = [column[0] for column in cursor.description]

            for row in cursor.fetchall():
                dict_ = dict()
                for i in range(len(columns)):
                    dict_[columns[i]] = row[i]
                result.append(dict_)
        except (pyodbc.ProgrammingError, TypeError):
            pass
        con.commit()
        cursor.close()
        con.close()
        query_create_table = re.search("(?i)(?<=((into ))).*(?=\n)", query)
        if result:
            return [dict(r) for r in result]
        elif query_create_table:
            return {'execute_query': query_create_table}
        else:
            return None

    def _send(
            self,
            data,
            replace,
            batch_size=1000,
            sub_commit=True):
        # Time initialization
        start = datetime.datetime.now()

        # Extract info
        rows = data["rows"]
        if not rows:
            return 0
        table_name = data["table_name"]
        columns_name = data["columns_name"]
        total_len_data = len(rows)

        # Clean table if needed
        if replace:
            cleaning_query = '''DELETE FROM ''' + table_name + ''';'''
            self.execute_query(cleaning_query)
            print(C.OKBLUE + "Cleaning Done" + C.ENDC)

        connection_kwargs = self.credentials()
        con = pyodbc.connect(**connection_kwargs)
        cursor = con.cursor()

        small_batch_size = int(2099 / len(columns_name))

        print("Initiate send_to_azure...")

        # Initialize counters
        boolean = True
        question_mark_pattern = "(%s)" % ",".join(["?" for i in range(len(rows[0]))])
        counter = 0
        while boolean:
            temp_row = []
            question_mark_list = []
            for i in range(small_batch_size):
                if rows:
                    value_list = rows.pop()
                    for i in range(len(value_list)):
                        if isinstance(value_list[i], str):
                            value_list[i] = replace_all_emoji(value_list[i])
                    temp_row.append(value_list)
                    question_mark_list.append(question_mark_pattern)
                else:
                    boolean = False
                    continue
            counter = counter + len(temp_row)
            # percent = round(float(counter * 100) / total_len_data)
            if sub_commit:
                suffix = "%% rows sent"
                print_progress_bar(counter, total_len_data, suffix=suffix)
            else:
                suffix = "% rows prepared to be sent"
                print_progress_bar(counter, total_len_data, suffix=suffix)
            data_values_str = ','.join(question_mark_list)
            columns_name_str = "\",\"".join(columns_name)
            inserting_request = '''INSERT INTO %s ("%s") VALUES %s ;''' % (
                table_name, columns_name_str, data_values_str)

            final_data = [y for x in temp_row for y in x]
            if final_data:
                try:
                    cursor.execute(inserting_request, final_data)
                except Exception as e:
                    cursor.close()
                    con.close()
                    raise e

            if sub_commit:
                con.commit()
        if not sub_commit:
            con.commit()
        cursor.close()
        con.close()

        print("data sent to azure")
        print("Total rows: %s" % str(total_len_data))
        print(C.BOLD + "Total time in seconds : %s" % str((datetime.datetime.now() - start).seconds) + C.ENDC)
        return 0

    def _send_data_custom(self,
                          data,
                          replace=True,
                          batch_size=1000,
                          other_table_to_update=None,
                          sub_commit=True
                          ):
        data_copy = copy.deepcopy(data)
        try:
            self._send(data, replace=replace, sub_commit=sub_commit)
        except Exception as e:
            print(e)
            if "invalid object name" in str(e).lower():
                create_table(
                    self,
                    data_copy,
                    other_table_to_update
                )
            elif "invalid column name" in str(e).lower():
                create_columns(self, data_copy, other_table_to_update)
            elif "string or binary data would be truncated" in str(e).lower():
                change_column_type(self, data_copy, other_table_to_update)
            elif "The conversion of the nvarchar value" in str(e) and "overflowed an int column" in str(e):
                change_column_type(self, data_copy, other_table_to_update)
            elif "Use a larger integer column" in str(e):
                change_column_type(self, data_copy, other_table_to_update)
            elif "Conversion failed when converting the nvarchar value" in str(e):
                change_column_type(self, data_copy, other_table_to_update)
            else:
                raise e
            self._send_data_custom(data_copy, replace=replace, batch_size=batch_size,
                                   other_table_to_update=other_table_to_update, sub_commit=sub_commit)

    def get_max(self, schema, table, field, filter_clause=""):
        try:
            r = self.execute_query("SELECT max(%s) as max FROM %s.%s %s" % (field, schema, table, filter_clause))
            return r[0]["max"]
        except IndexError:
            return None
        except Exception as e:
            if "object" in str(e):
                return None
            raise e

    def clean(self, selecting_id, schema_prefix, table):
        print('trying to clean table %s.%s using %s' % (schema_prefix, table, selecting_id))
        cleaning_query = """
                DELETE FROM %(schema_name)s.%(table_name)s WHERE %(id)s IN (SELECT distinct %(id)s FROM %(schema_name)s.%(table_name)s_temp);
                INSERT INTO %(schema_name)s.%(table_name)s 
                SELECT * FROM %(schema_name)s.%(table_name)s_temp;
                DELETE FROM %(schema_name)s.%(table_name)s_temp;
                """ % {"table_name": table,
                       "schema_name": schema_prefix,
                       "id": selecting_id}
        self.execute_query(cleaning_query)
        print('cleaned')

    def get_data_type(self, table_name, schema_name):
        query = """ select
                       col.name as column_name,
                       t.name as data_type
                
                  from sys.tables as tab
                       inner join sys.columns as col
                        on tab.object_id = col.object_id
                      inner join sys.schemas as sch
                        on tab.schema_id = sch.schema_id
                       left join sys.types as t
                        on col.user_type_id = t.user_type_id
                where tab.name='%s' and sch.name='%s'

                """ % (table_name, schema_name)

        return self.execute_query(query=query)

    def create_view_from_columns(self, view_name, columns, schema_name, table_name):
        drop_view_query = "DROP VIEW IF EXISTS %s;" % view_name
        view_query = "CREATE VIEW %s as (SELECT %s FROM %s.%s)" % (view_name, columns, schema_name, table_name)
        self.execute_query(drop_view_query)
        self.execute_query(view_query)

    def create_schema(self, schema_name):
        self.execute_query("CREATE SCHEMA %s" % schema_name)
