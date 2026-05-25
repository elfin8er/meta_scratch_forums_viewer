from datetime import datetime
from scratch import transpile_to_json as transpile
from scratch import save_sb3

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

sb_input_file = 'Live Forum Feed [Updates Daily].sb3'
python_source_file = open("./outputs/script.py").read()
json_output_file = f"output_{timestamp}.json"
sb_output_file = f"output_{timestamp}.sb3"

print(f"Transpiling {python_source_file} to {json_output_file}...")
json_str = transpile(python_source_file)
with open(json_output_file, "w") as f:
    f.write(json_str)

save_sb3(json_str, sb_output_file, source_sb3=sb_input_file)