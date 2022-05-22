
call hydromt build wflow ../../3_models/wflow "{'basin': [34.33,-20.12,34.95,-19.30], 'outlets': true}" -i wflow_build.ini --dd -vv
call hydromt update wflow ../../3_models/wflow -i wflow_update_forcing.ini -d .\era5.yml -vv

call ../bin/wflow_cli_v0.5.2/bin/wflow_cli.exe wflow_sbm.toml