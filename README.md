# *AWS Chat Client*
---

## AWS Chat Client
This project covers the use of the AWS Cloud Computing system to create and customize a CUI for deployment. 

>"How may I help you today?"

## Technologies 

This project uses Python, AWS Lex, AWS Lambda, to test and deploy cloud based CUI tools. 

[AWS Lex](https://aws.amazon.com/lex/)
[AWS Lambda](https://aws.amazon.com/lambda/)

### Installation Guide

In order to use this program please create an account at [AMAZON AWS](https://aws.amazon.com/). The following portions of code were used in the Lambda Function.  
```python
from datetime import datetime
from dateutil.relativedelta import relativedelta
```

## Usage 
the following blocks of python code were written to complete the Lambda functionality. NOTE: code is not functioning as of 7/31/22.  

```python 
def get_recommendation():
    if risk_level == "None":
        print(f"100% bonds (AGG), 0% equities (SPY).")
    
    elif risk_level == "Low":
         print(f"60% bonds (AGG), 40% equities (SPY).")
        
    elif risk_level == "Medium":
          print(f"40% bonds (AGG), 60% equities (SPY).")

    elif risk_level == "High": 
         print("20% bonds (AGG), 80% equities (SPY).")
        
    else:
        print(f"Please select a valid risk level.")
        
```
This else/if sequence is meant to output a portfolio recommendation based on user input in the Lex CUI. 

```python
def validate_data(age, investment_amount, intent_request):
    """
    Validates the data provided by the user.
    """

    #  age should be > 0 and < 65
    if age is not None:
        parse_int(age)
        if age > 0 and age < 65:
            return build_validation_result(
                False,
                "age",
                "You should be between ages of 1 and 65 to use this service, "
                "please provide a different date of birth.",
            )

    #  investment_amount should be >= 5000
    if investment_amount is not None:   
        parse_int(investment_amount)
        if investment_amount >= 5000:
            return build_validation_result(
                False,
                "investmentAmount",
                "please provide an amount greater than or equal to 5000.",
            )

    # A True results is returned if age or amount are valid
    return build_validation_result(True, None, None)

```
These functions are meant to validate the age of the user and the amount of the investment that they would like to make in the chat client. 

SEE MORE: Brief videos in repository show working chat client and currently non-functioning Lambda execution layer. 

## Contributors

Jeffrey J. Wiley Jr

## License

MIT



