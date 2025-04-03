#!/bin/bash

# Navigate to the graph_app directory and execute the graph_app.sh script
cd ./graph_app
bash ./graph_app.sh &  # Run in the background

# Navigate to the web_app directory and execute the web_app.sh script
cd ../web_app
bash ./web_app.sh &  # Run in the background

# Return to the original directory
cd ..