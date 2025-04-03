#!/bin/bash

echo "Setting CAIG environment variables"

echo 'setting CAIG_AZURE_OPENAI_COMPLETIONS_DEP'
export CAIG_AZURE_OPENAI_COMPLETIONS_DEP="gpt-4o"

echo 'setting CAIG_AZURE_OPENAI_EMBEDDINGS_DEP'
export CAIG_AZURE_OPENAI_EMBEDDINGS_DEP="text-embedding-ada-002"

echo 'setting CAIG_AZURE_OPENAI_KEY'
export CAIG_AZURE_OPENAI_KEY="xxxxxxxxxxx"

echo 'setting CAIG_AZURE_OPENAI_URL'
export CAIG_AZURE_OPENAI_URL="xxxxxxxxxxx"

echo 'setting CAIG_CONFIG_CONTAINER'
export CAIG_CONFIG_CONTAINER="config"

echo 'setting CAIG_CONVERSATIONS_CONTAINER'
export CAIG_CONVERSATIONS_CONTAINER="conversations"

echo 'setting CAIG_COSMOSDB_NOSQL_ACCT'
export CAIG_COSMOSDB_NOSQL_ACCT="xxxxxxxxxx"

echo 'setting CAIG_COSMOSDB_NOSQL_AUTH_MECHANISM'
export CAIG_COSMOSDB_NOSQL_AUTH_MECHANISM="key"

echo 'setting CAIG_COSMOSDB_NOSQL_KEY'
export CAIG_COSMOSDB_NOSQL_KEY="xxxxxxxxxxxxxx

echo 'setting CAIG_COSMOSDB_NOSQL_RG'
export CAIG_COSMOSDB_NOSQL_RG="xxxxxxxxxxx"

echo 'setting CAIG_COSMOSDB_NOSQL_URI'
export CAIG_COSMOSDB_NOSQL_URI="xxxxxxxxxxxxx"

echo 'setting CAIG_FEEDBACK_CONTAINER'
export CAIG_FEEDBACK_CONTAINER="feedback"

echo 'setting CAIG_GRAPH_DUMP_OUTFILE'
export CAIG_GRAPH_DUMP_OUTFILE="tmp/model_dump.nt"

echo 'setting CAIG_GRAPH_DUMP_UPON_BUILD'
export CAIG_GRAPH_DUMP_UPON_BUILD="false"

echo 'setting CAIG_GRAPH_NAMESPACE'
export CAIG_GRAPH_NAMESPACE="http://cosmosdb.com/caig#"

echo 'setting CAIG_GRAPH_SERVICE_NAME'
export CAIG_GRAPH_SERVICE_NAME="caig-graph"

echo 'setting CAIG_GRAPH_SERVICE_PORT'
export CAIG_GRAPH_SERVICE_PORT="8001"

echo 'setting CAIG_GRAPH_SERVICE_URL'
export CAIG_GRAPH_SERVICE_URL="http://127.0.0.1"

echo 'setting CAIG_GRAPH_SOURCE_CONTAINER'
export CAIG_GRAPH_SOURCE_CONTAINER="libraries"

echo 'setting CAIG_GRAPH_SOURCE_DB'
export CAIG_GRAPH_SOURCE_DB="caig"

echo 'setting CAIG_GRAPH_SOURCE_OWL_FILENAME'
export CAIG_GRAPH_SOURCE_OWL_FILENAME="ontologies/libraries.owl"

echo 'setting CAIG_GRAPH_SOURCE_RDF_FILENAME'
export CAIG_GRAPH_SOURCE_RDF_FILENAME="rdf/libraries-graph.nt"

echo 'setting CAIG_GRAPH_SOURCE_TYPE'
export CAIG_GRAPH_SOURCE_TYPE="json_docs_file"

echo 'setting CAIG_HOME'
export CAIG_HOME="xxxxxxxxxxxxxxxx"

echo 'setting CAIG_LOG_LEVEL'
export CAIG_LOG_LEVEL="info"

echo 'setting CAIG_WEBSVC_AUTH_HEADER'
export CAIG_WEBSVC_AUTH_HEADER="x-caig-auth"

echo 'setting CAIG_WEBSVC_AUTH_VALUE'
export CAIG_WEBSVC_AUTH_VALUE="mK6ZQw!81<26>"

echo 'setting CAIG_WEB_APP_NAME'
export CAIG_WEB_APP_NAME="caig-web"

echo 'setting CAIG_WEB_APP_PORT'
export CAIG_WEB_APP_PORT="8000"

echo 'setting CAIG_WEB_APP_URL'
export CAIG_WEB_APP_URL="http://127.0.0.1"
