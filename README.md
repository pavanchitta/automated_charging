Venmo requests for PG&E



Getting the bill payments
Ability to get this in the future every month
Or from an offline source (downloaded CSV) for previous payments
Processing the payment information
Get the amount to charge
Call the venmo API
Cron job to run the above in a loop



class Transaction
	amount: float
	date: datetime / str


Interface TransactionExtractor
GetAllPayments, GetPaymentsWithinTimeRange, GetLatestPayment
One that extracts from offline CSV
One that tries to extract from online

Then compose this TransactionExtractor behavior into another class, 
PaymentRequester, which maybe VenmoRequester subclasses. Can have simple behavior like MakeRequest. Problem is signature might be different for different concrete classes, e.g. form of ID. Maybe just allow for an untyped payload dict

Can also have an adapter interface responsible for generating the input CSV that the
Transaction extractor operates over. Can have a PGE version of this which just generates from the
initial raw CSV. But in the future this could be from other bills, etc.

Need to have a Venmo Client class which supports basic functionality.
- Need to be able to MakeCharge(Amount, PersonId, description)
- Need to figure out how to manage all the credentials / env variables that give
  sufficient permissions for this.