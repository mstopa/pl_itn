# Placeholder


# Generate proto
python3 -m grpc_tools.protoc --proto_path=pl_itn_service/proto=pl_itn_api --python_out=.  --grpc_python_out=. pl_itn_api/api.proto
