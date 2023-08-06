#Copyright 2020 Guillaume Karklins
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

"""
Author: Guillaume Karklins
Creation date: August 2020
Last edit date: August 2020
Comment: this file introduces liquidity ratio functions.
""" 


def current_ratio(current_assets, current_liabilities, decimals=0):
    #this function calculates the current ratio
    
    cr = current_assets / current_liabilities
     
    if decimals != 0:   
        try:
            cr = round(cr, decimals)
        except TypeError:
            print("decimals must be an integer")
            
    return cr

         
def cash_ratio(cash, current_liabilities, decimals=0):
    #this function calculates the cash ratio
    
    cr = cash / current_liabilities
     
    if decimals != 0:   
        try:
            cr = round(cr, decimals)
        except TypeError:
            print("decimals must be an integer")
            
    return cr


def cashtoworkcap_ratio(cash, current_assets, current_liabilities, decimals=0):
    #this function calculates the cash to working capital ratio
    
    cr = cash / (current_assets - current_liabilities)
     
    if decimals != 0:   
        try:
            cr = round(cr, decimals)
        except TypeError:
            print("decimals must be an integer")
            
    return cr


def quick_ratio(current_liabilities, quick_assets=None, cash=None, receivables=None, mark_securities=None,
                current_assets=None, inventory=None, current_prepaid_assets=None, decimals=0):
    #this function calculates the quick ratio, 3 possible manners depending inputs provided
    
    if quick_assets is not None:
        qr = quick_assets / current_liabilities
        
    elif (cash is not None) and (receivables is not None) and  (mark_securities is not None):
        qr = (cash + receivables + mark_securities) / current_liabilities
        
    elif (current_assets is not None) and (inventory is not None) and (current_prepaid_assets is not None):
        qr = (current_assets - inventory - current_prepaid_assets) / current_liabilities
        
    else:
        raise ValueError("quick_assets or cash/receivables/mark_securities or current_assets/inventory/current_prepaid_assets must be specified")
    
     
    if decimals != 0:   
        try:
            qr = round(qr, decimals)
        except TypeError:
            print("decimals must be an integer")
            
    return qr


#end