from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import webbrowser
import threading
import time
import socket
#functions

#DataFrames
df_p=pd.read_csv("products.csv" , encoding='ISO-8859-1')
df_od=pd.read_csv("order_details.csv" , encoding='ISO-8859-1')
df_cat=pd.read_csv("categories.csv" , encoding='ISO-8859-1')
df_orders=pd.read_csv("orders.csv" , encoding='ISO-8859-1')
df_ship_providers=pd.read_csv("shippers.csv" , encoding='ISO-8859-1')
df_cust=pd.read_csv("customers.csv" , encoding='ISO-8859-1')
df_orders['orderDate'] = pd.to_datetime(df_orders['orderDate'], format='%Y-%m-%d')
df_orders['requiredDate'] = pd.to_datetime(df_orders['requiredDate'], format='%Y-%m-%d')
df_orders['shippedDate'] = pd.to_datetime(df_orders['shippedDate'], format='%Y-%m-%d')
df_orders['shipperID'] = df_orders['shipperID'].astype(int)

#functions
def total_sale(df,quantity,unitPrice,discount):
    sale=(df['unitPrice']*
                   df['quantity'])-((df['unitPrice']*
                    df['quantity']) *
                    df['discount'])
    return sale
def categorize_consistency(score):
    if score > 200:
        return 'rating: Excellent, description: Costs vary by <5% from mean',
            
              
        
    elif 100 < score <= 200:
        return 'rating: Good, description: Costs vary by 5-10%'
           
            
        
    elif 50 < score <= 100:
        return 'rating: Moderate, description: Costs vary by 10-20%'
            
            
        
    else:
        return 'rating: Poor, description: Costs vary by >20%'
            
            
        
#merge
merged_all= pd.merge(df_od,df_orders, on='orderID', how='inner')
merged_all['orderDate'] =  pd.to_datetime(merged_all['orderDate'])
sales=pd.DataFrame()
#sales['orderDate']=merged_all['orderDate'].dt.to_timestamp()
sales['orderDate'] =merged_all['orderDate'] 
sales['Sales']=(merged_all['unitPrice']*
                   merged_all['quantity'])-((merged_all['unitPrice']*
                    merged_all['quantity']) *
                    merged_all['discount'])
sales['productID']=merged_all['productID']
sales['customerID']=merged_all['customerID']
#print(sales)

#day_sales
days_sales= sales.groupby(sales['orderDate'].dt.date)['Sales'].sum()
day_array = days_sales.to_numpy()
day_labels = days_sales.index.to_numpy()

days_sales=pd.DataFrame()
days_sales['orderDate']=day_labels
days_sales['Sales']=day_array
#print(days_sales)
#print(days_sales)
#print(day_array)
#print(day_labels)
max_index_day = days_sales['Sales'].idxmax()
row_with_max_day = days_sales[days_sales['Sales'] == days_sales['Sales'].max()]

max_sales_date_day = row_with_max_day['orderDate'].iloc[0]  # Get the first date with the max sales
max_sales_value_day = row_with_max_day['Sales'].iloc[0]

#-------------------------------
min_index_day = days_sales['Sales'].idxmin()

row_with_min_day= days_sales[days_sales['Sales'] == days_sales['Sales'].min()]


min_sales_date_day = row_with_min_day['orderDate'].iloc[0]  # Get the date with the min sales
min_sales_value_day = row_with_min_day['Sales'].iloc[0]  # Get the sales value for that date


#-------------------------------


#month_sales
month_sales= sales.groupby(sales['orderDate'].dt.to_period('M'))['Sales'].sum()
month_array = month_sales.to_numpy()
month_labels = month_sales.index.to_numpy()
#print(month_array)
#print(month_labels)

month_sales=pd.DataFrame()
month_sales['orderDate']=month_labels
month_sales['orderDate'] = month_sales['orderDate'].dt.to_timestamp()
month_sales['orderDate'] = pd.to_datetime(month_sales['orderDate'])
month_sales['orderDate']=month_sales['orderDate'].dt.to_period('M')
month_sales['orderDate']=month_sales['orderDate'].astype(str)
month_sales['Sales']=month_array
#print(month_sales)

max_index_month = month_sales['Sales'].idxmax()
row_with_max_month = month_sales[month_sales['Sales'] == month_sales['Sales'].max()]

max_sales_date_month = row_with_max_month['orderDate'].iloc[0]  # Get the first date with the max sales
max_sales_value_month = row_with_max_month['Sales'].iloc[0]

#-------------------------------
min_index_month = month_sales['Sales'].idxmin()

row_with_min_month= month_sales[month_sales['Sales'] == month_sales['Sales'].min()]


min_sales_date_month = row_with_min_month['orderDate'].iloc[0]  # Get the date with the min sales
min_sales_value_month = row_with_min_month['Sales'].iloc[0]  # Get the sales value for that date


#-------------------------------




#year_sales
year_sales= sales.groupby(sales['orderDate'].dt.year)['Sales'].sum()
year_array = year_sales.to_numpy()
year_labels = year_sales.index.to_numpy()
#print(year_array)
#print(year_labels)

year_sales=pd.DataFrame()
year_sales['orderDate']=year_labels
year_sales['orderDate']=year_sales['orderDate'].astype(str)
year_sales['Sales']=year_array
#print(year_sales)

#-----------------------------
max_index_year = year_sales['Sales'].idxmax()
row_with_max_year = year_sales[year_sales['Sales'] == year_sales['Sales'].max()]

max_sales_date_year = row_with_max_year['orderDate'].iloc[0]  # Get the first date with the max sales
max_sales_value_year = row_with_max_year['Sales'].iloc[0]

#-------------------------------
min_index_year = year_sales['Sales'].idxmin()

row_with_min_year= year_sales[year_sales['Sales'] == year_sales['Sales'].min()]


min_sales_date_year = row_with_min_year['orderDate'].iloc[0]  # Get the date with the min sales
min_sales_value_year = row_with_min_year['Sales'].iloc[0]  # Get the sales value for that date

#-----------------------




#------------------------------------
#product-sales
product_sales= sales.groupby(sales['productID'])['Sales'].sum()
product_array = product_sales.to_numpy()
product_labels = product_sales.index.to_numpy()
#print(product_sales)
#print(product_array)
#print(product_labels)
product_sales=pd.DataFrame()
product_sales['productID']=product_labels
product_sales['Sales']=product_array
max_index = sales['Sales'].idxmax()
min_index = sales['Sales'].idxmin()

#-----------------------------
max_index_product = product_sales['Sales'].idxmax()
row_with_max_product = product_sales[product_sales['Sales'] == product_sales['Sales'].max()]

max_sales_date_product = row_with_max_product['productID'].iloc[0]  # Get the first date with the max sales
max_sales_value_product = row_with_max_product['Sales'].iloc[0]

#-------------------------------
min_index_product =product_sales['Sales'].idxmin()

row_with_min_product= product_sales[product_sales['Sales'] == product_sales['Sales'].min()]


min_sales_date_product = row_with_min_product['productID'].iloc[0]  # Get the date with the min sales
min_sales_value_product = row_with_min_product['Sales'].iloc[0]  # Get the sales value for that date

#-----------------------

#customer_key
customer_sales= sales.groupby(sales['customerID'])['Sales'].sum()
customer_sales_df = customer_sales.reset_index()
customer_array = customer_sales.to_numpy()
customer_labels = customer_sales.index.to_numpy()
customer_sales_df=pd.DataFrame(customer_sales)
#print(customer_sales)
#print(customer_array)
#print(customer_labels)

top_sales = customer_sales_df.nlargest(3, 'Sales')
#print(top_sales)
customer_1_id = top_sales.index[0]
customer_1 = top_sales.iloc[0].values[0]

customer_2_id = top_sales.index[1]
customer_2 = top_sales.iloc[1].values[0]

customer_3_id = top_sales.index[2]
customer_3 = top_sales.iloc[2].values[0]

#print(f"first: {customer_1} ;id: {customer_1_id} , sec:{customer_2} ; id: {customer_2_id} , their:{customer_3} ; id: {customer_3_id}")

#shipper_concs
merged_ship_group=merged_all.groupby(merged_all['shipperID'])['freight'].sum()

ship_array = merged_ship_group.to_numpy()
ship_labels = merged_ship_group.index.to_numpy()


Shippers_df = pd.DataFrame({
    'shipperID': ship_labels,
    'total freight': ship_array
})
merged_ship_name= pd.merge(Shippers_df,df_ship_providers, on='shipperID', how='inner')

ship_costs_stat = df_orders.groupby('shipperID')['freight'].describe()
ship_costs_stat_reset = ship_costs_stat[['mean', 'std']].reset_index()
merged_ship_name = pd.merge(merged_ship_name, ship_costs_stat_reset,
                            on='shipperID', how='inner')


merged_ship_name['CV'] = merged_ship_name['std'] / merged_ship_name['mean']

merged_ship_name['Consistency_Score'] = (1 / merged_ship_name['CV']) * 100

shippers_id = merged_ship_name['shipperID'].to_numpy()
c_s_array = merged_ship_name['Consistency_Score'].to_numpy()


print(c_s_array)
sorted_indices = np.argsort(c_s_array)
cS_rank = shippers_id[sorted_indices[:3]]
print()

#print(ship_costs_stat)


#----------------

#dash
# Initialize Dash app

external_stylesheets = ['/assets/custom.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout =html.Div(
                     children=[
  html.Div(
    style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '0px',
           'backgroundColor': 'rgba(255, 255, 255, 0.8)'},
    children=[
        html.Img(
            src='/assets/1d65b272-0568-4b09-bc06-2c5ffada914b_removalai_preview.png',
            style={
                'marginLeft': '0px',
                'marginRight': '0px',
                'height': '150px',
                'width': '250px',
                'marginLeft':'0px'
            }
        ),
        html.H3(
            children=[
                "Northwind Traders Analysis Dashboard",
                
            ],
            style={
                'textAlign': 'center',
                'marginBottom': '0px',
                'marginRight': '0px',
                'marginLeft': '100px',
                #'backgroundColor': 'rgba(255, 255, 255, 0.8)',
                'fontSize': '100px',
                'marginTop':'0px',
                'font-size': '40px'
            }
        )
    ]
)
#----------------
   ,
    html.Hr(),
   html.Div(
    
    children=[
     html.H2(
        'Day Sales Trends',
        style={
            'textAlign': 'center',
            'marginBottom': '5px',
            'font-size': '40px',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)'
        }
    ),
    dcc.Graph(figure=px.line(days_sales, x='orderDate', y='Sales')),
   
    html.H4([
    f"Maximum Day:{max_sales_date_day} , Revenue: {max_sales_value_day}$", html.Br(),
    f"Minumum Day:{min_sales_date_day} , Revenue: {min_sales_value_day}$" 
    
]
            ,style={
            'textAlign': 'center',
            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
            'marginTop':'0px',
            'font-size': '30px'
        })
])
  ,html.Hr(),
  #-----------------------------

   html.Div(
    
    children=[
     html.H2(
        'Month Sales Trends',
        style={
            'textAlign': 'center',
            'marginBottom': '5px',
            'font-size': '40px',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)'
        }
    ),
    dcc.Graph(figure=px.line(month_sales, x='orderDate', y='Sales')),
   
    html.H4([
    f"Maximum Month:{max_sales_date_month} , Revenue: {max_sales_value_month}$", html.Br(),
    f"Minumum Month:{min_sales_date_month} , Revenue: {min_sales_value_month}$" 
    
]
            ,style={
            'textAlign': 'center',
            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
            'marginTop':'0px',
            'font-size': '30px'
        })
]),
  #-----------------------------
  html.Hr(),
   html.Div(
    
    children=[
     html.H2(
        'Year Sales Trends',
        style={
            'textAlign': 'center',
            'marginBottom': '5px',
            'font-size': '40px',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)'
        }
    ),
    dcc.Graph(figure=px.line(year_sales, x='orderDate', y='Sales')),
   
    html.H4([
    f"Maximum Year:{max_sales_date_year} , Revenue: {max_sales_value_year}$", html.Br(),
    f"Minumum Yearay:{min_sales_date_year} , Revenue: {min_sales_value_year}$" 
    
]
            ,style={
            'textAlign': 'center',
            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
            'marginTop':'0px',
            'font-size': '30px'
        })
])
,
  html.Hr(),
  #----------------
   html.Div(
    
    children=[
     html.H2(
        'Product Sales',
        style={
            'textAlign': 'center',
            'marginBottom': '5px',
            'font-size': '40px',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)'
        }
    ),


     
    dcc.Graph(figure=px.line(product_sales, x='productID', y='Sales')),
   
    html.H4([
    f"Maximum Product ID:{max_sales_date_product} , Sales: {max_sales_value_product}$", html.Br(),
    f"Minumum Product ID:{min_sales_date_product} , Sales: {min_sales_value_product}$" 
    
]
            ,style={
            'textAlign': 'center',
            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
            'marginTop':'0px',
            'font-size': '30px'
        })
])
  #---------------------------------------------
  ,html.Hr(),
   html.Div(
    children=[
        html.H2(
            'Shipping Costs Consistency',
            style={
                'textAlign': 'center',
                'marginBottom': '5px',
                'fontSize': '40px',
                'backgroundColor': 'rgba(255, 255, 255, 0.8)'
                
            }
        ),
        # Add the box plot graph
        dcc.Graph(figure=px.box(
        df_orders,
        x='shipperID',
        y='freight',
        color='shipperID',  # This will only work if 'CV' is a categorical column
        title='Box Plot of Freight by ShipperID with CV',
        labels={
            'freight': 'Freight Cost ($)',
            'shipperID': 'Shipper ID'
            
        })
    ),
html.Div(style={
                'textAlign': 'center',
                'marginBottom': '0px',
                'fontSize': '20px',
                'backgroundColor': 'rgba(255, 255, 255, 0.8)',
                'padding': '10px'
            },children=[html.H5('Detailed data'),
    dash_table.DataTable(data=merged_ship_name.to_dict('records'), page_size=10)
])
,
        # Additional text information (max/min sales)
        html.H4(
            children=[
                f"ID:1 , {categorize_consistency(c_s_array[0])}", html.Br(),
                f"ID:2 , {categorize_consistency(c_s_array[1])}",html.Br(),
                f"ID:3 , {categorize_consistency(c_s_array[2])}",html.Br(),
                f'Arrangements of Shippers from Lowest Consistency Score(best): {cS_rank}'
            ],
            style={
                'textAlign': 'center',
                'backgroundColor': 'rgba(255, 255, 255, 0.6)',
                'marginTop': '20px',  # Add space above this section
                'fontSize': '30px'
            }
        )
    ]),

  #------------------
  html.Hr(),html.Div(
    
    children=[
     html.H2(
        'Key customers',
        style={
            'textAlign': 'center',
            'marginBottom': '5px',
            'font-size': '40px',
            'backgroundColor': 'rgba(255, 255, 255, 0.8)'
        }
    ),
    dcc.Graph(figure=px.histogram(sales, x='customerID', y='Sales')),
   
    html.H4([
    f"1. {customer_1:<15}$ , ID: {customer_1_id}", html.Br(),
    f"2. {customer_2:<15}$ , ID: {customer_2_id}", html.Br(),
    f"3. {customer_3:<15}$ , ID: {customer_3_id}"
]
            ,style={
            'textAlign': 'center',
            'backgroundColor': 'rgba(255, 255, 255, 0.6)',
            'marginTop':'0px',
            'font-size': '30px'
        })
])


  ])
#----------------------------------------

#------------------------------------------

# Browser launch helpers
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def open_browser():
    time.sleep(3)
    if not is_port_in_use(8050):
        print("Server failed to start! Check terminal for errors.")
        return
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == '__main__':
    print("Starting server...")
    threading.Thread(target=open_browser).start()
    try:
        app.run(host='127.0.0.1', port=8050, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Failed to start server: {e}")

