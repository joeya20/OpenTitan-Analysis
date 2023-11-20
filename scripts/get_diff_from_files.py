import os
from pathlib import Path
import subprocess
import csv

def get_diff():
    count  = 0
    rows = []
    for pr in os.listdir('v2'):
        pr_path = Path('v2').joinpath(pr)
        if not pr_path.as_posix().endswith('^'):
            count += 1
            for file in os.listdir(pr_path):
                fixed_file_path = pr_path.joinpath(file)
                buggy_file_path = Path(pr_path.as_posix() + '^').joinpath(file)
                print(fixed_file_path)
                print(buggy_file_path)
                proc = subprocess.run(['./sv_diff', f'{fixed_file_path}', f'{buggy_file_path}'], capture_output=True, text=True)
                if proc.stdout == "" or  proc.stdout is None:
                    print(pr_path.as_posix())
                    print(proc.stderr)
                nodes = proc.stdout.splitlines()
                for node in nodes:
                    # print(node)
                    rows.append(
                        {
                            'pr_number': pr, 
                            'file': file, 
                            'node': node.split(':')[0], 
                            'count': node.split(':')[1], 
                        }
                    )
    print(count)
    # with open('diff_data_final_v2.csv', newline='', mode='w') as csv_file:
    #     field_names = ['pr_number', 'file', 'node', 'count']
    #     writer = csv.DictWriter(csv_file, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(rows)
        
def main():
    get_diff()

if __name__=="__main__":
    main()