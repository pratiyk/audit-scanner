import json
import sys
import os  
from collections import Counter

# Function to read JSON from a file
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from file {file_path}: {e}")
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")

# Function to extract severity counts from Retire.js scan results
def extract_severity_counts(data):
    if not isinstance(data, dict):
        raise ValueError("Expected data to be a dictionary with library names as keys.")
    
    severity_counter = Counter()
    for library, details in data.items():
        if 'vulnerabilities' in details:
            vulnerabilities = details['vulnerabilities']
            for vulnerability in vulnerabilities:
                severity = vulnerability.get('severity')
                if severity:
                    severity_counter[severity] += 1
    
    return [{"severity": k, "count": v} for k, v in severity_counter.items()]

# Function to generate HTML with D3.js from JSON data
def generate_html_from_json(data, output_file):
    # Generate HTML content
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pie Chart using D3.js</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <style>
            .arc text {{
                font: 12px sans-serif;
                text-anchor: middle;
            }}
        </style>
    </head>
    <body>
        <script>
            // Data
            const data = {json.dumps(data)};
            
            // Dimensions
            const width = 450;
            const height = 450;
            const margin = 40;
            
            // Radius
            const radius = Math.min(width, height) / 2 - margin;
            
            // Append the SVG object
            const svg = d3.select("body")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
            
            // Color scale
            const color = d3.scaleOrdinal()
                .domain(data.map(d => d.severity))
                .range(d3.schemeSet3);
            
            // Compute the position of each group on the pie
            const pie = d3.pie()
                .value(d => d.count);
            
            const data_ready = pie(data);
            
            // Shape helper to build arcs
            const arc = d3.arc()
                .innerRadius(0)
                .outerRadius(radius);
            
            // Build the pie chart
            svg
                .selectAll('pieces')
                .data(data_ready)
                .enter()
                .append('path')
                .attr('d', arc)
                .attr('fill', d => color(d.data.severity))
                .attr("stroke", "black")
                .style("stroke-width", "2px")
                .style("opacity", 0.7);
            
            // Add labels
            svg
                .selectAll('pieces')
                .data(data_ready)
                .enter()
                .append('text')
                .text(d => d.data.severity)
                .attr("transform", d => "translate(" + arc.centroid(d) + ")")
                .style("text-anchor", "middle")
                .style("font-size", 15);
        </script>
    </body>
    </html>
    '''
    
    # Ensure the output path is not a directory
    if os.path.isdir(output_file):
        raise IsADirectoryError(f"The specified output path '{output_file}' is a directory. Please provide a file path.")

    # Write HTML content to file
    with open(output_file, 'w') as file:
        file.write(html_content)
    
    print(f"HTML file generated: {output_file}")

# Main function
def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_pie_chart.py <input_json_file> <output_html_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Ensure the output file path includes a filename
    if os.path.isdir(output_file):
        print(f"The specified output path '{output_file}' is a directory. Please provide a file path including a filename.")
        sys.exit(1)

    # Read data from JSON file
    try:
        data = read_json_file(input_file)
    except ValueError as e:
        print(e)
        sys.exit(1)
    
    # Extract severity counts from Retire.js scan results
    try:
        severity_counts = extract_severity_counts(data)
    except ValueError as e:
        print(e)
        sys.exit(1)
    
    # Generate HTML file
    generate_html_from_json(severity_counts, output_file)

# Run the main function
if __name__ == "__main__":
    main()
