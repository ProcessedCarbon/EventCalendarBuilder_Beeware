class GoogleEvent:
    def __init__(self, event: str, 
                 location: str, 
                 start_datetime: str, 
                 end_datetime: str, 
                 tzstart: str, 
                 tzend:str, 
                 rrule:str,
                 colorId=1,
                 ):
        
        self.event = {
            "summary" : event,
            "location" : location,
            "description" : "Test description",
            "colorId" : colorId,
            "start" : {
                "dateTime" : start_datetime,
                "timeZone" : tzstart
            },
            "end" : {
                "dateTime" : end_datetime,
                "timeZone" : tzend
            },
            'recurrence': [
                rrule
            ],
            # "attendees" : [
            #     {"email":"nonexistantemail@mail.com"}
            # ]
        }

    def __repr__(self):
        return f"GoogleEvent(event='{self.event}')"
    
    def getEvent(self)->str:
        return self.event['summary']
    
    def getLocation(self)->str:
        return self.event['location']
    
    def getStartDate(self)->str:
        return self.event['start']['dateTime']
    
    def getStartTz(self)->str:
        return self.event['start']['timeZone']
    
    def getEndDate(self)->str:
        return self.event['end']['dateTime']
    
    def getEndTz(self)->str:
        return self.event['end']['timeZone']
    
    #['RRULE:FREQ=DAILY;UNTIL=20230215T220000Z']
    def getRRULE(self)->str:
        return self.event['recurrence'][0]
    
    def getRRULEDict(self)->dict:
        if len(self.getRRULE()) == 0:
            return {}
        
        rules = self.getRRULE().split(';')
        rule_dict = {}
        for r in rules:
            split = r.split('=')
            rule_dict[split[0]] = split[1]
        return rule_dict
    
    def getUNTILDate(self)->str:
        '''
        Returns UNTIL date is there is one in the recurrence param, if not just returns End Date
        '''
        rules = self.getRRULEDict()
        if len(rules) > 0:
            r_date = rules['UNTIL']
            _until = self.getEndDate()
            _until = _until.replace(_until[:4], r_date[:4])
            _until = _until.replace(_until[5:7], r_date[4:6])
            _until = _until.replace(_until[8:10], r_date[6:8])
            return _until
        else:
            #print('NO UNTIL DATE IN RRULE')
            return self.getEndDate()
