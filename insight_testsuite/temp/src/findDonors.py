
# !/usr/bin/python


# define function: median
def get_median(lst):
    sorted_list = sorted(lst)
    list_len = len(lst)
    index = (list_len - 1) // 2

    if list_len % 2:
        return int(round(float(sorted_list[index])))
    else:
        return int(round(float((sorted_list[index] + sorted_list[index + 1])/2.0)))


# generate file for medianvals_by_zip.txt
def build_zip(dic, receiver, zipcode):
    zip_list = dic[receiver][zipcode]
    median = get_median(zip_list)
    number = len(zip_list)
    total = sum(zip_list)
    result = receiver + '|' + zipcode+ '|' + str(median)+ '|' + str(number) + '|' + str(total)
    text_file_zip.write(result + '\n')


# generate file for medianvals_by_date.txt
def build_date(dic):
    for id in sorted(dic.iterkeys()):
        for dt in sorted(dic[id].iterkeys(), key=int):
            median = get_median(dic[id][dt])
            number = len(dic[id][dt])
            total = sum(dic[id][dt])

            if len(str(dt)) == 7:
                new_date = str(0) + str(dt)
            else:
                new_date = str(dt)
            result = id + '|' + new_date + '|' + str(median) + '|' + str(number) + '|' + str(total)
            text_file_date.write(result + '\n')


# add elements to dictionary
def build_dict(dic, recipient_id, group_by):
    # add things to dic_date
    if recipient_id not in dic:
        dic[recipient_id] = {}
        dic[recipient_id][group_by] = []
    elif group_by not in dic[recipient_id]:
        dic[recipient_id][group_by] = []
    dic[recipient_id][group_by].append(amount)

# the outputs of step 1 is stored in input_infos
dic_zip = {}
dic_date = {}

filepath_zip = "./output/medianvals_by_zip.txt"
text_file_zip = open(filepath_zip, "w")
filepath_date = "./output/medianvals_by_date.txt"
text_file_date = open(filepath_date, "w")


with open("./input/itcont.txt") as f:

    # Test the code on first five lines.
    # head = [next(f) for x in xrange(3)]

    for line in f:
        text = line.split('|')

        other = text[15]
        recipient = text[0]
        fullzip = text[10]
        amount = int(text[14])
        date = text[13]

        # ignore the record if other is not empty, and empty cells in the CMTE_ID or TRANSACTION_AMT fields

        if other == '' and recipient != '' and amount != '':

            # ignore the record in _by_zip.txt if ZIP_CODE is an invalid zipcode (i.e., empty, fewer than five digits)
            if len(fullzip) >= 5:
                zip = fullzip[:5]

                # add things to dic_zip
                build_dict(dic_zip, recipient, zip)
                build_zip(dic_zip, recipient, zip)

            if len(date) == 8:
                build_dict(dic_date, recipient, date)

build_date(dic_date)

text_file_zip.close()
text_file_date.close()

