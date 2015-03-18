# -*- coding: utf-8 -*-
# !/bin/env python

class Patient:
    def __init__(self, patient_id, district, school, class_name, name, gender, dob, contact_info, height, weight, fat,
                 fat_percentage, bmi, fat_type, basic_metabolism, measured_angle, x_ray_num,
                 cobb_section, cobb_degree, is_checked):
        self.patient_id = patient_id
        self.district = district
        self.school = school
        self.class_name = class_name
        self.name = name
        self.gender = gender
        self.dob = dob
        self.contact_info = contact_info
        self.height = height
        self.weight = weight
        self.fat = fat
        self.fat_percentage = fat_percentage
        self.bmi = bmi
        self.fat_type = fat_type
        self.basic_metabolism = basic_metabolism
        self.measured_angle = measured_angle
        self.x_ray_num = x_ray_num
        self.cobb_section = cobb_section
        self.cobb_degree = cobb_degree
        self.is_checked = is_checked

    def __str__(self):
        return '[Patient: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]' % (
            self.patient_id, self.district, self.school, self.class_name, self.name, self.gender, self.dob,
            self.contact_info, self.height, self.weight, self.fat, self.fat_percentage, self.bmi, self.fat_type,
            self.basic_metabolism,
            self.measured_angle, self.x_ray_num, self.cobb_section, self.cobb_degree, self.is_checked)

    def check(self, x_ray_num, cobb_section, cobb_degree):
        self.x_ray_num = x_ray_num
        self.cobb_section = cobb_section
        self.cobb_degree = cobb_degree
        self.is_checked = True


if __name__ == '__main__':
    p = Patient(1, "district ", "school ", "class ", u"姓名 ", u"男", "2008/11/18", 120, 20, 'fat',
                0.2, 20, 'fat_type', 'basic_metabolism',
                "contact information ********************* ", "measured angle ", "", "", "", False)
    for key in p.__dict__:
        print key, '=>', getattr(p, key)

    print unicode(p)