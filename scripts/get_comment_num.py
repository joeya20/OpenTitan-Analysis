import subprocess
import csv
import json
import argparse
import pathlib

def get_discussion(issues):
    comments = dict()
    for issue_pr_pair in issues:
        issue = issue_pr_pair['issue']
        pr = issue_pr_pair['pr']
        issue_pr_comments = []
        
        print(f"fetching {issue}")
        # get issue comments
        if issue != None and issue != '':
            proc = subprocess.run(['gh', 'issue', 'view', '-R', 'https://github.com/lowRISC/opentitan', f'{issue}', '--json', 'body,comments'], capture_output=True, text=True)
            resp_json = json.loads(proc.stdout)
            issue_pr_comments.append(resp_json['body'])
            for comment in resp_json['comments']:
                issue_pr_comments.append(comment['body'])

        # get pr comments
        if pr != None and pr != '':
            proc = subprocess.run(['gh', 'pr', 'view', '-R', 'https://github.com/lowRISC/opentitan', f'{pr}', '--json', 'body,comments'], capture_output=True, text=True)
            resp_json = json.loads(proc.stdout)
            issue_pr_comments.append(resp_json['body'])
            for comment in resp_json['comments']:
                issue_pr_comments.append(comment['body'])
            
        comments[issue] = issue_pr_comments
        
    with open("comments.json", "w") as json_file:
        json.dump(comments, json_file)
        
def get_comment_count(issues):
    rows = []
    
    for issue_pr_pair in issues:
        issue = issue_pr_pair['issue']
        pr = issue_pr_pair['pr']
        
        print(f"fetching {issue}")
        # get issue comments
        if issue != None and issue != '':
            proc = subprocess.run(['gh', 'issue', 'view', '-R', 'https://github.com/lowRISC/opentitan', f'{issue}', '--json', 'comments'], capture_output=True, text=True)
            resp_json = json.loads(proc.stdout)
            issue_comment_count = len(resp_json['comments'])

        # get pr comments
        if pr != None and pr != '':
            proc = subprocess.run(['gh', 'pr', 'view', '-R', 'https://github.com/lowRISC/opentitan', f'{pr}', '--json', 'comments'], capture_output=True, text=True)
            resp_json = json.loads(proc.stdout)
            pr_comment_count = len(resp_json['comments'])
            
        rows.append({
            'issue number': issue,
            'issue comment count': issue_comment_count,
            'pr comment count': pr_comment_count,
        })
        
    with open('ot_comment_count.csv', newline='', mode='w') as csv_file:
        field_names = ['issue number', 'issue comment count', 'pr comment count']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(rows)
    
def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("read_path")
    args = arg_parser.parse_args()
    args.repo = "https://github.com/lowRISC/opentitan"
    
    abs_path_r = pathlib.Path(args.read_path).absolute()
    
    # get data
    args.rows = []
    with open(abs_path_r,  newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        issues = []
        for row in csv_reader:
            issues.append(
                {
                    'issue': row['number'],
                    'pr' : row['PR URL']
                }
            )
        get_discussion(issues)
    
if __name__=='__main__':
    main()