import java.util.*;
/*
Name: Rushil Venkateswar
Roll Number: 20CS30045
Assignment 1
*/

public class program {    
    class entity {
        int unique_ID;
        String name;
        String joining_date;

        public entity(Scanner Obj) {
            Random rand = new Random();
            this.unique_ID = rand.nextInt(9000000) + 1000000;//code to assign a 7 digit random number

            Obj.nextLine();
            System.out.println("Enter the name of the Entity.");
            this.name = Obj.nextLine();
            System.out.println("Enter joining date of Entity(in YYYY-MM-DD format).");
            this.joining_date = Obj.next(); //pass date as YYYY-MM-DD
        }
    }

    class manufacturer extends entity {
        //list of all manufacturers
        static List<manufacturer> mf_list = new ArrayList<manufacturer>();
        //product list unique to each manufacturer
        List<product> pdt_list = new ArrayList<product>();

        public manufacturer(Scanner Obj) {
            super(Obj);
            mf_list.add(this);
        }

        static manufacturer find_by_ID(int ID) {
            for(manufacturer mf : mf_list) {
                if(mf.unique_ID == ID)
                    return mf;
            }

            return null;
        }

        //function to print all the manufacturers
        public static void print_all() {
            System.out.println("Unique ID\t\tName\t\tJoining Date");
            for(manufacturer mf : mf_list) {
                System.out.println(mf.unique_ID+"\t\t"+mf.name+"\t\t"+mf.joining_date);
            }
        }

        public static void delete(Scanner Obj) {
            System.out.println("Here is the list of all the manufacturers on our website:\n");
            print_all();
            System.out.println("\nWarning! Deleting manufacturer entry will delete the products listed by it as well!\nEnter ID to be deleted:");
            int ID = Obj.nextInt();
            manufacturer mf = manufacturer.find_by_ID(ID);
            if(mf != null) {
                mf_list.remove(mf);
                mf.pdt_list.clear();
                mf = null;
                System.out.println("Manufacturer with ID: "+ID+" deleted.");
            }
            else {
                System.out.println("Manufacturer with ID: "+ID+" does not exist.");
            }
        }

        void list_products() {
            System.out.println("Product ID\t\tProduct Name");
            for(product pd : this.pdt_list) {
                System.out.println(pd.unique_ID+"\t\t"+pd.name);
            }
        }

        //add a product to an existing manufacturer
        void add_product(Scanner Obj) {
            System.out.println("Here is the list of all the products on our website:\n");
            product.print_all();
            System.out.println("\nDo you want to add an existing product to this manufacturer(enter '1' without the quotes) or do you want to create a new product listing(enter '0' without the quotes)?");
            int existing_pd = Obj.nextInt();
            if(existing_pd == 1) {
                System.out.println("Enter unique ID of the product");
                int pd_ID = Obj.nextInt();
                product pd = product.find_by_ID(pd_ID);
                if(pd != null) {
                    this.pdt_list.add(pd); //add product to product list of this manufacturer
                    pd.mf = this; //add this manufacturer as the manufacturer of this product
                }
            }
            else {
                product new_pd = new product(Obj);
                this.pdt_list.add(new_pd);
                new_pd.mf = this;
            }
        }
    }

    class customer extends entity { 
        static List<customer> cm_list = new ArrayList<customer>();
        int zipcode;
        int order_ID;
        int order_qty;

        Map<product, Integer> purchased_pdts = new HashMap<product, Integer>();

        public customer(Scanner Obj) {
            super(Obj);
            cm_list.add(this);
            System.out.println("Enter zipcode of customer.");
            this.zipcode = Obj.nextInt();
        }

        static customer find_by_ID(int ID) {
            for(customer cm : cm_list) {
                if(cm.unique_ID == ID)
                    return cm;
            }

            return null;
        }

        public static void print_all() {
            System.out.println("Unique ID\t\tName\t\tJoining Date");
            for(customer cm : cm_list) {
                System.out.println(cm.unique_ID+"\t\t"+cm.name+"\t\t"+cm.joining_date);
            }
        }

        public static void delete(Scanner Obj) {
            System.out.println("Here is the list of all the customers on our website:\n");
            print_all();
            System.out.println("\nEnter ID to be deleted:");
            int ID = Obj.nextInt();
            customer cm = customer.find_by_ID(ID);
            if(cm != null) {
                cm_list.remove(cm);
                cm = null;
                System.out.println("Customer with ID: "+ID+" deleted.");
            }
            else {
                System.out.println("Customer with ID: "+ID+" does not exist.");
            }
        }

        void add_order(Scanner Obj) {
            System.out.println("List of all products:");
            product.print_all();
            System.out.println("Enter the product ID, followed by the quantity of the product you want.");
            this.order_ID = Obj.nextInt();
            this.order_qty = Obj.nextInt();
        }

        void process_order(Scanner Obj) {
            add_order(Obj);

            shops_and_warehouses nearest_shop = shops_and_warehouses.get_nearest(this.zipcode);
            product pd = product.find_by_ID(this.order_ID);

            if((nearest_shop != null) && (pd != null)) {
                if(nearest_shop.inventory.get(pd) != null || nearest_shop.inventory.get(pd) >= this.order_qty) {
                    int stock = nearest_shop.inventory.get(pd);
                    nearest_shop.inventory.put(pd, stock - this.order_qty); //product gets allotted to customer and hence its stock goes down by required number of unit
                    delivery_agent final_da = delivery_agent.assign(this.zipcode); //delivery agent is assigned to the customer
                    if(final_da != null) {
                        System.out.println("Your delivery agent is: "+final_da.name+", with the joining date: "+final_da.joining_date+" and Unique ID = "+final_da.unique_ID);
                        final_da.num_products++;
                        this.purchased_pdts.put(pd, this.order_qty);
                    }
                }
                else {
                    System.out.println("Sorry, the item is currently out of stock.");
                }
            }
            else {
                System.out.println("Sorry, no shops available in your zipcode. Order could not be processed.");
            }
        }

        void list_purchases() {
            System.out.println("Product ID\t\tProduct Name\t\tQuantity Ordered");
            for(Map.Entry<product, Integer> order : this.purchased_pdts.entrySet()) {
                product pd = order.getKey();
                int qty = order.getValue();
                System.out.println(pd.unique_ID+"\t\t"+pd.name+"\t\t"+qty);
            }
        }
    }

    class product extends entity {
        static List<product> pd_list = new ArrayList<product>();
        manufacturer mf;
        List<shops_and_warehouses> sw_list = new ArrayList<shops_and_warehouses>();

        public product(Scanner Obj) {
            super(Obj);
            pd_list.add(this);
        }

        static product find_by_ID(int ID) {
            for(product pd : pd_list) {
                if(pd.unique_ID == ID)
                    return pd;
            }

            return null;
        }

        void add_manufacturer(Scanner Obj) {
            System.out.println("Here is the list of all the manufacturers on our website:\n");
            manufacturer.print_all();
            System.out.println("\nDo you want to add this product to an existing manufacturer(enter '1' without the quotes) or do you want to create a new manufacturer listing(enter '0' without the quotes)?");
            int existing_mf = Obj.nextInt();
            if(existing_mf == 1) {
                System.out.println("Enter unique ID of the manufacturer");
                int mf_ID = Obj.nextInt();
                manufacturer mf = manufacturer.find_by_ID(mf_ID);
                if(mf != null) {
                    mf.pdt_list.add(this); //add product to product list of this manufacturer
                    this.mf = mf; //add this manufacturer as the manufacturer of this product
                }
            }
            else {
                manufacturer new_mf = new manufacturer(Obj);
                new_mf.pdt_list.add(this);
                this.mf = new_mf;

            }
        }

        public static void print_all() {
            System.out.println("Unique ID\t\tName\t\tJoining Date");
            for(product pd : pd_list) {
                System.out.println(pd.unique_ID+"\t\t"+pd.name+"\t\t"+pd.joining_date);
            }
        }

        public static void delete(Scanner Obj) {
            System.out.println("Here is the list of all the products on our website:\n");
            print_all();
            System.out.println("\nWarning! Deleting product will remove it from Manufacturer's product list and Shops & Warehouses' inventory as well!\nEnter ID to be deleted:");
            int ID = Obj.nextInt();
            product pd = product.find_by_ID(ID);
            if(pd != null) {
                for(shops_and_warehouses sw : pd.sw_list) {
                    sw.remove_from_inventory(pd);
                }
                pd.mf.pdt_list.remove(pd);
                pd = null;
                System.out.println("Product with ID: "+ID+" deleted.");
            }
            else {
                System.out.println("Product with ID: "+ID+" does not exist.");
            }
            
        }
    }

    class shops_and_warehouses extends entity {
        static List<shops_and_warehouses> sw_list = new ArrayList<shops_and_warehouses>();
        int zipcode;
        Map<product, Integer> inventory = new HashMap<product, Integer>();

        public shops_and_warehouses(Scanner Obj) {
            super(Obj);
            sw_list.add(this);
            System.out.println("Enter the zipcode of this Shop/Warehouse.");
            this.zipcode = Obj.nextInt();
        }

        static shops_and_warehouses find_by_ID(int ID) {
            for(shops_and_warehouses sw : sw_list) {
                if(sw.unique_ID == ID)
                    return sw;
            }

            return null;
        }

        public void remove_from_inventory(product pd) {
            this.inventory.remove(pd);
        }

        public static void print_all() {
            System.out.println("Unique ID\t\tName\t\tJoining Date");
            for(shops_and_warehouses sw : sw_list) {
                System.out.println(sw.unique_ID+"\t\t"+sw.name+"\t\t"+sw.joining_date);
            }
        }

        public static void delete(Scanner Obj) {
            System.out.println("Here is the list of all the Shops/Warehouses on our website:\n");
            print_all();
            System.out.println("\nWarning! Deleting Shop/Warehouse will remove the products listed in its inventory as well!\nEnter ID to be deleted:");
            int ID = Obj.nextInt();
            shops_and_warehouses sw = shops_and_warehouses.find_by_ID(ID);
            if(sw != null) {
                sw.inventory.clear();
                sw_list.remove(sw);
                sw = null;
                System.out.println("Shop/Warehouse with ID: "+ID+" deleted.");
            }
            else {
                System.out.println("Shop/Warehouse with ID: "+ID+" does not exist.");
            }
        }

        void add_copies(Scanner Obj) {
            System.out.println("Here is the list of all the products on our website:\n");
            product.print_all();
            System.out.println("\nDo you want to create a new product or add one of these to the inventory? Enter 1 for new product and 0 otherwise.");
            if(Obj.nextInt() == 1) {
                product new_pd = new product(Obj);
                System.out.println("Enter the quantity of the product you want to add to inventory:");
                int num = Obj.nextInt();
                new_pd.sw_list.add(this);
                this.inventory.put(new_pd, num);
            }
            else {
                System.out.println("Enter the number and ID of the product that you'd like to add to Shop/Warehouse: "+this.name+", with unique ID: "+this.unique_ID);
                int num = Obj.nextInt();
                int pd_ID = Obj.nextInt();
                product pd = product.find_by_ID(pd_ID);
                if(pd != null) {
                    if(this.inventory.containsKey(pd)) { //if product already exists in inventory
                        int val = this.inventory.get(pd);
                        val += num; //increase the product count
                        this.inventory.put(pd, val);
                    }
                    else { //if product doesn't exist in inventory
                        this.inventory.put(pd, num);
                    }
                }
                else {
                    System.out.println("Product with ID: "+pd_ID+" does not exist.");
                }
            }
        }

        static shops_and_warehouses get_nearest(int zipcode) {
            for(shops_and_warehouses sw : sw_list) {
                if(sw.zipcode == zipcode) {
                    return sw;
                }
            }

            return null;
        }

        void list_inventory() {
            System.out.println("Product ID\t\tProduct Name\t\tQuantity Stocked");
            for(Map.Entry<product, Integer> order : this.inventory.entrySet()) {
                product pd = order.getKey();
                int qty = order.getValue();
                System.out.println(pd.unique_ID+"\t\t"+pd.name+"\t\t"+qty);
            }
        }
    }

    class delivery_agent extends entity {
        static List<delivery_agent> da_list = new ArrayList<delivery_agent>();
        int zipcode;
        int num_products;

        public delivery_agent(Scanner Obj) {
            super(Obj);
            System.out.println("Enter the zipcode of this agent:");
            this.zipcode = Obj.nextInt();
            this.num_products = 0;
            da_list.add(this);
        }

        static delivery_agent find_by_ID(int ID) {
            for(delivery_agent da : da_list) {
                if(da.unique_ID == ID)
                    return da;
            }

            return null;
        }

        public static void print_all() {
            System.out.println("Unique ID\t\tName\t\tJoining Date");
            for(delivery_agent da : da_list) {
                System.out.println(da.unique_ID+"\t\t"+da.name+"\t\t"+da.joining_date);
            }
        }

        public static void delete(Scanner Obj) {
            System.out.println("Here is the list of all the delivery agents on our website:\n");
            print_all();
            System.out.println("\nEnter ID to be deleted:");
            int ID = Obj.nextInt();
            delivery_agent da = delivery_agent.find_by_ID(ID);
            if(da != null) {
                da = null;
                System.out.println("Delivery Agent with ID: "+ID+" deleted.");
            }
            else {
                System.out.println("Delivery Agent with ID: "+ID+" does not exist.");
            }
        }

        //finds agent with least number of products delivered (returns null if no agent in your zipcode)
        static delivery_agent assign(int zipcode) {
            int count = 9999999;
            delivery_agent final_da = null;
            for(delivery_agent da : da_list) {
                if(da.zipcode == zipcode) {
                    if(da.num_products < count) {
                        count = da.num_products;
                        final_da = da;
                    }
                }
            }

            return final_da;
        }
    }

    public static void main(String[] args) {
        program ob = new program();
        Scanner sc = new Scanner(System.in);

        char quit=' ';
        manufacturer mf = null;
        customer cm = null;
        product pd = null;
        shops_and_warehouses sw = null;
        delivery_agent da = null;

        System.out.println("Welcome to our Online Medicine Delivery Network!");
        do {
            System.out.println("Please enter 1 to create Manufacturer, 2 to create Customer, 3 to create Product(as well as the manufacturer), 4 to create Shop/Warehouse(as well as the inventory), 5 to create Delivery Agent or any other number to skip.");
            switch(sc.nextInt()) {
                case 1:
                    mf = ob.new manufacturer(sc);
                    break;
                case 2:
                    cm = ob.new customer(sc);
                    break;
                case 3:
                    pd = ob.new product(sc);
                    pd.add_manufacturer(sc);
                    break;
                case 4:
                    sw = ob.new shops_and_warehouses(sc);
                    System.out.println("Would you like to add a product along with its count to the inventory of this shop? Enter 1 if yes and 0 if no.");
                    if(sc.nextInt() == 1) {
                        sw.add_copies(sc);
                    }
                    break;
                case 5:
                    da = ob.new delivery_agent(sc);
                    break;
                default:
                    System.out.println("Skipped");
            }

            System.out.println("Please enter 1 to print all Manufacturers, 2 to print all Customers, 3 to print all Products, 4 to print all Shops/Warehouses, 5 to print all Delivery Agents or any other number to skip.");
            switch(sc.nextInt()) {
                case 1:
                    manufacturer.print_all();
                    break;
                case 2:
                    customer.print_all();;
                    break;
                case 3:
                    product.print_all();
                    break;
                case 4:
                    shops_and_warehouses.print_all();
                    break;
                case 5:
                    delivery_agent.print_all();
                    break;
                default:
                    System.out.println("Skipped."); 
            }

            System.out.println("Please enter 1 to delete a Manufacturer, 2 to delete a Customer, 3 to delete a Product, 4 to delete a Shop/Warehouse, 5 to delete a Delivery Agent or any other number to skip.");
            switch(sc.nextInt()) {
                case 1:
                    manufacturer.delete(sc);
                    break;
                case 2:
                    customer.delete(sc);;
                    break;
                case 3:
                    product.delete(sc);
                    break;
                case 4:
                    shops_and_warehouses.delete(sc);
                    break;
                case 5:
                    delivery_agent.delete(sc);
                    break;
                default:
                    System.out.println("Skipped.");
            }
            
            System.out.println("Following are the other functions available to you:(enter the number to execute that function)");
            System.out.println("1. Add a product to newly created manufacturer");
            System.out.println("2. Add a certain number of copies of a product to a shop");
            System.out.println("3. Add and Process an order of a product from a customer");
            System.out.println("4. List all the purchases made by a customer");
            System.out.println("5. List the inventory of a shop");
            System.out.println("6. List the products made by a manufacturer");
            System.out.println("Enter Choice(or any other number to skip):");

            switch(sc.nextInt()) {
                case 1:
                    mf.add_product(sc);
                    break;
                case 2:
                    if(shops_and_warehouses.sw_list.isEmpty() || product.pd_list.isEmpty()) {
                        System.out.println("Request cannot be processed due to one or more missing entities");
                        break;
                    }
                    sw.add_copies(sc);
                    break;
                case 3:
                    if(customer.cm_list.isEmpty() || product.pd_list.isEmpty() || shops_and_warehouses.sw_list.isEmpty() || delivery_agent.da_list.isEmpty()) {
                        System.out.println("Order cannot be processed due to one or more missing entities.");
                        break;
                    }
                    cm.process_order(sc);
                    break;
                case 4:
                    if(customer.cm_list.isEmpty()) {
                        System.out.println("Customer list is empty.");
                        break;
                    }
                    System.out.println("Enter ID of the customer whose purchases you want to view");
                    customer.print_all();
                    int cm_ID = sc.nextInt();
                    customer target_c = customer.find_by_ID(cm_ID);
                    if(target_c != null) {
                        target_c.list_purchases();
                    }
                    else {
                        System.out.println("The customer with ID: "+cm_ID+" does not exist.");
                    }
                    break;
                case 5:
                    if(shops_and_warehouses.sw_list.isEmpty()) {
                        System.out.println("Shops and Warehouses list is empty.");
                        break;
                    }
                    System.out.println("Enter ID of the shop whose inventory you want to view");
                    shops_and_warehouses.print_all();
                    int sw_ID = sc.nextInt();
                    shops_and_warehouses target_sw = shops_and_warehouses.find_by_ID(sw_ID);
                    if(target_sw != null) {
                        target_sw.list_inventory();
                    }
                    else {
                        System.out.println("Shop/Warehouse with ID: "+sw_ID+" does not exist.");
                    }
                    break;
                case 6:
                    if(manufacturer.mf_list.isEmpty()) {
                        System.out.println("Manufacturer list is empty.");
                        break;
                    }
                    System.out.println("Enter ID of the manufacturer whose products you want to view");
                    manufacturer.print_all();
                    int mf_ID = sc.nextInt();
                    manufacturer target_mf = manufacturer.find_by_ID(mf_ID);
                    if(target_mf != null) {
                        target_mf.list_products();
                    }
                    else {
                        System.out.println("Manufacturer with ID: "+mf_ID+" does not exist.");
                    }
                    break;
                default:
                    System.out.println("Skipped.");
            }
            System.out.println("To quit, press 'q'(without the quotes). To go back to beginning, enter any other character.");
            quit = sc.next().charAt(0);

        }while(quit != 'q');
        sc.close();
    }
}