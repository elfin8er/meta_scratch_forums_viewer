from scratch import convert_sb3_to_py as decompile

sb3_file = 'Live Forum Feed [Updates Daily].sb3'
python_output_file = "output_script.py"

try:
    decompile(sb3_file, python_output_file)
    print(f"Decompilation successful! Python code saved to {python_output_file}")
except Exception as e:
    print(f"An error occurred during decompilation: {e}")