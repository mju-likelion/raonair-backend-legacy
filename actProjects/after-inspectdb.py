import os
current_dir = os.path.dirname(__file__)

models = open(current_dir + "/App/models.py", "r+")
lines = models.readlines()
tobe_delete_lines = []

for i, line in enumerate(lines):
    new_line = line.lstrip()
    if new_line.startswith('created_at') or new_line.startswith('updated_at'):
        tobe_delete_lines.append(i)

for i in reversed(tobe_delete_lines):
    del lines[i]

models.seek(0)
models.truncate()
for line in lines:
    models.write(line)

models.close()
