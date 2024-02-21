import unicodedata as uni

test = 'Width : 36 ½ "'
test2 = 'Weight :  15 lb 4 oz'
def measure_break(measurement):
    list = [None,[[],[]],0]
    list[0] = measurement.split(":")[0][:-1].lower()
    measure = measurement.split(":")[1][1:] if uni.name(measurement.split(":")[1][:1]).split()[-1] == "SPACE" else measurement.split(":")[1]
    for piece in measure.split():
        measure_stage = list[2]
        if piece.isnumeric():
            try:
                piece = uni.numeric(piece)
            except TypeError: pass
            try:
                list[1][0][measure_stage]+=float(piece)
            except:
                list[1][0].append(float(piece))
        
        elif piece.isalpha():
            list[1][1].append(piece)
            if len(list[1][0]) < list[2]+1: list[1][0].append(0)
            list[2]+=1
        else:
            try:
                if uni.name(piece).split()[0] in ["APOSTROPHE", "QUOTATION"]:
                    list[1][1].append(piece)
                    if len(list[1][0]) < list[2]+1: list[1][0].append(0)
                    list[2]+=1
            except: pass
    list_output = [0, None]
    list_output = unit_conversion(list[1])
    return [list[0], list_output]

def unit_conversion(measurement_list):
    list_output = [0, None]
    for n in range(len(measurement_list[0])):
        try:
            if uni.name(measurement_list[1][n]).split()[0] == "APOSTROPHE":
                coef = 12
            elif uni.name(measurement_list[1][n]).split()[0] == "QUOTATION":
                coef = 1
            if list_output[1] == None: list_output[1] = "inches"
            if list_output[1] == "inches": list_output[0] += (coef * measurement_list[0][n])
        except:
            if measurement_list[1][n] == "lb":
                coef = 1
            elif measurement_list[1][n] == "oz":
                coef = 0.0625
            if list_output[1] == None: list_output[1] = "lb"
            if list_output[1] == "lb": list_output[0] += (coef * measurement_list[0][n])
    return list_output

print(measure_break(test))