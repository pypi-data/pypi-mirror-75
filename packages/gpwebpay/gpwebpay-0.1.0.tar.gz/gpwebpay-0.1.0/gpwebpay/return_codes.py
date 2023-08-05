PRCODE = {
    "0": "OK",
    "1": "Field too long",
    "2": "Field too short",
    "3": "Incorrect content of field",
    "4": "Field is null",
    "5": "Missing required field",
    "6": "Missing field",
    "11": "Unknown merchant",
    "14": "Duplicate order number",
    "15": "Object not found",
    "16": "Amount to approve exceeds payment amount",
    "17": "Amount to deposit exceeds approved amount",
    "18": "Total sum of credited amounts exceeded deposited amount",
    "20": "Object not in valid state for operation",
    "25": "Operation not allowed for user",
    "26": "Technical problem in connection to authorization center",
    "27": "Incorrect payment type",
    "28": "Declined in 3D",
    "30": "Declined in AC",
    "31": "Wrong digest",
    "32": "Expired card",
    "33": "Original/Master order was not authorized",
    "34": "Original/Master order is not valid for subsequent payment",
    "35": "Session expired",
    "38": "Card not supported",
    "40": "Declined in Fraud detection system",
    "50": "The cardholder canceled the payment",
    "80": "Duplicate MessageId",
    "82": "HSM key label missing",
    "83": "Canceled by issuer",
    "84": "Duplicate value",
    "85": "Declined due to merchant’s rules",
    "200": "Additional info request",
    "300": "Soft decline – issuer requires SCA",
    "1000": "Technical problem",
}


SRCODE = {
    "1": "ORDERNUMBER",
    "2": "MERCHANTNUMBER",
    "3": "PAN",
    "4": "EXPIRY",
    "5": "CVV",
    "6": "AMOUNT",
    "7": "CURRENCY",
    "8": "DEPOSITFLAG",
    "10": "MERORDERNUM",
    "11": "CREDITNUMBER",
    "12": "OPERATION",
    "14": "ECI",
    "18": "BATCH",
    "22": "ORDER",
    "24": "URL",
    "25": "MD",
    "26": "DESC",
    "34": "DIGEST",
    "43": "ORIGINAL ORDER NUMBER",
    "45": "USERPARAM1",
    "70": "VRCODE",
    "71": "USERPARAM2",
    "72": "FASTPAYID",
    "73": "PAYMETHOD",
    "83": "ADDINFO",
    "84": "MPS_CHECKOUT_ID",
    "86": "PAYMETHODS",
    "88": "DEPOSIT_NUMBER",
    "89": "RECURRING_ORDER",
    "90": "PAIRING",
    "91": "SHOP_ID",
    "92": "PANPATTERN",
    "93": "TOKEN",
    "95": "FASTTOKEN",
    "96": "SUBMERCHANT INFO",
    "97": "TOKEN_HSM_LABEL",
    "98": "CUSTOM INSTALLMENT COUNT",
    "99": "COUNTRY",
    "100": "TERMINAL INFO",
    "101": "TERMINAL ID",
    "102": "TERMINAL OWNER",
    "103": "TERMINAL CITY",
    "104": "MC ASSIGNED ID",
    # TODO: Add the rest of the codes
    #  If PRCODE == 28
    #  If PRCODE == 30
}
