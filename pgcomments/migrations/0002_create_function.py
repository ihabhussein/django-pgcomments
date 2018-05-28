import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pgcomments', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL("""
            CREATE OR REPLACE FUNCTION pgcomments_add_comment (
                _id integer,
                _path integer[],
                _author text,
                _text text
            ) RETURNS VOID LANGUAGE SQL AS $$
                WITH X AS (
                    SELECT (
                               '{' ||
                               array_to_string(array_append(_path, NULL), ',children,', '') ||
                               '-1}'
                           )::text[] AS path,
                           jsonb_build_object(
                               'author', _author,
                               'text', _text,
                               'created_at', now(),
                               'children', '[]'::jsonb
                           ) AS new_value
                )
                UPDATE pgcomments_thread
                   SET thread = jsonb_insert(thread, X.path, X.new_value, true)
                  FROM X
                 WHERE id = _id;
            $$;
        """, reverse_sql="""
            DROP FUNCTION IF EXISTS blog_add_comment (integer, integer[], text, text);
        """),

        migrations.RunSQL("""
            CREATE OR REPLACE FUNCTION pgcomments_set_attribute (
                _id integer,
                _path integer[],
                _name text,
                _value jsonb
            ) RETURNS VOID LANGUAGE SQL AS $$
                WITH X AS (
                    SELECT ('{' || array_to_string(_path, ',children,') || '}')::text[] AS path,
                           jsonb_build_object(_name, _value) AS new_value
                )
                UPDATE pgcomments_thread
                   SET thread = jsonb_set(thread, X.path, thread#>X.path || X.new_value)
                  FROM X
                 WHERE id = _id;
            $$;
        """, reverse_sql="""
            DROP FUNCTION IF EXISTS pgcomments_set_attributes (integer, integer[], text, jsonb);
        """),

        migrations.RunSQL("""
            CREATE OR REPLACE FUNCTION pgcomments_get_attribute (
                _id integer,
                _path integer[],
                _name text
            ) RETURNS jsonb LANGUAGE SQL AS $$
                WITH X AS (
                    SELECT ('{' || array_to_string(_path, ',children,') || ',' || _name || '}')::text[] AS path
                )
                SELECT thread#>X.path FROM pgcomments_thread, X
                 WHERE id = _id;
            $$;
        """, reverse_sql="""
            DROP FUNCTION IF EXISTS pgcomments_get_attributes (integer, integer[], text);
        """),

        migrations.RunSQL("""
            CREATE OR REPLACE FUNCTION pgcomments_delete_comment (
                _id integer,
                _path integer[]
            ) RETURNS VOID LANGUAGE SQL AS $$
                SELECT pgcomments_set_attribute (_id, _path, 'author', '""');
                SELECT pgcomments_set_attribute (_id, _path, 'text', '""');
            $$;
        """, reverse_sql="""
            DROP FUNCTION IF EXISTS pgcomments_delete_comment (integer, integer[]);
        """),

        migrations.RunSQL("""
            CREATE OR REPLACE FUNCTION pgcomments_delete_thread (
                _id integer,
                _path integer[]
            ) RETURNS VOID LANGUAGE SQL AS $$
                SELECT pgcomments_delete_comment (_id, _path);
                SELECT pgcomments_set_attribute (_id, _path, 'children', '[]');
            $$;
        """, reverse_sql="""
            DROP FUNCTION IF EXISTS pgcomments_delete_thread (integer, integer[]);
        """),
    ]
