# LSEG
# Workflow
## 'logs-analyser'

- An action to analyze the csv format logs based on a .log file

## Inputs

- `file` (required): File path.

# Python Script
- `read_file` - Reads the log file and returns a dictionary of lines.
- `extract_job` - Extracts jobs from the logs by matching START and END lines for each task ID. 
- `severity` - Analyzes each parsed job and calculates the duration.

## Example Usage

```yaml
      - name: Set up Python
        uses: actions/setup-python@v5.6.0
        with:
          python-version: '3.11'
          
      - name: Logs Analyzer
      - run: |
          echo "Start analyzing the logs..."
          python3 logs-pattern.py ${{ inputs.file_path }}
```