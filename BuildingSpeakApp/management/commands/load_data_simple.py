import csv, smtplib, requests, datetime, pytz
from email.mime.text import MIMEText
from BuildingSpeakApp.models import Equipment
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        #add code to iterate over all models and load data if file exists AND
        #   if file is not the default instantiation file
        #   or maybe if 'channel_list' is empty or some other check that would indicate
        #   no data files need to be processed (vs. needs to be but isn't where it's supposed to be)
        r1 = Equipment.objects.get(pk=3)
        
        r = requests.get(r1.channel_file.url)
        if r.status_code == 404:
            pass #do something because the file isn't there!
        elif r.status_code == 200:
            pass #then do the reader/loader stuff below, need to pull that up into here
        else:
            pass #do something else because we don't know why but we're not geting the file!
        csvfilereader = csv.reader(r1.channel_file, delimiter=',', quotechar='|')
        for lastrow in csvfilereader:
            pass
        tempV = [1,2,3,4] #using tempV[i] instead of r1.V[i] which is float not int, will get fixed when I create real fields
        for i,val in enumerate(r1.channel_list):
            #if val == 'timestamp': time_object = dt.strptime(lastrow[r1.V[i]],r1.name)
            x = r1.__getattribute__(val)
            x.extend([lastrow[tempV[i]]])
            r1.__setattr__(val,x)
        r1.save()

        # Message to be sent
        message = MIMEText("Updated %s." % r1.name)
        
        # Sending email username/password and receiving phone number
        email_username = "dashley@drydenengineering.com"
        email_password = "Dryden030211!"
        destination = "gte647i@gmail.com"        
        #destination = "6788367759@vtext.com"
        
        # Gmail to Verizon. Change here for different combinations.
        #email_username += "@gmail.com"
        #phone_number += "@vtext.com"
        #visit for help on SMS: http://en.wikipedia.org/wiki/List_of_SMS_gateways
        
        # Format message to look like an email
        message["From"] = "dashley@drydenengineering.com"
        message["To"] = destination
        message["Subject"] = "updated %s on %s" % (r1.name, timezone.now().ctime())
        
        # Connect and send
        s = smtplib.SMTP('oxmail.registrar-servers.com:26')
        s.starttls()
        s.login(email_username, email_password)
        s.sendmail(email_username, destination, message.as_string())
        s.quit()