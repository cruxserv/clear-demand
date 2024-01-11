# clear-demand
Coding Test for Clear Demand

Database Schema

1. Product Table
ProductID (Primary Key): Unique identifier for the product (e.g., UPC).
Description: Text description of the product.
Cost: The cost for the store owner to acquire or manufacture the product.
RegularPrice: The regular selling price of the product.
2. Inventory Table
InventoryID (Primary Key): Unique identifier for the inventory record.
ProductID (Foreign Key): References ProductID in the Product table.
QuantityOnHand: The number of units available in inventory.
Date: The date of the inventory record.
3. MarkdownPlan Table
MarkdownPlanID (Primary Key): Unique identifier for the markdown plan.
ProductID (Foreign Key): References ProductID in the Product table.
StartDate: The start date of the markdown period.
EndDate: The end date of the markdown period.
InitialReduction: The initial price reduction percentage.
MidwayReduction: The midway price reduction percentage.
FinalReduction: The final price reduction percentage.
4. SalesData Table
SalesDataID (Primary Key): Unique identifier for the sales data record.
ProductID (Foreign Key): References ProductID in the Product table.
MarkdownPlanID (Foreign Key, Nullable): References MarkdownPlanID in the MarkdownPlan table. Can be null if the sale is not part of a markdown.
Date: The date of the sale.
UnitsSold: The number of units sold.
SellPrice: The selling price per unit.

Relationships
Product to Inventory: One-to-Many (One product can have many inventory records).
Product to MarkdownPlan: One-to-Many (One product can have multiple markdown plans).
Product to SalesData: One-to-Many (One product can have multiple sales data records).
MarkdownPlan to SalesData: One-to-Many (One markdown plan can relate to multiple sales data records, but it's optional for a sale record to be linked to a markdown plan).