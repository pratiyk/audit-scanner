import json
import os
from collections import Counter, defaultdict


def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON from file {file_path}: {e}")
    except Exception as e:
        raise ValueError(f"Error reading file {file_path}: {e}")


def extract_severity_counts(data):
    if not isinstance(data, dict):
        raise ValueError("Expected data to be a dictionary with library names as keys.")
    
    severity_counter = Counter()
    vulnerabilities_by_severity = defaultdict(list)
    
    for library, details in data.items():
        if 'vulnerabilities' in details:
            for vulnerability in details['vulnerabilities']:
                severity = vulnerability.get('severity')
                summary = vulnerability['identifiers'].get('summary', 'N/A')
                fixes = vulnerability.get('info', [])
                fix_links = ', '.join(f'<a href="{fix}" target="_blank">{fix}</a>' for fix in fixes)
                
                if severity:
                    severity_counter[severity] += 1
                    vulnerabilities_by_severity[severity].append({
                        'library': library,
                        'severity': severity,
                        'summary': summary,
                        'fix': fix_links
                    })
    
    return severity_counter, vulnerabilities_by_severity


def generate_html_from_json(severity_counts, vulnerabilities_by_severity, output_file):
   
    severity_data = [{"severity": k, "count": v} for k, v in severity_counts.items()]

   
    color_map = {
        'low': '#28a745',
        'medium': '#ffc107',
        'high': '#dc3545',
        'critical': '#dc3545' 
    }

    
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vulnerability Report</title>
        <script src="https://d3js.org/d3.v7.min.js"></script>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Roboto', sans-serif;
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                background-color: #f5f5f5;
            }}
            h1 {{
                margin-top: 20px;
                color: #333;
            }}
            #pie-chart {{
                margin-top: 10px;
                width: 90%;
                max-width: 450px;
                height: 450px;
            }}
            table {{
                width: 90%;
                max-width: 1000px;
                margin-top: 30px;
                border-collapse: collapse;
                background-color: #fff;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                border-spacing: 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
                word-wrap: break-word;
            }}
            th {{
                background-color: #007BFF;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            tr:hover {{
                background-color: #ddd;
            }}
            .arc text {{
                font: 12px sans-serif;
                text-anchor: middle;
            }}
            .table-container {{
                width: 90%;
                max-width: 1200px;
                margin: 0 auto;
            }}
            .low-severity {{ border-left: 5px solid #28a745; }}
            .medium-severity {{ border-left: 5px solid #ffc107; }}
            .high-severity {{ border-left: 5px solid #dc3545; }}
            th.library, td.library {{ width: 25%; }}
            th.severity, td.severity {{ width: 15%; }}
            th.summary, td.summary {{ width: 40%; }}
            th.fix, td.fix {{ width: 20%; }}
            @media (max-width: 768px) {{
                table {{
                    width: 100%;
                }}
            }}
        </style>
    </head>
    <body>
        <h1>Vulnerability Report</h1>
        
        <!-- Pie Chart -->
        <div id="pie-chart"></div>
        
        <script>
            // Data for Pie Chart
            const data = {json.dumps(severity_data)};
            
            // Define colors
            const colorMap = {json.dumps(color_map)};
            
            // Dimensions
            const width = document.getElementById('pie-chart').clientWidth;
            const height = width;
            const margin = 40;
            
            // Radius
            const radius = Math.min(width, height) / 2 - margin;
            
            // Append the SVG object
            const svg = d3.select("#pie-chart")
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
            
            // Color scale
            const color = d3.scaleOrdinal()
                .domain(data.map(d => d.severity))
                .range(Object.values(colorMap));
            
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
                .attr("stroke", "white")
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
        
        <!-- Vulnerabilities Tables -->
        <div class="table-container">
            <h2>Low Severity Vulnerabilities</h2>
            <table class="low-severity">
                <tr>
                    <th class="library">Library</th>
                    <th class="summary">Summary</th>
                    <th class="fix">Fix</th>
                </tr>
                {''.join(f'''
                <tr>
                    <td class="library">{vul['library']}</td>
                    <td class="summary">{vul['summary']}</td>
                    <td class="fix">{vul['fix']}</td>
                </tr>
                ''' for vul in vulnerabilities_by_severity.get('low', []))}
            </table>
            
            <h2>Medium Severity Vulnerabilities</h2>
            <table class="medium-severity">
                <tr>
                    <th class="library">Library</th>
                    <th class="summary">Summary</th>
                    <th class="fix">Fix</th>
                </tr>
                {''.join(f'''
                <tr>
                    <td class="library">{vul['library']}</td>
                    <td class="summary">{vul['summary']}</td>
                    <td class="fix">{vul['fix']}</td>
                </tr>
                ''' for vul in vulnerabilities_by_severity.get('medium', []))}
            </table>
            
            <h2>High Severity Vulnerabilities</h2>
            <table class="high-severity">
                <tr>
                    <th class="library">Library</th>
                    <th class="summary">Summary</th>
                    <th class="fix">Fix</th>
                </tr>
                {''.join(f'''
                <tr>
                    <td class="library">{vul['library']}</td>
                    <td class="summary">{vul['summary']}</td>
                    <td class="fix">{vul['fix']}</td>
                </tr>
                ''' for vul in vulnerabilities_by_severity.get('high', []))}
            </table>
            
            <h2>Critical Severity Vulnerabilities</h2>
            <table class="critical-severity">
                <tr>
                    <th class="library">Library</th>
                    <th class="summary">Summary</th>
                    <th class="fix">Fix</th>
                </tr>
                {''.join(f'''
                <tr>
                    <td class="library">{vul['library']}</td>
                    <td class="summary">{vul['summary']}</td>
                    <td class="fix">{vul['fix']}</td>
                </tr>
                ''' for vul in vulnerabilities_by_severity.get('critical', []))}
            </table>
        </div>
    </body>
    </html>
    '''
    
    if os.path.isdir(output_file):
        raise ValueError(f"{output_file} is a directory. Please provide a file path.")
    
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    print(f"HTML file generated: {output_file}")


def main():
    input_file = input("Enter the path to the JSON file: ")
    output_file = input("Enter the path for the output HTML file: ")

    try:
        data = read_json_file(input_file)
        severity_counts, vulnerabilities_by_severity = extract_severity_counts(data)
    except ValueError as e:
        print(e)
        return
    
    
    generate_html_from_json(severity_counts, vulnerabilities_by_severity, output_file)

if __name__ == "__main__":
    main()
