##########################################
# Compile Flatbuffers Schemas

for DATA_SCHEMA_FBS in schema/*.fbs; 
do 
    flatc --python -o python ${DATA_SCHEMA_FBS}
    # flatc --js --es6-js-export -o js ${DATA_SCHEMA_FBS}
    flatc --ts -o ts ${DATA_SCHEMA_FBS}
done

flatc --python -o python schema/main.fbs
# flatc --js --es6-js-export -o js schema/main.fbs
flatc --ts --no-fb-import -o ts schema/main.fbs

##########################################
# Format Python files
black python/Dim/*
