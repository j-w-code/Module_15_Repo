{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "044f803c-78fe-4020-8255-e8675e48a4d9",
   "metadata": {},
   "outputs": [],
   "source": [
    "### Required Libraries ###\n",
    "from datetime import datetime\n",
    "from dateutil.relativedelta import relativedelta\n",
    "\n",
    "### Functionality Helper Functions ###\n",
    "def parse_int(n):\n",
    "    \"\"\"\n",
    "    Securely converts a non-integer value to integer.\n",
    "    \"\"\"\n",
    "    try:\n",
    "        return int(n)\n",
    "    except ValueError:\n",
    "        return float(\"nan\")\n",
    "\n",
    "\n",
    "def get_recommendation():\n",
    "    if risk_level == \"None\":\n",
    "        print(f\"100% bonds (AGG), 0% equities (SPY).\")\n",
    "    \n",
    "    elif risk_level == \"Low\":\n",
    "         print(f\"60% bonds (AGG), 40% equities (SPY).\")\n",
    "        \n",
    "    elif risk_level == \"Medium\":\n",
    "          print(f\"40% bonds (AGG), 60% equities (SPY).\")\n",
    "\n",
    "    elif risk_level == \"High\": \n",
    "         print(\"20% bonds (AGG), 80% equities (SPY).\")\n",
    "        \n",
    "    else:\n",
    "        print(f\"Please select a valid risk level.\")\n",
    "        \n",
    "\n",
    "\n",
    "def build_validation_result(is_valid, violated_slot, message_content):\n",
    "    \"\"\"\n",
    "    Define a result message structured as Lex response.\n",
    "    \"\"\"\n",
    "    if message_content is None:\n",
    "        return {\"isValid\": is_valid, \"violatedSlot\": violated_slot}\n",
    "\n",
    "    return {\n",
    "        \"isValid\": is_valid,\n",
    "        \"violatedSlot\": violated_slot,\n",
    "        \"message\": {\"contentType\": \"PlainText\", \"content\": message_content},\n",
    "    }\n",
    "\n",
    "def validate_data(age, investment_amount, intent_request):\n",
    "    \"\"\"\n",
    "    Validates the data provided by the user.\n",
    "    \"\"\"\n",
    "\n",
    "    #  age should be > 0 and < 65\n",
    "    if age is not None:\n",
    "        parse_int(age)\n",
    "        if age > 0 and age < 65:\n",
    "            return build_validation_result(\n",
    "                False,\n",
    "                \"age\",\n",
    "                \"You should be between ages of 1 and 65 to use this service, \"\n",
    "                \"please provide a different date of birth.\",\n",
    "            )\n",
    "\n",
    "    #  investment_amount should be >= 5000\n",
    "    if investment_amount is not None:   \n",
    "        parse_int(investment_amount)\n",
    "        if investment_amount >= 5000:\n",
    "            return build_validation_result(\n",
    "                False,\n",
    "                \"investmentAmount\",\n",
    "                \"please provide an amount greater than or equal to 5000.\",\n",
    "            )\n",
    "\n",
    "    # A True results is returned if age or amount are valid\n",
    "    return build_validation_result(True, None, None)\n",
    "\n",
    "### Dialog Actions Helper Functions ###\n",
    "def get_slots(intent_request):\n",
    "    \"\"\"\n",
    "    Fetch all the slots and their values from the current intent.\n",
    "    \"\"\"\n",
    "    return intent_request[\"currentIntent\"][\"slots\"]\n",
    "\n",
    "\n",
    "def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):\n",
    "    \"\"\"\n",
    "    Defines an elicit slot type response.\n",
    "    \"\"\"\n",
    "\n",
    "    return {\n",
    "        \"sessionAttributes\": session_attributes,\n",
    "        \"dialogAction\": {\n",
    "            \"type\": \"ElicitSlot\",\n",
    "            \"intentName\": intent_name,\n",
    "            \"slots\": slots,\n",
    "            \"slotToElicit\": slot_to_elicit,\n",
    "            \"message\": message,\n",
    "        },\n",
    "    }\n",
    "\n",
    "\n",
    "def delegate(session_attributes, slots):\n",
    "    \"\"\"\n",
    "    Defines a delegate slot type response.\n",
    "    \"\"\"\n",
    "\n",
    "    return {\n",
    "        \"sessionAttributes\": session_attributes,\n",
    "        \"dialogAction\": {\"type\": \"Delegate\", \"slots\": slots},\n",
    "    }\n",
    "\n",
    "\n",
    "def close(session_attributes, fulfillment_state, message):\n",
    "    \"\"\"\n",
    "    Defines a close slot type response.\n",
    "    \"\"\"\n",
    "\n",
    "    response = {\n",
    "        \"sessionAttributes\": session_attributes,\n",
    "        \"dialogAction\": {\n",
    "            \"type\": \"Close\",\n",
    "            \"fulfillmentState\": fulfillment_state,\n",
    "            \"message\": message,\n",
    "        },\n",
    "    }\n",
    "\n",
    "    return response\n",
    "\n",
    "\n",
    "\"\"\"\n",
    "Step 3: Enhance the Robo Advisor with an Amazon Lambda Function\n",
    "\n",
    "In this section, you will create an Amazon Lambda function that will validate the data provided by the user on the Robo Advisor.\n",
    "\n",
    "1. Start by creating a new Lambda function from scratch and name it `recommendPortfolio`. Select Python 3.7 as runtime.\n",
    "\n",
    "2. In the Lambda function code editor, continue by deleting the AWS generated default lines of code, then paste in the starter code provided in `lambda_function.py`.\n",
    "\n",
    "3. Complete the `recommend_portfolio()` function by adding these validation rules:\n",
    "\n",
    "    * The `age` should be greater than zero and less than 65.\n",
    "    * The `investment_amount` should be equal to or greater than 5000.\n",
    "\n",
    "4. Once the intent is fulfilled, the bot should respond with an investment recommendation based on the selected risk level as follows:\n",
    "\n",
    "    * **none:** \"100% bonds (AGG), 0% equities (SPY)\"\n",
    "    * **low:** \"60% bonds (AGG), 40% equities (SPY)\"\n",
    "    * **medium:** \"40% bonds (AGG), 60% equities (SPY)\"\n",
    "    * **high:** \"20% bonds (AGG), 80% equities (SPY)\"\n",
    "\n",
    "> **Hint:** Be creative while coding your solution, you can have all the code on the `recommend_portfolio()` function, or you can split the functionality across different functions, put your Python coding skills in action!\n",
    "\n",
    "5. Once you finish coding your Lambda function, test it using the sample test events provided for this Challenge.\n",
    "\n",
    "6. After successfully testing your code, open the Amazon Lex Console and navigate to the `recommendPortfolio` bot configuration, integrate your new Lambda function by selecting it in the “Lambda initialization and validation” and “Fulfillment” sections.\n",
    "\n",
    "7. Build your bot, and test it with valid and invalid data for the slots.\n",
    "\n",
    "\"\"\"\n",
    "\n",
    "\n",
    "### Intents Handlers ###\n",
    "def recommend_portfolio(intent_request):\n",
    "    \"\"\"\n",
    "    Performs dialog management and fulfillment for recommending a portfolio.\n",
    "    \"\"\"\n",
    "\n",
    "    first_name = get_slots(intent_request)[\"firstName\"]\n",
    "    age = get_slots(intent_request)[\"age\"]\n",
    "    investment_amount = get_slots(intent_request)[\"investmentAmount\"]\n",
    "    risk_level = get_slots(intent_request)[\"riskLevel\"]\n",
    "    source = intent_request[\"invocationSource\"]\n",
    "  \n",
    "    if source == \"DialogCodeHook\":\n",
    "        # This code performs basic validation on the supplied input slots.\n",
    "\n",
    "        # Gets all the slots\n",
    "        slots = get_slots(intent_request)\n",
    "\n",
    "        # Validates user's input using the validate_data function\n",
    "        validation_result = validate_data(age, investment_amount, intent_request)\n",
    "\n",
    "        # If the data provided by the user is not valid,\n",
    "        # the elicitSlot dialog action is used to re-prompt for the first violation detected.\n",
    "        if not validation_result[\"isValid\"]:\n",
    "            slots[validation_result[\"violatedSlot\"]] = None  # Cleans invalid slot\n",
    "\n",
    "            # Returns an elicitSlot dialog to request new data for the invalid slot\n",
    "            return elicit_slot(\n",
    "                intent_request[\"sessionAttributes\"],\n",
    "                intent_request[\"currentIntent\"][\"name\"],\n",
    "                slots,\n",
    "                validation_result[\"violatedSlot\"],\n",
    "                validation_result[\"message\"],\n",
    "            )\n",
    "\n",
    "        # Fetch current session attributes\n",
    "        output_session_attributes = intent_request[\"sessionAttributes\"]\n",
    "\n",
    "        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.\n",
    "        return delegate(output_session_attributes, get_slots(intent_request))\n",
    "\n",
    "    #investment recommendation\n",
    "    recommendation = get_recommendation()\n",
    "    # Return a message with conversion's result.\n",
    "    return close(\n",
    "        intent_request[\"sessionAttributes\"],\n",
    "        \"Fulfilled\",\n",
    "        {\n",
    "            \"contentType\": \"PlainText\",\n",
    "            \"content\": \"\"\"Thank you for your information;\n",
    "             Good luck with your portfolio.\n",
    "            \"\"\".format(\n",
    "                recommendation\n",
    "            ),\n",
    "        },\n",
    "    )\n",
    "    \n",
    "  \n",
    "  \n",
    "\n",
    "### Intents Dispatcher ###\n",
    "def dispatch(intent_request):\n",
    "    \"\"\"\n",
    "    Called when the user specifies an intent for this bot.\n",
    "    \"\"\"\n",
    "\n",
    "    intent_name = intent_request[\"currentIntent\"][\"name\"]\n",
    "\n",
    "    # Dispatch to bot's intent handlers\n",
    "    if intent_name == \"recommendPortfolio\":\n",
    "        return recommend_portfolio(intent_request)\n",
    "\n",
    "    raise Exception(\"Intent with name \" + intent_name + \" not supported\")\n",
    "\n",
    "\n",
    "### Main Handler ###\n",
    "def lambda_handler(event, context):\n",
    "    \"\"\"\n",
    "    Route the incoming request based on intent.\n",
    "    The JSON body of the request is provided in the event slot.\n",
    "    \"\"\"\n",
    "\n",
    "    return dispatch(event)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "dev",
   "language": "python",
   "name": "dev"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
