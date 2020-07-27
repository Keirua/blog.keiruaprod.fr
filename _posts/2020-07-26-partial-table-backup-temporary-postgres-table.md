---
title: Importing a partial table backup using a temporary PostgreSQL table
layout: post
lang: en
---

During an update we broke a row on a database recently, and some people had unnecessary notifications when they logged in the application. Turns out we needed to fetch the `updated_at` value of a specific postgres table from a previous backup to fix this problem.

Here is how we did it:

First, export the row in question from a previous database dump.

    $ psql
    \c database_name

    COPY (
        SELECT
            id,
            updated_at
        FROM dossiers
        where
            …
    ) TO '/tmp/dossiers-updates.csv' With CSV DELIMITER ',';

Then, you can upload this on the database server:

    scp /tmp/dossiers-updates.csv database.server:/tmp/dossiers-updates.csv

and reimport the data:

    CREATE TEMP TABLE tmp_updates (id int, updated_at timestamp); -- but see below
    COPY tmp_updates FROM '/tmp/dossiers-updates.csv' (FORMAT csv);
    UPDATE dossiers
        SET updated_at = tmp_updates.updated_at
        FROM tmp_updates
        WHERE
            dossiers.id = tmp_updates.id
            AND …
    ;

…and you are done. The `tmp_updates` table will be removed at the end of the execution, and you'll be able to go back to your normal life.

# More power

The previous solution can be enough, but should we have a more serious problem, it turns out that parsing the initial CSV file is not very difficult, and we can perform some operations in ruby on the data, for instance like this:

    # convert-to-update.sql
    require 'csv'

    csv_update_file = "/tmp/dossiers-updates.csv"

    CSV.foreach(csv_update_file) do |row|
      puts "update dossiers set updated_at = '#{row[1]}' where id = #{row[0]} AND revision_id IS NOT NULL AND updated_at <= '2020-07-22 09:20:00';\n";
    end

Sure, that's not the most awesome ruby script ever, but sometimes a 10 lines script is good enough.

Then, we can generate a large SQL file that we can upload

    ruby convert-to-update.rb > /tmp/updates.sql

and we can import it as a file:

    time psql -d database_name -h localhost  -p 5432 -f /tmp/updates.sql
