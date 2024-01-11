# clear-demand
Coding Test for Clear Demand

Visual Representation of the ERD

1. Product Table
This is a central table.
It has one-to-many relationships with the Inventory and MarkdownPlan tables.
Key: ProductID (Primary Key).
2. Inventory Table
Linked to the Product table.
Each inventory record is associated with one product.
Key: InventoryID (Primary Key).
3. MarkdownPlan Table
Linked to the Product table.
Each markdown plan is specific to one product.
Key: MarkdownPlanID (Primary Key).
4. SalesData Table
Linked to the MarkdownPlan table.
Each sales data entry is associated with one markdown plan.
Key: SalesDataID (Primary Key).
5. DailyMetrics Table
Linked to the SalesData table.
Each set of daily metrics corresponds to one sales data entry.
Key: MetricsID (Primary Key).

Database Schema
The main entities are Products, Inventory, Markdown Plans, and Sales Data. Let's define these entities and their relationships.

Entities and Attributes
1. Product
ProductID (Primary Key): A unique identifier, such as a UPC.
Description: A brief description of the product.
Cost: The cost to the store owner for acquiring the product.
RegularPrice: The regular selling price of the product.
2. Inventory
InventoryID (Primary Key)
ProductID (Foreign Key): Links to the Product.
QuantityOnHand: The number of units available.
Date: The specific date for the inventory count.
3. MarkdownPlan
MarkdownPlanID (Primary Key)
ProductID (Foreign Key): Links to the Product.
StartDate: The beginning date for the markdown.
EndDate: The target end date for the markdown.
InitialReduction: The initial price reduction percentage.
MidwayReduction: The midway price reduction percentage.
FinalReduction: The final day price reduction percentage.
4. SalesData
SalesDataID (Primary Key)
MarkdownPlanID (Foreign Key): Links to the Markdown Plan.
Date: The date of the sale.
UnitsSold: The number of units sold that day.
SellPrice: The selling price on that day (reflecting markdowns).
5. DailyMetrics
MetricsID (Primary Key)
SalesDataID (Foreign Key): Links to the Sales Data.
UnitsSold: The number of units sold that day.
Margin: Calculated as SellPrice - Cost.
ProfitOrLoss: Calculated for the day.
RemainingInventory: Calculated based on inventory and sales.

Relationships
Product to Inventory: One-to-Many (One product can have many inventory records).
Product to MarkdownPlan: One-to-Many (One product can have multiple markdown plans).
MarkdownPlan to SalesData: One-to-Many (One markdown plan can have multiple sales data entries).
SalesData to DailyMetrics: One-to-One (Each sales data entry has a corresponding daily metric record).
