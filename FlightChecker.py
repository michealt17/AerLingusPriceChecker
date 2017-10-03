import requests
import json
import smtplib


email = '<EMAIL>'
password = '<PASSWORD>'
recipient_email = '<RECIPIENT_EMAIL>'

def search_flights(numAdults, departureDate, returnDate, 
                   outboundOriginCode, outboundDestinationCode, inboundOriginCode, inboundDestinationCode):
    
    headers = {'Content-Type': 'application/json'}
    url = "https://www.aerlingus.com/api/search/fixedFlight"
    payload = {
					"fareCategory": "ECONOMY",
					"fareType": "MULTI",
					"flightJourneySearches": [
						{
							"departureDate": departureDate,
							"sourceAirportCode": outboundOriginCode,
							"destinationAirportCode": outboundDestinationCode
						},
						{
							"departureDate": returnDate,
							"sourceAirportCode": inboundOriginCode,
							"destinationAirportCode": inboundDestinationCode
						}
					],
					"groupBooking": "false",
					"numAdults": numAdults,
					"numChildren": 0,
					"numInfants": 0,
					"numYoungAdults": 0,
					"promoCode": ""
				}

    r = requests.post(url, data=json.dumps(payload), headers=headers)    
    result = json.loads(r.text)
    #print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ': ')))
    
    total = 0
    output = ""
    for flight in result['data'][0]['flightOptions']:
        output += flight['sourceAirportName'] + ' -> ' + flight['destinationAirportName'] + '\n'
        output += 'Price: EURO ' + str(flight['airJourney'][0]['lowPrice']) + '\n'
        output += 'Seats remaining at this price: ' + str(flight['airJourney'][0]['lowPriceAvailableSeats']) + '\n'
        total += (flight['airJourney'][0]['lowPrice']*2)
        output += '\n'
    
    output += 'Total: EURO ' + str(total)
    return output

def send_email(user, pwd, recipient, subject, body):

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except Exception as e: 
        print ("failed to send mail")
        print(e)
	
if __name__ == '__main__':
    bodyText = search_flights(2, '2018-05-04', '2018-05-16', 'DUB', 'SFO', 'NYC', 'DUB')
    print(bodyText)
    send_email(email, password, recipient_email, "Flights Prices", bodyText)