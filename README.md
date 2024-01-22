# ikea_inventory_db
Building DB with tables to hold inventory of all assorted IKEA boxes from assemblies. The purppose of this exercise is to create to database that can be queried on a purchase-by-purchase bundling. The debate of whether to normalize or denormalize this DB is currently aimed towards normalizing. This is because of the very organic and nearly infite combinations possible of items to be purchased. The goal of this practic will be to give a list of dimesions and weights of all boxes from a specific list of products that will be given from a UI. The boxes will be ranked in groups by margins of weight and dimensions (possibly by kg/cm^2 / lbm/in^2 for later calculations of balance). The number of groups per order will vary, but will currently be expected narrowed to 3 or 5 by experiments with standard deviation to be committed later.

DB Structure intended:
Web Scraped Data:
    Main Prod SRC Table:
    Start with a Main Prod SRC Table which will have the URL, product number/name, category break down, count of boxes per purchase, list of box item numbers, count of finish differences (if still varied among product number/name), metadata, updated date (reliant on DAG or manual exectuion), availablity status.
    
    Main Piece SRC Table:
    Get each box from the Prod Table links and store the URL, item number, dimensions (L, W, H independant fields ordered in greatest to least), weight, metadata, updated date (reliant on DAG or manual execution), availablity status.

Notes: Will possible use DEV SRC tables for initial loading to then filter down to recent changes, mainly around finish/new product numbers, availability change (will likely relate )
