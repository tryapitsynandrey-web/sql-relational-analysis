import json
import glob
import re
from pathlib import Path

for nb_file in glob.glob('/Users/andrewshwarts/Documents/Git_main/sql-relational-analysis/analysis/notebooks/*.ipynb'):
    with open(nb_file, 'r') as f:
        nb = json.load(f)
        
    first_cell = nb['cells'][0]
    source = "".join(first_cell['source'])
    
    sql_file_match = re.search(r"with open\('../../sql/analysis/(.*?)', 'r'\) as f:", source)
    if not sql_file_match:
        sql_file_match = re.search(r"sql_path.*'sql'.*'analysis'.*'(.*?)'", source)
        if not sql_file_match:
            print(f"Match failed for {nb_file}")
            continue
        
    sql_file = sql_file_match.group(1)
    
    # Locate where the df assignments begin
    df_part = source[source.find('df1 = pd.read_sql'):]
    
    new_source = (
        "import os\n"
        "import pandas as pd\n"
        "import psycopg2\n"
        "import matplotlib.pyplot as plt\n"
        "import re\n"
        "from pathlib import Path\n"
        "from IPython.display import display\n"
        "from dotenv import load_dotenv\n"
        "\n"
        "load_dotenv()\n"
        "\n"
        f"sql_path = Path(__file__).resolve().parent.parent.parent / 'sql' / 'analysis' / '{sql_file}'\n"
        "\n"
        "with open(sql_path, 'r') as f:\n"
        "    sql_script = f.read()\n"
        "\n"
        "queries = [q.strip() for q in re.split(r'(?m)^-- \\d+\\. .*$', sql_script) if q.strip()]\n"
        "queries = queries[1:]\n"
        "\n"
        "with psycopg2.connect(\n"
        "    host=os.environ.get('DB_HOST', os.environ.get('POSTGRES_HOST', 'localhost')),\n"
        "    port=os.environ.get('DB_PORT', os.environ.get('POSTGRES_PORT', '5432')),\n"
        "    user=os.environ.get('DB_USER', os.environ.get('POSTGRES_USER', 'postgres')),\n"
        "    password=os.environ.get('DB_PASSWORD', os.environ.get('POSTGRES_PASSWORD', 'postgres')),\n"
        "    dbname=os.environ.get('DB_NAME', os.environ.get('POSTGRES_DB', 'olist'))\n"
        ") as conn:\n"
    )
    
    for line in df_part.split('\n'):
        if line.strip() == '':
            new_source += "\n"
        elif line.startswith('df'):
            new_source += f"    {line}\n"
        else:
            new_source += f"{line}\n"
            
    # Clean up excess newlines
    new_source = new_source.strip() + "\n"
    
    # Format properly for Jupyter cells
    lines = new_source.split('\n')
    formatted_source = [line + '\n' for line in lines[:-1]]
    
    first_cell['source'] = formatted_source
    
    with open(nb_file, 'w') as f:
        json.dump(nb, f, indent=1)

print("Done refactoring notebooks")
