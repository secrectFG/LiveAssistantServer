call .venv\Scripts\activate.bat
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. grpc.proto
echo "done"
pause