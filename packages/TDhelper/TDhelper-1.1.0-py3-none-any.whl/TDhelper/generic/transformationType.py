import datetime

def transformation(value, transformationType):
    try:
        if not isinstance(transformationType,int):
            value= int(value)
        if not isinstance(transformationType,str):
            if isinstance(type(value), datetime.datetime):
                value= datetime.datetime.strftime(value,'%Y-%m-%d %H:%M:%S')
            else:
                value= str(value)
        if not isinstance(transformationType, datetime.datetime):
            if isinstance(type(value),str):
                value= datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            else:
                raise Exception('value type must is str.')
        if not isinstance(transformationType,bool):
            if value:
                value= True
            else:
                value= False
    except Exception as e:
        raise e
    return value