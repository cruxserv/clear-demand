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
Cost: The cost to the store owner for acquiring the product (mandatory field).
RegularPrice: The regular selling price of the product (mandatory field).
2. Inventory
InventoryID (Primary Key)
ProductID (Foreign Key): Links to the Product (mandatory field).
QuantityOnHand: The number of units available (mandatory field).
Date: The specific date for the inventory count (mandatory field).
3. MarkdownPlan
MarkdownPlanID (Primary Key)
ProductID (Foreign Key): Links to the Product (mandatory field).
StartDate: The beginning date for the markdown (mandatory field).
EndDate: The target end date for the markdown (mandatory field).
InitialReduction: The initial price reduction percentage (mandatory field).
MidwayReduction: The midway price reduction percentage.
FinalReduction: The final day price reduction percentage.
4. SalesData
SalesDataID (Primary Key)
MarkdownPlanID (Foreign Key): Links to the Markdown Plan.
ProductID (Foreign Key): Links to the Product (mandatory field).
Date: The date of the sale (mandatory field).
UnitsSold: The number of units sold that day (mandatory field).
SellPrice: The selling price on that day (reflecting markdowns) (mandatory field).
5. DailyMetrics
MetricsID (Primary Key)
SalesDataID (Foreign Key): Links to the Sales Data (mandatory field).
UnitsSold: The number of units sold that day (mandatory field).
Margin: Calculated as SellPrice - Cost.
ProfitOrLoss: Calculated for the day.
RemainingTotalInventory: Calculated based on inventory and sales.

Relationships
Product to Inventory: One-to-Many (One product can have many inventory records).
Product to MarkdownPlan: One-to-Many (One product can have multiple markdown plans).
MarkdownPlan to SalesData: One-to-Many (One markdown plan can have multiple sales data entries).
SalesData to DailyMetrics: One-to-One (Each sales data entry has a corresponding daily metric record).
