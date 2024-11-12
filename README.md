# Flow Log Parser

## Description

This project is a Python program that parses flow log data and maps each flow log entry to a tag based on a provided lookup table. The lookup table is a CSV file containing mappings of destination port and protocol combinations to tags.

The program generates an output file containing:

- **Count of matches for each tag**
- **Count of matches for each port/protocol combination**

## Assumptions

- **Flow Log Format**: The program only supports the **default flow log format** (version 2). Custom log formats are not supported.
- **Protocol Mapping**: The program maps protocol numbers to protocol names for TCP (`6`), UDP (`17`), ICMP (`1`), and other common protocols. Unknown protocols are categorized as `'other'`.
- **Case Insensitivity**: Matching of protocols and tags is case-insensitive.
- **Input File Sizes**:
  - The flow log file size can be up to **10 MB**.
  - The lookup table can have up to **10,000 mappings**.

## Requirements

- **Python Version**: The program is compatible with **Python 3**.
- **Libraries**: Only standard Python libraries are used. No external libraries or packages like Hadoop, Spark, Pandas, etc., are required.

## How to Run the Program

### 1. Prepare Input Files

- **Flow Log File**: Ensure you have a flow log file in the default format (version 2). Example filename: `flow_logs.txt`.
- **Lookup Table File**: Prepare a CSV file containing the tag mappings with the following columns: `dstport`, `protocol`, `tag`. Example filename: `lookup_table.csv`.

### 2. Run the Program

Open a terminal, navigate to the project directory, and execute the following command:

```bash
python3 flow_log_parser.py flow_logs.txt lookup_table.csv output.txt
```

- Replace `flow_logs.txt` with the path to your flow log file.
- Replace `lookup_table.csv` with the path to your lookup table file.
- Replace `output.txt` with the desired path for the output file.

### 3. View the Output

The program will generate an output file containing:

- **Tag Counts**: Counts of matches for each tag.
- **Port/Protocol Combination Counts**: Counts of matches for each port/protocol combination.

Example content of `output.txt`:

```
Tag Counts:

Tag,Count
sv_p1,2
sv_p2,1
email,3
untagged,8

Port/Protocol Combination Counts:

Port,Protocol,Count
443,tcp,1
...
```

## Tests Performed

### Test 1: Basic Functionality Test

- **Objective**: Verify that the program correctly maps flow log entries to tags based on the lookup table.
- **Procedure**:
  - Used the provided sample flow logs and lookup table.
  - Ran the program and compared the output with the expected counts.
- **Result**: The program's output matched the expected results, confirming correct functionality.

### Test 2: Case Insensitivity Test

- **Objective**: Ensure matching is case-insensitive for protocols and tags.
- **Procedure**:
  - Modified the protocol names and tags in the lookup table to various cases (e.g., 'TCP', 'udp', 'Sv_P1').
  - Ran the program and verified that tags were correctly assigned.
- **Result**: The program correctly assigned tags regardless of case, confirming case-insensitive matching.

### Test 3: Missing Fields in Flow Logs

- **Objective**: Test how the program handles flow log entries with missing fields.
- **Procedure**:
  - Added flow log entries with missing fields to simulate incomplete data.
  - Ran the program and checked for errors or crashes.
- **Result**: The program skipped invalid entries without crashing, demonstrating robustness.

### Test 4: Handling Unknown Protocols

- **Objective**: Verify the handling of unknown protocol numbers.
- **Procedure**:
  - Added flow log entries with protocol numbers not in the `protocol_map` (e.g., ‘99’).
  - Ran the program and observed that these entries were categorized under 'other' and processed accordingly.
- **Result**: The program handled unknown protocols without errors.

### Test 5: Edge Port Numbers

- **Objective**: Test the program with edge port numbers (e.g., ‘0’, ‘65535’).
- **Procedures**:
  - Added flow log entries with destination ports ‘0’ and ‘65535’.
  - Updated the lookup table to include mappings for these ports.
  - Ran the program and verified correct tagging.
- **Results**: The program correctly processed entries with edge port numbers.

### Test 6: All Entries Untagged

- **Objective**: Check the program’s behavior when none of the flow log entries match the lookup table.
- **Procedures**:
  - Used a lookup table that doesn’t include any of the ports/protocols from the flow logs.
  - Ran the program and ensured all entries were counted under 'untagged'.
- **Results**: All entries were correctly counted as 'untagged'.

### Test 7: Special Characters in Tags

- **Objective**: Verify the program handles tags with special characters.
- **Procedures**:
  - Added tags with special characters (e.g., ‘sv_P#1’, ‘email-service@domain’) in the lookup table.
  - Ran the program and observed that tags were assigned correctly.
- **Results**: The program handled tags with special characters without issues.

### Test 8: Non-Standard Protocols

- **Objective**: Test the program with protocols other than TCP, UDP, and ICMP.
- **Procedures**:
  - Added entries with protocol numbers for GRE (‘47’) and ESP (‘50’).
  - Updated the protocol_map to include these protocols.
  - Ran the program and observed the tagging.
- **Results**: After updating the `protocol_map`, the program correctly processed these protocols.

## Analysis

- **Performance**: The program is efficient in processing large files, thanks to line-by-line reading and the use of dictionaries for quick lookups.
- **Code Quality**:
  - **Modularity**: Functions are well-organized, making the code maintainable and easy to understand.
  - **Readability**: Code includes comments and follows good naming conventions.
- **Limitations**:
  - The program does not support custom flow log formats.
  - Only protocol numbers '1', '6', '17', '47', '50', '51', '58', '89', and '132' are explicitly mapped; others are categorized as 'other'.
- **Potential Improvements**:
  - Allow users to specify additional protocol mappings via a configuration file.
  - Enhance error reporting and logging.
  - Support custom flow log formats if needed.

## Files Included in the Repository

- `flow_log_parser.py`: The main Python script.
- `README.md`: This README file with instructions and information.
- Sample input files (in each test folder):
  - `tests/test1/flow_logs.txt`: Sample flow log file.
  - `tests/test1/lookup_table.csv`: Sample lookup table.

## Contact Information

If you have any questions or need further assistance, please feel free to reach out:

- **Email**: [lizonglun120@gmail.com](mailto:lizonglun120@gmail.com)
- **GitHub**: [Darren221](https://github.com/Darren221)