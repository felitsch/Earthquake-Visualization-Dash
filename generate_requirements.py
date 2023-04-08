import os
import re
import subprocess
import sys

def main():
    pip_path = os.path.join(sys.prefix, 'bin', 'pip')
    
    output = subprocess.check_output([pip_path, 'freeze']).decode('utf-8')
    clean_requirements = []

    for line in output.splitlines():
        if line.startswith('-e') or line.startswith('--editable') or '@' in line:
            parts = re.split(r'[=<>@]', line)
            if len(parts) >= 3:
                package_name, package_version = parts[0], parts[2]
                clean_line = f"{package_name}=={package_version}"
            else:
                continue
        else:
            clean_line = line
        clean_requirements.append(clean_line)

    with open('requirements.txt', 'w') as f:
        f.write('\n'.join(clean_requirements))

if __name__ == "__main__":
    main()
