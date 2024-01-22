#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Check if the necessary variables are set
if [ -z "$PGDATABASE" ] || [ -z "$PGUSER" ] || [ -z "$PGPASSWORD" ] || [ -z "$PGHOST" ] || [ -z "$PGPORT" ]; then
    echo "Please set PGDATABASE, PGUSER, PGPASSWORD, PGHOST, and PGPORT in your .env file."
    exit 1
fi

# Function to execute a SQL command as the postgres user
function execute_sql() {
    PGPASSWORD=postgres psql -h $PGHOST -U postgres -d postgres -c "$1"
}

# Create the database and user, then grant privileges
if execute_sql "DROP DATABASE IF EXISTS $PGDATABASE;" &&
   execute_sql "CREATE DATABASE $PGDATABASE;" &&
   execute_sql "DROP USER IF EXISTS $PGUSER;" &&
   execute_sql "CREATE USER $PGUSER WITH PASSWORD '$PGPASSWORD';" &&
   execute_sql "ALTER ROLE $PGUSER SET client_encoding TO 'utf8';" &&
   execute_sql "ALTER ROLE $PGUSER SET default_transaction_isolation TO 'read committed';" &&
   execute_sql "ALTER ROLE $PGUSER SET timezone TO 'UTC';" &&
   execute_sql "GRANT ALL PRIVILEGES ON DATABASE $PGDATABASE TO $PGUSER;" &&
   execute_sql "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO $PGUSER;" &&
   execute_sql "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO $PGUSER;" &&
   execute_sql "GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO $PGUSER;" &&
   execute_sql "ALTER ROLE $PGUSER INHERIT;" &&
   execute_sql "GRANT USAGE ON SCHEMA public TO $PGUSER;" && 
    execute_sql "ALTER DATABASE $PGDATABASE OWNER TO $PGUSER;"; then
    echo "Database setup completed successfully."
fi
