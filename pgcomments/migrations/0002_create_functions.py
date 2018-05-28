FUNCTIONS = [
    ("pgcomments_add_comment (integer, integer[], text, text)", "void", "SQL", """
        WITH X AS (
            SELECT '{' || array_to_string(array_append($2, NULL), ',children,', '') || '-1}' AS path,
                   jsonb_build_object('author', $3, 'text', $4, 'created_at', now(), 'children', '[]'::jsonb) AS new_value
        )
        UPDATE pgcomments_thread
           SET thread = jsonb_insert(thread, X.path::text[], X.new_value, true)
          FROM X WHERE id = $1;
    """),

    ("pgcomments_set_attribute (integer, integer[], text, jsonb)", "void", "SQL", """
        WITH X AS (
            SELECT '{' || array_to_string($2, ',children,') || '}' AS path,
                   jsonb_build_object($3, $4) AS new_value
        )
        UPDATE pgcomments_thread
           SET thread = jsonb_set(thread, X.path::text[], thread #> X.path::text[] || X.new_value)
          FROM X WHERE id = $1;
    """),

    ("pgcomments_get_attribute (integer, integer[], text)", "jsonb", "SQL", """
        WITH X AS (
            SELECT '{' || array_to_string($2, ',children,') || ',' || $3 || '}' AS path
        )
        SELECT thread #> X.path::text[]
          FROM pgcomments_thread, X WHERE id = $1;
    """),

    ("pgcomments_delete_comment (integer, integer[])", "void", "SQL", """
        SELECT pgcomments_set_attribute ($1, $2, 'author', '""');
        SELECT pgcomments_set_attribute ($1, $2, 'text', '""');
    """),

    ("pgcomments_delete_thread (integer, integer[])", "void", "SQL", """
        SELECT pgcomments_delete_comment ($1, $2);
        SELECT pgcomments_set_attribute ($1, $2, 'children', '[]');
    """),
]

################################################################################

from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('pgcomments', '0001_initial'),
    ]
    operations = [
        migrations.RunSQL(
            "CREATE OR REPLACE FUNCTION {0} RETURNS {1} LANGUAGE {2} AS $${3}$$;".format(*f),
            "DROP FUNCTION IF EXISTS {0};".format(*f)
        ) for f in FUNCTIONS
    ]
