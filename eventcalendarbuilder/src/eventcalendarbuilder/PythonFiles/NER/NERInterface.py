import spacy
import eventcalendarbuilder.PythonFiles.Managers.DirectoryManager as directory_manager
import logging

parent_dir = directory_manager.getCurrentFileDirectory(__file__)
model_path = directory_manager.getFilePath(parent_dir, 'model/model-best')

#model_path = "model/model-best"

class NERInterface:
    nlp = spacy.load(model_path) #load model   

    # Extracts entities from given text
    def GetEntitiesFromText(text:str):
        """
        Get the entities from doc and returns them. Current assumes that doc only has 1 of each

        :param text (str): The text to run the model on
        :return: The entities of event, time, date and loc. They can be null
        """
        if text == None or "":
            #print(f"[{__name__}] INVALID PARAM GIVEN!")
            logging.error(f"[{__name__}] INVALID PARAM GIVEN!")
            return

        doc = NERInterface.nlp(text) 
        entityList = list(doc.ents)
        events = []                

        if len(entityList) > 0 :
            tmp_time_list = []
            loc = ""
            event_name = ""
            curr_dt =None
            dt = {}

            for entity in entityList:
                e = str(entity)
                if entity.label_ == "E_NAME":
                    if event_name != e:

                        # To handle if first entity in list is event
                        if event_name == "":
                            event_name = e
                            continue
                        
                        # If date has more than 2 time, split each one up into its individual date
                        for d in dt:
                            if len(dt[d]) > 2:
                                tmp_key = d
                                del dt[d]
                                for t in dt[tmp_key]:
                                    dt[tmp_key] = t

                        events.append(NERInterface.getEntities(e=event_name, dt=dt, l=loc))
                        tmp_time_list = []
                        dt ={}
                        curr_dt = None
                        loc = ""
                        event_name = e # set name to the next entity

                elif entity.label_ == "E_DATE":
                    # Already encountered a time label before date
                    if len(tmp_time_list) > 0 and curr_dt != None:
                        dt[curr_dt] = tmp_time_list
                        tmp_time_list = []
                    curr_dt = entity
                    dt[curr_dt] = tmp_time_list

                elif entity.label_ == "E_TIME":
                    # Handle already encountered date
                    if curr_dt != None: dt[curr_dt].append(e)
                    else: tmp_time_list.append(e)

                elif entity.label_ == "E_LOC":
                    loc = e
                
                # Append what is left and return list of events
                if entity == entityList[-1] and entity.label_ != "E_NAME":
                    events.append(NERInterface.getEntities(e=event_name, dt=dt, l=loc))
                    return events
                
        return events
    
    # Creates NER entity dataype
    def getEntities(e : str, dt : list, l : str):
        return {
            "EVENT" : e,
            "DATE_TIME" : dt,
            "LOC" : l,
        }