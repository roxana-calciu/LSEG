import time
import warnings
import sys

def read_file(file_path):
    """
    Reads the log file and returns a dictionary of lines.
    Each line is stored with its line number as key (starting at 1).
    
    Example:
    {
        1: "11:35:23,scheduled task 032, START,37980",
        2: "11:35:56,scheduled task 032, END,37980",
        ...
    }
    """
    log_dict = {}

    with open(file_path, "r") as f:
        for i, line in enumerate(f, start=1):
            log_dict[i] = line.strip()
    return log_dict


def extract_job(logs):
    """
    Extracts jobs from the logs by matching START and END lines for each task ID.
    
    Returns a dictionary:
    {
        line_num: {
            'startTime': '11:35:23',
            'endTime': '11:35:56',
            'jobName': 'scheduled task 032',
            'status': 'START',
            'taskId': '37980'
        },
        ...
    }

    Note: It only includes lines with START, and populates their END time later by matching the same taskId.
    """
    task_dict = {}

    for line_num, line in logs.items():
        if 'START' in line:
            parts = line.split(',')
            task_dict[line_num] = {
                'startTime': parts[0],
                'endTime': None,
                'jobName': parts[1],
                'status': 'START',
                'taskId': parts[3]
            }

    for line in logs.values():
        if 'END' in line:
            parts = line.split(',')
            task_id = parts[3]
            end_time = parts[0]

            for job in task_dict.values():
                if job['taskId'] == task_id and job['endTime'] is None:
                    job['endTime'] = end_time
                    break  

    return task_dict


def severity(parsed_logs):
    """
    Analyzes each parsed job and calculates the duration.
    - Prints an ERROR if the job took more than 10 minutes (600 seconds)
    - Warns if the job took more than 5 minutes (300 seconds)

    Skips incomplete or malformed jobs safely.
    """
    for key, values in parsed_logs.items():
        start = values.get('startTime')
        end = values.get('endTime')
        job = values.get('jobName', 'Unknown')
        task = values.get('taskId', 'Unknown')

        if not start or not end or not isinstance(start, str) or not isinstance(end, str):
            print(f"Skipping incomplete log entry {key} → {values}")
            continue

        try:
            start_time = time.strptime(start, '%H:%M:%S')
            end_time = time.strptime(end, '%H:%M:%S')
            duration = time.mktime(end_time) - time.mktime(start_time)

            if duration > 600:
                print(f"ERROR: Job {job} with Task ID {task} exceeded 10 minutes ({duration:.1f} seconds)")
            elif duration > 300:
                warnings.warn(f"WARNING: Job {job} with Task ID {task} took too long: {duration:.1f} seconds")

        except Exception as e:
            print(f"Unexpected error at entry {key}: {e} → {values}")


def main():
    """
    Entry point of the script.
    - Reads the log file
    - Extracts job info
    - Analyzes duration and logs warnings/errors
    """
    if len(sys.argv) < 2:
        print("Usage: python3 filter-logs.py <log_file>")
        return

    file_path = sys.argv[1]
    log_dict = read_file(file_path)
    parsed_logs = extract_job(log_dict)
    severity(parsed_logs)


if __name__ == "__main__":
    main()
