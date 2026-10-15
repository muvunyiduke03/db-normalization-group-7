# Second Normal Form (2NF)

## Composite keys

The project-assignment record is identified by the composite key `(ProjectID, WorkerName, SupplierName)`. The corresponding CSV is [2NF_Project_Assignments.csv](2NF_Project_Assignments.csv). Its key columns also form foreign keys to the project, worker, and supplier tables.

The atomic child tables have composite keys as well:

- Assignment skills: `(ProjectID, WorkerName, SupplierName, SkillPosition)`
- Assignment certifications: `(ProjectID, WorkerName, SupplierName, CertificationPosition)`
- Assignment materials: `(ProjectID, WorkerName, SupplierName, MaterialPosition)`
- Assignment equipment: `(ProjectID, WorkerName, SupplierName, EquipmentPosition)`
- Supplier phones: `(SupplierName, PhonePosition)`

The prior 1NF files used generated `SourceRowID` values. For this dependency-based stage, the assignment's natural composite key is made explicit. It is unique for all 15 source records.

## Partial dependencies found

In the combined source record, project descriptive and client/supervisor columns depended on `ProjectID` alone; worker phone and hourly rate depended on `WorkerName` alone; supplier city and supplier phone values depended on `SupplierName` alone. Each determinant is a proper subset of the assignment key, so keeping those facts on the assignment would create partial dependencies.

The source does not support moving worker skills or certifications to a worker-only table: those lists vary between assignments for the same worker. Materials and equipment also vary between project/supplier records. They remain associated with the full assignment key rather than assuming dependencies not supported by the data.

## Data moved into separate tables

- Project details, including the client and supervisor columns, are in [2NF_Projects.csv](2NF_Projects.csv).
- Worker phone and hourly rate are in [2NF_Workers.csv](2NF_Workers.csv).
- Supplier city is in [2NF_Suppliers.csv](2NF_Suppliers.csv), and supplier phones are in [2NF_Supplier_Phones.csv](2NF_Supplier_Phones.csv).
- Assignment-specific skills, certifications, materials/costs, and equipment/rental costs are in [2NF_Assignment_Skills.csv](2NF_Assignment_Skills.csv), [2NF_Assignment_Certifications.csv](2NF_Assignment_Certifications.csv), [2NF_Assignment_Materials.csv](2NF_Assignment_Materials.csv), and [2NF_Assignment_Equipment.csv](2NF_Assignment_Equipment.csv).

## Primary keys and foreign keys

- `2NF_Projects`: primary key `ProjectID`.
- `2NF_Workers`: primary key `WorkerName`.
- `2NF_Suppliers`: primary key `SupplierName`.
- `2NF_Project_Assignments`: composite primary key `(ProjectID, WorkerName, SupplierName)`; each column is a foreign key to its corresponding entity table.
- `2NF_Supplier_Phones`: composite primary key `(SupplierName, PhonePosition)`; `SupplierName` is a foreign key to `2NF_Suppliers`.
- Each assignment child table has the assignment composite key plus its position column as primary key; the three assignment columns together are a foreign key to `2NF_Project_Assignments`.

CSV files cannot enforce database constraints, so these primary and foreign keys are represented by their columns and documented design.

## Why the design is in 2NF

The project, worker, and supplier facts that depended on only part of the composite assignment key have been moved to relations keyed by those determinants. Assignment-specific child values use the entire assignment key plus a position to identify each atomic value. Therefore, every non-key attribute in the composite-key relations depends on the whole key, not just a proper subset. This is the 2NF decomposition; it does not claim to resolve transitive dependencies or multi-valued dependencies reserved for later stages.
