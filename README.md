# retire-scan
## Overview:
This script is designed to scan a specified file or directory for known vulnerabilities using Retire.js. It prompts the user for a path, checks if Retire.js is installed (installing it if necessary), and then runs a Retire.js scan on the provided path.

## Prerequisites:
Node.js and npm should be installed on your system.

## Usage:
- Run the Script
    - Execute the script from your terminal:
      
      ```
      ./script_name.sh
      ```
- Provide Path
    - When prompted, enter the file or directory path you want to scan.
      
- Scan Results
    - The script will install Retire.js if it is not already installed.
    - It will then run a Retire.js scan on the specified path and display the results.
 

## Demo:

![Screenshot_20240708_180712](https://github.com/pratiyk/audit-scanner/assets/38837970/d34b163e-f5e6-4ebc-a192-0d7d274d3c65)

![retire-scan](https://github.com/pratiyk/audit-scanner/assets/38837970/23340df5-4833-4537-9563-5bfe1c1831ba)

-------

# generate-pie-chart
## Overview:
This Python script reads a Retire.js JSON output file, processes the vulnerabilities by severity, and generates an HTML file containing a pie chart visualizing the severity distribution using D3.js.

## Requirements:
- Python 3.x
- `d3.js` (loaded from CDN in the HTML file)
- No additional Python libraries are required

## Demo:

![image](https://github.com/user-attachments/assets/7913cdc0-6176-4abd-869b-f89bf20c3bb9)

![image](https://github.com/user-attachments/assets/0738c87b-4cdd-4a1e-9429-d26d7b5edc8c)


