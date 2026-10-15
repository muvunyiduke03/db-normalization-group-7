# First Normal Form (1NF)

## Columns that violated 1NF

The pipe-delimited columns contained more than one value in a cell: `WorkerSkills`, `WorkerCertifications`, `SupplierPhones`, `MaterialSupplied`, `MaterialUnitCost`, `EquipmentUsed`, and `EquipmentRentalCost`.

## How values were made atomic

Each value separated by `|` was written as its own row in a dedicated CSV. Material names remain paired with their unit costs by their original position, and equipment names remain paired with their rental costs the same way. The `*Position` fields preserve list order. Each output row contains only one value for each attribute.

The scalar fields from each original record remain in [1NF_Construction_Records.csv](1NF_Construction_Records.csv). The repeating values are in [1NF_Worker_Skills.csv](1NF_Worker_Skills.csv), [1NF_Worker_Certifications.csv](1NF_Worker_Certifications.csv), [1NF_Supplier_Phones.csv](1NF_Supplier_Phones.csv), [1NF_Materials.csv](1NF_Materials.csv), and [1NF_Equipment.csv](1NF_Equipment.csv).

## Rows or tables created

Both. The original records were assigned `SourceRowID` values 1 through 15. Each pipe-separated item became an atomic row in its corresponding CSV, linked to the original record by `SourceRowID`. Material/cost and equipment/cost pairs are kept on the same child row. This avoids creating artificial combinations among separate lists.

## Row-identifying keys

- In `1NF_Construction_Records.csv`, `SourceRowID` identifies a row.
- In each child CSV, the composite of `SourceRowID` and its position column identifies a row: `SkillPosition`, `CertificationPosition`, `PhonePosition`, `MaterialPosition`, or `EquipmentPosition` as appropriate.

`SourceRowID` is a generated identifier for the source CSV row, not a claim about the dataset's natural business key. This submission addresses atomicity and row identification for 1NF only; it intentionally does not attempt the dependency-based decompositions of later normal forms.
