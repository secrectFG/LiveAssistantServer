call conda activate py37
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc.proto
pause