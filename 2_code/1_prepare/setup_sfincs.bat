hydromt build sfincs ../../3_models/sfincs/00_base "{'bbox': [34.33,-20.12,34.95,-19.30]}" -i build_sfincs.ini -d ../../1_data/1_static/static_data.yml -vv
hydromt update sfincs ../../3_models/sfincs/00_base -o ../../3_models/sfincs/00_base_riv -i update_sfincs_rivers.ini -d ../../1_data/1_static/static_data.yml -vv