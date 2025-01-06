import os
import subprocess

def create_requirements_txt():
    if os.path.exists('requirements.txt'):
        print("A requirements.txt file already exists.")
        choice = input("Do you want to (u)pdate it, (o)verwrite it, or (s)kip? [u/o/s]: ").lower()
        
        if choice == 'u':
            update_requirements()
        elif choice == 'o':
            generate_new_requirements()
        elif choice == 's':
            print("Skipping requirements.txt generation.")
        else:
            print("Invalid choice. Skipping requirements.txt generation.")
    else:
        generate_new_requirements()

def update_requirements():
    try:
        subprocess.check_call(['pip', 'install', 'pipreqs'])
        subprocess.check_call(['pipreqs', '.', '--savepath', 'new_requirements.txt'])
        
        with open('requirements.txt', 'r') as old_file, open('new_requirements.txt', 'r') as new_file:
            old_reqs = set(old_file.read().splitlines())
            new_reqs = set(new_file.read().splitlines())
        
        updated_reqs = old_reqs.union(new_reqs)
        
        with open('requirements.txt', 'w') as updated_file:
            updated_file.write('\n'.join(sorted(updated_reqs)))
        
        os.remove('new_requirements.txt')
        print("Requirements.txt file updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error updating Requirements.txt: {e}")

def generate_new_requirements():
    try:
        subprocess.check_call(['pip', 'install', 'pipreqs'])
        subprocess.check_call(['pipreqs', '.', '--force'])
        print("Requirements.txt file created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error creating Requirements.txt: {e}")

def create_readme():
    if os.path.exists('README.md'):
        print("A README.md file already exists.")
        choice = input("Do you want to overwrite it? [y/n]: ").lower()
        if choice != 'y':
            print("Skipping README.md creation.")
            return

    readme_content = """# Project Name

Brief description of your project.

## Installation

```
pip install -r requirements.txt
```

## Usage

Explain how to use your project.

## Contributing

Guidelines for contributing to your project.

## License

Specify your project's license.
"""

    with open('README.md', 'w') as f:
        f.write(readme_content)
    print("README.md file created successfully.")

def main():
    create_requirements_txt()
    create_readme()

if __name__ == "__main__":
    main()
