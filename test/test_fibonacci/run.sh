#!/bin/sh

# Run the server
server_script="./src/server/main.py"
server_port=10003
script_dir="./scripts"
script_file="fibonacci.dsl"

python $server_script --port $server_port "$script_dir/$script_file" >/dev/null 2>&1 &
server_pid=$!
echo "Server($server_pid) started on port $server_port"

# Run the client
client_script="./src/client/main.py"
test_dir="./test/test_fibonacci"

for i in 1 2; do
    python $client_script --port $server_port <"$test_dir/input$i.txt" >"$test_dir/output$i.txt"
    if [ "$(diff "$test_dir/output$i.txt" "$test_dir/expected$i.txt" -b)" = "" ]; then
        echo "Test $i passed..."
    else
        echo "Test $i failed..."
        kill -9 $server_pid
        exit 1
    fi
done

echo "Test passed"
kill -9 $server_pid
exit 0
