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
            CREATE OR REPLACE FUNCTION pgcomments_set_comment_attributes (
                _id integer,
                _path integer[],
                _new_value jsonb
            ) RETURNS VOID LANGUAGE SQL AS $$
                WITH X AS (
                    SELECT ('{' || array_to_string(_path, ',children,') || '}')::text[] AS path,
                           _new_value::jsonb AS new_value
                )
                UPDATE pgcomments_thread
                   SET thread = jsonb_set(thread, X.path, thread#>X.path || X.new_value)
                  FROM X
                 WHERE id = _id;
            $$;
        """, reverse_sql="""
            DROP FUNCTION IF EXISTS pgcomments_set_comment_attributes (integer, integer[], jsonb);
        """),
    ]
