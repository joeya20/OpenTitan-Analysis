from pathlib import Path
import subprocess
import csv
import argparse
import pathlib
import subprocess
import json
import os
import shutil
import re

visited = set()
my_count  = 0

def getPRData(url):
    if(url in visited):
        return
    visited.add(url)
    print(f"fetching {url}...")
    proc = subprocess.run(['gh', 'pr', 'view', '-R', 'https://github.com/lowRISC/opentitan', f'{url}', '--json', 'number,mergeCommit,files'], capture_output=True, text=True)
    
    resp_json = json.loads(proc.stdout)
    files_json = resp_json['files']
    pr_number = resp_json['number']
    merge_oid = resp_json['mergeCommit']['oid']
    new_path = Path("v2")
    # print(files_json)
    os.chdir("opentitan")
    subprocess.run(['git', 'checkout', merge_oid])
    os.chdir("..")
    
    os.mkdir(new_path.joinpath(str(pr_number)))
    for file in files_json:
        file_name = str(file['path']).split('/')[-1]
        if os.path.exists(Path('opentitan').joinpath(file['path']).as_posix()) and str(file['path']).__contains__('/rtl/'):
            shutil.copy(Path('opentitan').joinpath(file['path']).as_posix(), new_path.joinpath(str(pr_number)).as_posix())
            # os.rename(file_name, file['path'])
        
    os.chdir("opentitan")
    subprocess.run(['git', 'checkout', merge_oid + '^'])
    os.chdir("..")
    
    os.mkdir(new_path.joinpath(str(pr_number) + '^'))
    for file in files_json:
        file_name = str(file['path']).split('/')[-1]
        if os.path.exists(Path('opentitan').joinpath(file['path']).as_posix()) and str(file['path']).__contains__('/rtl/'):
            shutil.copy(Path('opentitan').joinpath(file['path']).as_posix(), new_path.joinpath(str(pr_number) + '^').as_posix())
            # os.rename(file_name, file['path'])
                    
# def getDiff(url):
#     proc = subprocess.run(['gh', 'pr', 'diff', '-R', 'https://github.com/lowRISC/opentitan', f'{url}'], capture_output=True, text=True)
#     pr_num = str(url).split('/')[-1]
#     if pr_num == "":
#         print(url)
#     write_line = True
#     with open(f'diff/{pr_num}_diff.txt', 'w') as diff_file:
#         for line in proc.stdout.splitlines():
#             if line.startswith("diff --git"):
#                 if line.strip().endswith('.sv'):
#                     # print(line + ";")
#                     write_line = True
#                 else:
#                     write_line = False
#             if write_line:
#                 diff_file.write(line + '\n')
    
# def parseDiff():
#     for diff in os.listdir('diff'):
#         with open(f'diff/{diff}') as diff_file:
#             pr_num = str(diff).split('_')[0]
#             with open(f'additions/{pr_num}.txt', 'w') as additions_file:
#                 with open(f'deletions/{pr_num}.txt', 'w') as deletions_file:
#                     addition = re.compile(r"^\+([ \t]+.*)")
#                     deletion = re.compile(r"^\-([ \t]+.*)")
#                     for line in diff_file.readlines():
#                         add_match = addition.match(line)
#                         del_match = deletion.match(line)
#                         if add_match is not None:
#                             additions_file.write(add_match.group(1))
#                             additions_file.write('\n')
#                         if del_match is not None:
#                             deletions_file.write(del_match.group(1))
#                             deletions_file.write('\n')
    
def main():    
    # call sv_diff
    # arg_parser = argparse.ArgumentParser()
    # arg_parser.add_argument("directory")
    # args = arg_parser.parse_args()
    # get_diff(args)
    # with open('ot_pr_ast_diff_test.csv', newline='', mode='+w') as csv_file:
    #     field_names = ['pr_number', 'file', 'node', 'count']
    #     writer = csv.DictWriter(csv_file, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(args.rows)
    
    # get pr diffs
    ot = Path("opentitan")    
    if not ot.is_dir:
        print("could not find opentitan directory")
        return
    with open('2023-08-04.csv',  newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            pr_url = row['PR URL']
            if pr_url != None and pr_url != '':
                getPRData(pr_url)
    print(my_count)
    # parse diff to extract deletions and additions
    # parseDiff()
    
    # call sv_diff to extract syntax nodes
    # rows = []
    # for addition in os.listdir('additions'):
    #     proc = subprocess.run(['./sv_diff', f'additions/{addition}'], capture_output=True, text=True)
    #     nodes = proc.stdout.splitlines()
    #     pr = addition.split('.')[0]
    #     for node in nodes:
    #         rows.append(
    #             {
    #                 'pr_number': pr, 
    #                 # 'file': file, 
    #                 'node': node.split(':')[0], 
    #                 'count': node.split(':')[1], 
    #             }
    #         )
    # with open('additions.csv', newline='', mode='w') as csv_file:
    #     field_names = ['pr_number', 'node', 'count']
    #     writer = csv.DictWriter(csv_file, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(rows)
        
    # rows = []
    # for deletion in os.listdir('deletions'):
    #     proc = subprocess.run(['./sv_diff', f'deletions/{deletion}'], capture_output=True, text=True)
    #     nodes = proc.stdout.splitlines()
    #     pr = deletion.split('.')[0]
    #     for node in nodes:
    #         rows.append(
    #             {
    #                 'pr_number': pr, 
    #                 # 'file': file, 
    #                 'node': node.split(':')[0], 
    #                 'count': node.split(':')[1], 
    #             }
    #         )
    # with open('deletions.csv', newline='', mode='w') as csv_file:
    #     field_names = ['pr_number', 'node', 'count']
    #     writer = csv.DictWriter(csv_file, fieldnames=field_names)
    #     writer.writeheader()
    #     writer.writerows(rows)
    
    
if __name__ == "__main__":
    main()