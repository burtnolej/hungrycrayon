def list_append(array,obj,attribute,value_flag=False):
    if hasattr(obj,attribute):
        if value_flag == False:
            array.append(getattr(obj,attribute))
        else:
            item = getattr(obj,attribute)
            if hasattr(item,"Value"):
                array.append(getattr(item,"Value"))
            else:
                array.append(-1)
    else:
        array.append(-1)