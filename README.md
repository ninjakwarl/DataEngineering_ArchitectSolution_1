# Modern Data Engineering Architect Solution
📚Proof of Concept Solution to Call SQL Procedure with Azure Functions (Python) using Pandas to ETL into CSV going to Blob Storage.

## Criteria:
- Create simple SQL procedure, which queries some example SQL table
- Create Azure Function HTTP triggered, which calls the procedure
- Azure Function should create Excel file based on query result (1:1) and store it to Blob Storage
- Azure Function code in Python
- Pandas library can be used also SQL Alchemy
- All secrets should be kept in Key Vaults
- Function should be parametrized based from the SQL Procedure (not from code).


I am using sql data from: https://pokeapi.co/api/v2/pokemon/

![image](https://user-images.githubusercontent.com/22649754/162198509-d6a67200-ac27-4152-9823-0bd398eac5e0.png)


