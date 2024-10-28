compatible={'O+': '''Minor antigen discripencies i.e antigens like
Kell ,ouffy etc.It wii leading to delayed homolytic
aattacks,& Recipients might have mild allergic
reactions& also risk of fever due to reation with donor
WBC.''',
'O-': '''Minor antigen discripencies i.e antigens like
Kell ,ouffy etc.It wii leading to delayed homolytic
aattacks,& Recipients might have mild allergic
reactions& also risk of fever due to reation with donor
WBC.''',
'A+': '''Recipients might have some possibility of mild
allergies& minor atigen i.e Lewis Antigen leads to
homolytic reaction.''',
'A-': '''Recipients might have some possibility of mild
allergies& minor atigen i.e Lewis Antigen leads to
homolytic reaction.''',
'B-': '''Variation of antigen i.e MNS antigen could lead to
Homolytic reaction& recipient might have allegic
reactions.''',
'B+': '''Variation of antigen i.e MNS antigen could lead to
Homolytic reaction& recipient might have allegic
reactions.''',
'AB+': '''Recipients have Rh antigen discrepencies& possibility
of allegic reactions & possibility of fever in recipients.''',
'AB-': '''Recipients have Rh antigen discrepencies& possibility
of allegic reactions & possibility of fever in recipients.'''}
all=['A+', 'A-', 'AB+', 'AB-', 'B+', 'B-', 'O+', 'O-']
recievers={'O+':['O+', 'O-'],
           'O-':['O-'],
           'A+':['A+', 'A-','O+', 'O-'],
           'A-':['A-','O-'],
           'B+':['B+', 'B-', 'O+', 'O-'],
           'B-':['B-','O-'],
           'AB+':all,
           'AB-':all[1::2]}


# print(recievers)
def compatiblity_checking(donor_blood_group,reciver_blood_group):
    donor_blood_group=donor_blood_group.upper()
    reciver_blood_group=reciver_blood_group.upper()
    possibility=recievers[reciver_blood_group]
    string=""
    if donor_blood_group in possibility:
        string="Compatible"
    else:
        string="Not Compatible"
    if string == "Compatible":
        return ['Compatible',compatible[reciver_blood_group]]
    else:
        return ["Not Compatible"]