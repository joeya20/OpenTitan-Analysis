import csv
import argparse
import pathlib
import subprocess
import json

visited = set()

def getPRData(url, number, args):
    if(url in visited):
        return
    visited.add(url)
    print(f"fetching {url}...")
    proc = subprocess.run(['gh', 'pr', 'view', '-R', f'{args.repo}', f'{url}', '--json', 'files,number'], capture_output=True, text=True)
    resp_json = json.loads(proc.stdout)
    if url == "https://github.com/lowRISC/opentitan/pull/10138":
        print(proc.stdout)
    files_json = resp_json['files']
    pr_number = resp_json['number']
    for file in files_json:
        args.rows.append({
            'issue_number': number, 
            'pr_number': pr_number,
            'pr_url': url, 
            'path': file['path'], 
            'additions': file['additions'], 
            'deletions': file['deletions']
        })

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("read_path")
    arg_parser.add_argument("write_path")
    args = arg_parser.parse_args()
    args.repo = "https://github.com/lowRISC/opentitan"
    
    abs_path_r = pathlib.Path(args.read_path).absolute()
    abs_path_w = pathlib.Path(args.write_path).absolute()
    
    # get data
    args.rows = []
    with open(abs_path_r,  newline='', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            number = row['number']
            url = row['PR URL']
            if url != None and url != '':
                getPRData(url, number, args)
    # print(args.rows)
    # write csv
    with open(abs_path_w, newline='', mode='+w') as csv_file:
        field_names = ['issue_number', 'pr_number', 'pr_url', 'path', 'additions', 'deletions']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(args.rows)
    
if __name__=="__main__":
    main()
