"""Code to run after generating the project."""

import shutil

shutil.rmtree("licenses")

project_slug = '{{project_slug}}'
create_python_classes = '{{create_python_classes}}'

if create_python_classes == "No":
    print("TODO - cleanup python")

print("** PROJECT CREATION COMPLETE **\n")
print("Next steps:")
print("cd {{project_name}}")
print("make setup")
